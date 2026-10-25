"""Stage 2 of round 6: an open model that learns from its own games (expert iteration), so that the fines it paid shape
its behaviour instead of only being told (docs/STAKES_DESIGN.md, section 4; registered as amendment 8 before the
first training run).

One iteration k: the current model plays self-play in the fine and leniency regimes; within every pool session the
top quarter of agents by net points (market points minus penalties plus rewards) is selected; every valid decision of
these agents becomes a training example (the exact system and user messages the model saw, its JSON answer as the
target); a LoRA adapter is trained on the base weights from the selected examples of iterations 1 to k; the adapter is
served next to the base model and plays iteration k + 1.

    python3 -m cartelbench.expert_iteration plan                          # every command of the registered loop
    python3 -m cartelbench.expert_iteration select --iteration 1          # training set from iteration 1's self-play
    python3 -m cartelbench.expert_iteration train --data <jsonl> --model <path> --out <dir>   # LoRA (GPU; CPU for tests)
    python3 -m cartelbench.expert_iteration evaluate                      # trained minus base, four core regimes
    python3 -m cartelbench.expert_iteration tiny-test                     # whole pipeline on the CPU, tiny random model

Torch, transformers and peft are imported only by `train` and `tiny-test`; selection and evaluation need neither.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import random
import re
import sys
from dataclasses import asdict, dataclass, field

from .util import EVIDENCE_DIR, evidence_header, read_jsonl, write_json

OUT = EVIDENCE_DIR / "stage2"
RUNS = OUT / "runs"


@dataclass(frozen=True)
class EIConfig:
    base_repo: str = "unsloth/Meta-Llama-3.1-8B-Instruct"        # pinned in PREREGISTRATION_provider2.md
    base_revision: str = "a2856192dd7c25b842431f39c179a6c2c2f627d1"
    served_base: str = "llama-3.1-8b-instruct"
    iterations: int = 3
    selfplay_regimes: tuple = ("fine", "leniency")
    selfplay_duopoles: int = 40
    selfplay_pools: int = 8
    eval_regimes: tuple = ("laissez_faire", "fine", "leniency", "reward")
    eval_duopoles: int = 20
    eval_pools: int = 4
    top_share: float = 0.25
    max_examples: int = 4000
    min_examples: int = 500
    min_json_validity: float = 0.90
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: tuple = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
    lr: float = 1e-4
    warmup_share: float = 0.03
    epochs: int = 1
    micro_batch: int = 2
    grad_accum: int = 8
    max_len: int = 4096
    modal_cap_usd: float = 60.0

    def adapter(self, k: int) -> str:
        return f"{self.served_base}-ei{k}"

    def selfplay_seed(self, k: int, regime: str) -> int:
        return 400 + 10 * k + 1 + list(self.selfplay_regimes).index(regime)       # 411, 412, 421, 422, 431, 432

    def eval_seed(self, trained: bool, regime: str) -> int:
        return (461 if trained else 451) + list(self.eval_regimes).index(regime)   # base 451..454, trained 461..464


CFG = EIConfig()


# ----- selection -----

def agent_net_points(run_dir: pathlib.Path) -> dict[tuple[int, str], int]:
    """Net points per agent over the session: the engine's `points` (market points plus fines and rewards)."""
    out: dict[tuple[int, str], int] = {}
    for r in read_jsonl(pathlib.Path(run_dir) / "periods.jsonl"):
        if r.get("header"):
            continue
        for agent, pts in zip(r["agents"], r["points"]):
            out[(r["pool"], agent)] = out.get((r["pool"], agent), 0) + int(pts)
    return out


def select_agents(scores: dict[tuple[int, str], int], top_share: float) -> set[tuple[int, str]]:
    """Top share of agents per pool session by net points; ties by agent id; at least one agent per pool."""
    by_pool: dict[int, list] = {}
    for (pool, agent), pts in scores.items():
        by_pool.setdefault(pool, []).append((-pts, agent))
    keep = set()
    for pool, lst in by_pool.items():
        lst.sort()
        n = max(1, math.ceil(top_share * len(lst)))
        keep |= {(pool, agent) for _, agent in lst[:n]}
    return keep


_PMIN = re.compile(r"State a price between (\d+) and (\d+)\. The lower of the two second statements")


def schema_for(row: dict) -> dict:
    """The JSON schema the engine sent with this decision, rebuilt from the logged step and user message (runs before
    the schema was logged); `prompts.question` is the one source of the schemas."""
    if row.get("schema"):
        return row["schema"]
    from .prompts import question

    step, user = row["step"], row["user"]
    m = re.search(r"Choose your price for this period \(integer between (\d+) and (\d+)\)", user) or \
        re.search(r"Answer with an integer between (\d+) and (\d+)", user)
    offset = int(m.group(1)) if m else 0
    ctx = {"period": row.get("period", 1), "firm_name": "x", "rival_name": "y", "partner_note": "", "history": "",
           "offset": offset, "discussion_note": "", "own_proposal": 0, "rival_proposal": 0, "own_price": 0, "rival_price": 0,
           "own_market": 0, "rival_market": 0}
    if step == "propose2":
        pm = _PMIN.search(user)
        if not pm:
            raise ValueError("propose2 call without its minimum")
        ctx["pmin"] = int(pm.group(1)) - offset
    if step == "price":
        ctx["can_report"] = "(field `report`)" in user
    return question(step, ctx)[1]


def request_user(row: dict) -> str:
    """The user message exactly as the OpenAI-compatible client sends it (schema appended, llm.OpenAICompatibleClient)."""
    return row["user"] + "\n\nJSON schema:\n" + json.dumps(schema_for(row))


def examples_from_run(run_dir: pathlib.Path, top_share: float) -> tuple[list[dict], dict]:
    run_dir = pathlib.Path(run_dir)
    systems = json.loads((run_dir / "prompts.json").read_text())["system_prompts"]
    keep = select_agents(agent_net_points(run_dir), top_share)
    calls = [r for r in read_jsonl(run_dir / "calls.jsonl") if not r.get("header")]
    n_valid = sum(1 for r in calls if not (r["defaulted"] or r["invalid_json"] or r["error"] or r["refusal"]))
    out = []
    for r in calls:
        if (r["pool"], r["agent"]) not in keep:
            continue
        if r["defaulted"] or r["invalid_json"] or r["error"] or r["refusal"] or not r.get("text"):
            continue
        out.append({"run_id": r["run_id"], "pool": r["pool"], "agent": r["agent"], "period": r["period"], "step": r["step"],
                    "messages": [{"role": "system", "content": systems[r["agent"]]},
                                 {"role": "user", "content": request_user(r)}],
                    "target": r["text"]})
    stats = {"run_dir": str(run_dir), "calls": len(calls), "json_validity": (n_valid / len(calls)) if calls else None,
             "agents_selected": len(keep), "examples": len(out)}
    return out, stats


def build_dataset(run_dirs: list[pathlib.Path], top_share: float, max_examples: int, seed: int) -> tuple[list[dict], list[dict]]:
    examples, stats = [], []
    for d in run_dirs:
        ex, st = examples_from_run(d, top_share)
        examples += ex
        stats.append(st)
    rng = random.Random(seed)
    rng.shuffle(examples)
    return examples[:max_examples], stats


# ----- training (torch, transformers, peft; imported here only) -----

def tokenize_example(tok, ex: dict, max_len: int) -> dict | None:
    """Input ids and labels; the prompt (system, user, assistant header) is masked with -100."""
    prompt = tok.apply_chat_template(ex["messages"], add_generation_prompt=True, tokenize=True)
    full = tok.apply_chat_template(ex["messages"] + [{"role": "assistant", "content": ex["target"]}], tokenize=True)
    if hasattr(prompt, "input_ids"):
        prompt, full = prompt["input_ids"], full["input_ids"]
    prompt, full = list(prompt), list(full)
    if full[:len(prompt)] != prompt:
        raise ValueError("chat template: the prompt is not a prefix of the full conversation")
    if len(full) > max_len:
        return None
    return {"input_ids": full, "labels": [-100] * len(prompt) + full[len(prompt):]}


def train_lora(examples: list[dict], model_path: str, out_dir: str, cfg: EIConfig = CFG, seed: int = 0,
               device: str | None = None, max_steps: int | None = None, tokenizer=None, model=None) -> dict:
    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.manual_seed(seed)
    random.seed(seed)
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    tok = tokenizer or AutoTokenizer.from_pretrained(model_path)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    base = model or AutoModelForCausalLM.from_pretrained(model_path, dtype=dtype)
    base.to(device)
    if device == "cuda":
        base.gradient_checkpointing_enable()
        base.enable_input_require_grads()
    lcfg = LoraConfig(r=cfg.lora_r, lora_alpha=cfg.lora_alpha, lora_dropout=cfg.lora_dropout,
                      target_modules=list(cfg.target_modules), task_type="CAUSAL_LM")
    net = get_peft_model(base, lcfg)
    data, dropped = [], 0
    for ex in examples:
        t = tokenize_example(tok, ex, cfg.max_len)
        if t is None:
            dropped += 1
        else:
            data.append(t)
    rng = random.Random(seed)
    steps_per_epoch = math.ceil(len(data) / (cfg.micro_batch * cfg.grad_accum))
    total = steps_per_epoch * cfg.epochs if max_steps is None else max_steps
    warm = max(1, int(cfg.warmup_share * total))
    opt = torch.optim.AdamW([p for p in net.parameters() if p.requires_grad], lr=cfg.lr, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / warm if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, total - warm))))
    net.train()
    log, step = [], 0
    pad = tok.pad_token_id
    for epoch in range(cfg.epochs):
        order = list(range(len(data)))
        rng.shuffle(order)
        batches = [order[i:i + cfg.micro_batch] for i in range(0, len(order), cfg.micro_batch)]
        for b0 in range(0, len(batches), cfg.grad_accum):
            group = batches[b0:b0 + cfg.grad_accum]
            n_tok = sum(sum(1 for x in data[i]["labels"] if x != -100) for mb in group for i in mb)
            loss_sum = 0.0
            for mb in group:
                L = max(len(data[i]["input_ids"]) for i in mb)
                ids = torch.full((len(mb), L), pad, dtype=torch.long)
                lab = torch.full((len(mb), L), -100, dtype=torch.long)
                att = torch.zeros((len(mb), L), dtype=torch.long)
                for j, i in enumerate(mb):
                    n = len(data[i]["input_ids"])
                    ids[j, :n] = torch.tensor(data[i]["input_ids"])
                    lab[j, :n] = torch.tensor(data[i]["labels"])
                    att[j, :n] = 1
                ids, lab, att = ids.to(device), lab.to(device), att.to(device)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=(device == "cuda")):
                    logits = net(input_ids=ids, attention_mask=att).logits
                # token-level mean over the whole accumulation group
                loss = torch.nn.functional.cross_entropy(logits[:, :-1].reshape(-1, logits.size(-1)).float(),
                                                         lab[:, 1:].reshape(-1), ignore_index=-100, reduction="sum") / max(1, n_tok)
                loss.backward()
                loss_sum += float(loss.detach())
            torch.nn.utils.clip_grad_norm_([p for p in net.parameters() if p.requires_grad], 1.0)
            opt.step()
            sched.step()
            opt.zero_grad(set_to_none=True)
            step += 1
            log.append({"step": step, "loss": loss_sum, "lr": sched.get_last_lr()[0], "answer_tokens": n_tok})
            if step >= total:
                break
        if step >= total:
            break
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    net.save_pretrained(str(out))
    stats = {"examples": len(examples), "used": len(data), "dropped_too_long": dropped, "steps": step,
             "first_loss": log[0]["loss"] if log else None, "last_loss": log[-1]["loss"] if log else None,
             "config": asdict(cfg), "seed": seed, "device": device}
    (out / "train_log.jsonl").write_text("".join(json.dumps(x) + "\n" for x in log))
    write_json(out / "train_stats.json", stats)
    return stats


# ----- the registered loop -----

def selfplay_command(cfg: EIConfig, k: int, regime: str, base_url: str = "$EI_URL/v1") -> str:
    model = cfg.served_base if k == 1 else cfg.adapter(k - 1)
    return (f"python3 -m cartelbench.run --provider openai --base-url {base_url} --api-key-env P2_KEY --model {model} "
            f"--regime {regime} --duopoles {cfg.selfplay_duopoles} --pools {cfg.selfplay_pools} "
            f"--seed {cfg.selfplay_seed(k, regime)} --out-dir evidence/stage2/runs")


def eval_command(cfg: EIConfig, trained: bool, regime: str, base_url: str = "$EI_URL/v1") -> str:
    model = cfg.adapter(cfg.iterations) if trained else cfg.served_base
    return (f"python3 -m cartelbench.run --provider openai --base-url {base_url} --api-key-env P2_KEY --model {model} "
            f"--regime {regime} --duopoles {cfg.eval_duopoles} --pools {cfg.eval_pools} "
            f"--seed {cfg.eval_seed(trained, regime)} --out-dir evidence/stage2/runs")


def plan(cfg: EIConfig = CFG) -> list[str]:
    cmds = ["EI_ADAPTERS= modal deploy scripts/modal_ei.py   # base model, LoRA enabled"]
    for k in range(1, cfg.iterations + 1):
        cmds += [selfplay_command(cfg, k, r) for r in cfg.selfplay_regimes]
        cmds += [f"python3 -m cartelbench.expert_iteration select --iteration {k}",
                 f"modal volume put cartelbench-ei evidence/stage2/data/ei{k}.jsonl /data/ei{k}.jsonl",
                 f"modal run scripts/modal_ei.py::train --iteration {k}",
                 f"modal volume get cartelbench-ei /adapters/ei{k} evidence/stage2/adapters/ei{k}",
                 f"EI_ADAPTERS={','.join(f'ei{j}' for j in range(1, k + 1))} modal deploy scripts/modal_ei.py"]
    cmds += [eval_command(cfg, t, r) for t in (False, True) for r in cfg.eval_regimes]
    cmds += ["python3 -m cartelbench.expert_iteration evaluate", "modal app stop -y cartelbench-ei"]
    return cmds


def _find(model: str, regime: str, seed: int) -> pathlib.Path:
    from .pools import find_run

    return find_run(model, regime, seed, RUNS)


def cmd_select(args) -> int:
    cfg = CFG
    k = args.iteration
    dirs = [_find(cfg.served_base if j == 1 else cfg.adapter(j - 1), r, cfg.selfplay_seed(j, r))
            for j in range(1, k + 1) for r in cfg.selfplay_regimes]
    examples, stats = build_dataset(dirs, cfg.top_share, cfg.max_examples, seed=k)
    cur = [s for s in stats if any(f"_s{cfg.selfplay_seed(k, r)}" in s["run_dir"] for r in cfg.selfplay_regimes)]
    validity = min(s["json_validity"] for s in cur)
    stop = []
    if validity < cfg.min_json_validity:
        stop.append(f"JSON validity {validity:.3f} below {cfg.min_json_validity} in iteration {k}")
    if len(examples) < cfg.min_examples:
        stop.append(f"{len(examples)} examples, fewer than {cfg.min_examples}")
    data = OUT / "data" / f"ei{k}.jsonl"
    data.parent.mkdir(parents=True, exist_ok=True)
    data.write_text("".join(json.dumps(x) + "\n" for x in examples))
    write_json(OUT / "data" / f"ei{k}_stats.json", {**evidence_header(f"python3 -m cartelbench.expert_iteration select --iteration {k}"),
                                                     "iteration": k, "runs": stats, "examples": len(examples), "stop": stop})
    print(json.dumps({"iteration": k, "examples": len(examples), "stop": stop}))
    return 1 if stop else 0


def cmd_train(args) -> int:
    examples = [json.loads(x) for x in pathlib.Path(args.data).read_text().splitlines() if x.strip()]
    print(json.dumps(train_lora(examples, args.model, args.out, seed=args.seed, max_steps=args.max_steps)))
    return 0


def cmd_evaluate(args) -> int:
    from .pools import cluster_parts, merge_runs, permutation_test
    from .round6 import KEYS
    from .scorecard import diff_ci, evaluate

    cfg = CFG
    header = evidence_header("python3 -m cartelbench.expert_iteration evaluate")
    base = {r: merge_runs([_find(cfg.served_base, r, cfg.eval_seed(False, r))]) for r in cfg.eval_regimes}
    trained = {r: merge_runs([_find(cfg.adapter(cfg.iterations), r, cfg.eval_seed(True, r))]) for r in cfg.eval_regimes}
    res = {**header, "comparisons": {}, "scorecards": {}}
    for r in cfg.eval_regimes:
        res["comparisons"][r] = {k: {"trained": trained[r]["metrics"].get(k), "base": base[r]["metrics"].get(k),
                                     "diff": diff_ci(trained[r], base[r], k, args.n_boot),
                                     "permutation": permutation_test(cluster_parts(trained[r]["rows"], k),
                                                                     cluster_parts(base[r]["rows"], k), "two-sided")}
                                 for k in KEYS}
    for name, runs in (("base", base), ("trained", trained)):
        rows = [x for x in evaluate(runs, args.n_boot) if x["n"] <= 6]
        res["scorecards"][name] = [{"n": x["n"], "result": x["result"], "replicated": x["replicated"]} for x in rows]
    write_json(OUT / "evaluate.json", res)
    print(json.dumps(res["scorecards"], indent=1))
    return 0


def tiny_test(workdir: pathlib.Path) -> dict:
    """The whole pipeline on the CPU: a fake seller plays fine and leniency, the top agents are selected, a tiny randomly
    initialised Llama with a locally trained tokenizer and the Llama-3 chat template is LoRA-trained for a few steps."""
    from tokenizers import Tokenizer, models, pre_tokenizers, trainers
    from transformers import LlamaConfig, LlamaForCausalLM, PreTrainedTokenizerFast

    from .engine import RunConfig, run_sync
    from .llm import FakeClient

    rng = random.Random(0)

    def script(user, schema):
        p = schema["properties"]
        if "talk" in p:
            return {"talk": rng.random() < 0.5, "reason": "x"}
        if "proposal" in p:
            return {"proposal": max(p["proposal"].get("minimum", 0), 9), "reason": "x"}
        if "price" in p:
            out = {"price": rng.choice([3, 7, 9]), "reason": "x"}
            if "report" in p:
                out["report"] = rng.random() < 0.3
            return out
        return {"report": rng.random() < 0.3, "reason": "x"}

    dirs = []
    for reg, seed in (("fine", 1), ("leniency", 2)):
        cfg = RunConfig(regime=reg, model="fake-ei", provider="fake", player="llm", duopoles=4, pools=2, seed=seed,
                        out_dir=str(workdir / "runs"), max_periods=6)
        s = run_sync(cfg, FakeClient(script))
        dirs.append(workdir / "runs" / s["run_id"])
    examples, stats = build_dataset(dirs, CFG.top_share, 64, seed=1)
    texts = [m["content"] for ex in examples for m in ex["messages"]] + [ex["target"] for ex in examples]
    tk = Tokenizer(models.BPE(unk_token="<unk>"))
    tk.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    specials = ["<unk>", "<|begin_of_text|>", "<|start_header_id|>", "<|end_header_id|>", "<|eot_id|>"]
    tk.train_from_iterator(texts, trainers.BpeTrainer(vocab_size=600, special_tokens=specials,
                                                      initial_alphabet=pre_tokenizers.ByteLevel.alphabet()))
    tok = PreTrainedTokenizerFast(tokenizer_object=tk, bos_token="<|begin_of_text|>", eos_token="<|eot_id|>", unk_token="<unk>")
    tok.chat_template = ("{{ bos_token }}{% for m in messages %}<|start_header_id|>{{ m['role'] }}<|end_header_id|>\n\n"
                         "{{ m['content'] }}<|eot_id|>{% endfor %}{% if add_generation_prompt %}"
                         "<|start_header_id|>assistant<|end_header_id|>\n\n{% endif %}")
    model = LlamaForCausalLM(LlamaConfig(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=2,
                                         num_attention_heads=2, num_key_value_heads=2, max_position_embeddings=8192))
    small = EIConfig(max_len=8192, micro_batch=2, grad_accum=2, lr=5e-3)
    stats_train = train_lora(examples, "", str(workdir / "adapter"), cfg=small, seed=0, device="cpu", max_steps=6,
                             tokenizer=tok, model=model)
    return {"selection": stats, "examples": len(examples), "train": stats_train,
            "first_example": {"step": examples[0]["step"], "target": examples[0]["target"][:80]}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    s = sub.add_parser("select")
    s.add_argument("--iteration", type=int, required=True)
    t = sub.add_parser("train")
    t.add_argument("--data", required=True)
    t.add_argument("--model", required=True)
    t.add_argument("--out", required=True)
    t.add_argument("--seed", type=int, default=0)
    t.add_argument("--max-steps", type=int, default=None)
    e = sub.add_parser("evaluate")
    e.add_argument("--n-boot", type=int, default=1000)
    tt = sub.add_parser("tiny-test")
    tt.add_argument("--workdir", default=str(OUT / "tiny_test"))
    args = ap.parse_args(argv)
    if args.cmd == "plan":
        print("\n".join(plan()))
        return 0
    if args.cmd == "tiny-test":
        res = tiny_test(pathlib.Path(args.workdir))
        write_json(OUT / "tiny_test.json", {**evidence_header("python3 -m cartelbench.expert_iteration tiny-test"), **res})
        print(json.dumps({k: res[k] for k in ("examples", "first_example")}), json.dumps(res["train"]["first_loss"]),
              json.dumps(res["train"]["last_loss"]))
        return 0
    return {"select": cmd_select, "train": cmd_train, "evaluate": cmd_evaluate}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
