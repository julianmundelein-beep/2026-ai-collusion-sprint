"""Stage 2 of round 6 on Modal: vLLM with LoRA adapters (self-play and evaluation) and LoRA training (expert iteration).

    EI_ADAPTERS= modal deploy scripts/modal_ei.py                    # base model, LoRA enabled, OpenAI-compatible endpoint
    modal volume put cartelbench-ei evidence/stage2/data/ei1.jsonl /data/ei1.jsonl
    modal run scripts/modal_ei.py::train --iteration 1                # adapter /adapters/ei1 in the volume
    EI_ADAPTERS=ei1 modal deploy scripts/modal_ei.py                 # base model and adapter ei1 (served as <base>-ei1)
    modal app stop -y cartelbench-ei                                  # endpoint down after the runs

The base model, revision, vLLM version, dtype and sampling defaults are those of PREREGISTRATION_provider2.md and
scripts/modal_vllm.py (weights from the volume `cartelbench-hf-cache`, already downloaded there). Training follows
`cartelbench.expert_iteration.train_lora` with the hyperparameters of `EIConfig` (amendment 8). The bearer token lives
in the Modal secret `cartelbench-vllm` (key VLLM_API_KEY) and locally in P2_KEY; it is never written to the repository.
Cost guards: one container per function, scale to zero after 5 idle minutes, a timeout on every function.
"""
from __future__ import annotations

import os
import pathlib
import subprocess

import modal

BASE_REPO = "unsloth/Meta-Llama-3.1-8B-Instruct"
BASE_REVISION = "a2856192dd7c25b842431f39c179a6c2c2f627d1"
SERVED = "llama-3.1-8b-instruct"
VLLM_VERSION = "0.31.0"
MAX_MODEL_LEN = 8192
PORT = 8000
SERVE_GPU = os.environ.get("EI_SERVE_GPU", "L40S")
TRAIN_GPU = os.environ.get("EI_TRAIN_GPU", "A100-80GB")
ADAPTERS = [a for a in os.environ.get("EI_ADAPTERS", "").split(",") if a]

hf_cache = modal.Volume.from_name("cartelbench-hf-cache", create_if_missing=True)
vllm_cache = modal.Volume.from_name("cartelbench-vllm-cache", create_if_missing=True)
ei_vol = modal.Volume.from_name("cartelbench-ei", create_if_missing=True)
VOLUMES = {"/root/.cache/huggingface": hf_cache, "/root/.cache/vllm": vllm_cache, "/ei": ei_vol}

serve_image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install(f"vllm=={VLLM_VERSION}", "huggingface_hub[hf_transfer]")
    .env({"HF_HOME": "/root/.cache/huggingface", "VLLM_USE_FLASHINFER_SAMPLER": "0", "EI_ADAPTERS": ",".join(ADAPTERS),
          "HF_HUB_OFFLINE": "1"})
)
train_image = (
    modal.Image.debian_slim(python_version="3.12")
    # the versions the CPU test of tests/test_stage2.py ran with
    .uv_pip_install("torch==2.14.1", "transformers==5.20.2", "peft==0.21.2", "accelerate==1.15.0", "huggingface_hub==2.3.0")
    .env({"HF_HOME": "/root/.cache/huggingface", "HF_HUB_OFFLINE": "1"})
    .add_local_python_source("cartelbench")
)

app = modal.App("cartelbench-ei")


@app.function(image=train_image, gpu=TRAIN_GPU, volumes=VOLUMES, timeout=6 * 60 * 60, max_containers=1)
def train(iteration: int) -> dict:
    """LoRA on the base weights from /ei/data/ei<k>.jsonl; adapter and logs to /ei/adapters/ei<k>."""
    import json

    from huggingface_hub import snapshot_download

    from cartelbench.expert_iteration import CFG, train_lora

    path = snapshot_download(BASE_REPO, revision=BASE_REVISION, local_files_only=True)
    data = pathlib.Path(f"/ei/data/ei{iteration}.jsonl")
    examples = [json.loads(x) for x in data.read_text().splitlines() if x.strip()]
    stats = train_lora(examples, path, f"/ei/adapters/ei{iteration}", cfg=CFG, seed=iteration, device="cuda")
    ei_vol.commit()
    return stats


def serve() -> None:
    from huggingface_hub import snapshot_download

    path = snapshot_download(BASE_REPO, revision=BASE_REVISION, local_files_only=True)
    cmd = [
        "vllm", "serve", path,
        "--served-model-name", SERVED,
        "--host", "0.0.0.0", "--port", str(PORT),
        "--api-key", os.environ["VLLM_API_KEY"],
        "--dtype", "bfloat16",
        "--max-model-len", str(MAX_MODEL_LEN),
        "--enable-prefix-caching",
        "--gpu-memory-utilization", "0.92",
        "--generation-config", "vllm",
        "--enable-lora", "--max-lora-rank", "16", "--max-loras", "4",
    ]
    adapters = [a for a in os.environ.get("EI_ADAPTERS", "").split(",") if a]
    if adapters:
        cmd += ["--lora-modules", *[f"{SERVED}-{a}=/ei/adapters/{a}" for a in adapters]]
    subprocess.Popen(cmd)


serve = app.function(
    image=serve_image,
    gpu=SERVE_GPU,
    volumes=VOLUMES,
    secrets=[modal.Secret.from_name("cartelbench-vllm")],
    max_containers=1,
    scaledown_window=5 * 60,
    timeout=12 * 60 * 60,
)(modal.concurrent(max_inputs=128)(modal.web_server(port=PORT, startup_timeout=30 * 60)(serve)))
