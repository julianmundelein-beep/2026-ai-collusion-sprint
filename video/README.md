# CartelBench video

Explainer video for the AI Collusion Research Sprint submission: 1920x1080, 30 fps, H.264, English, about 4:49 without voice, text cards readable without sound. Output: `video/out/CartelBench_AI-Collusion-Research-Sprint_2026.mp4`.

Everything on screen is generated from the repository: `build.py` draws every frame with Pillow, reads the numbers from `cartelbench/evidence/` (round4 and provider2 scorecards, `round7/diagonal.json`, `round4/screen.json`, `round4/scorecards.json`, `risk_cards/risk_cards.json`) and `cartelbench/data/human_baseline.json`, and encodes with the ffmpeg binary of the PyPI package `imageio-ffmpeg`. `facts_used.md` lists every number with its place in `paper/report.md` and its measurement key.

## Rebuild

```sh
pip install pillow imageio-ffmpeg
python3 video/build.py                # full render, about 10 minutes
python3 video/build.py --timeline     # scene start and end times only
python3 video/build.py --stills-only  # the three PNGs in video/stills/
```

The script uses the Inter font if it finds it (`/usr/share/fonts/opentype/inter`, `~/Library/Fonts`, or the folder in `VIDEO_FONT_DIR`), otherwise DejaVu Sans. Each scene lasts at least 3 s plus 0.35 s per prose word on the card and 3 s after its last element appears.

## Check the result

```sh
ffprobe -v error -show_entries format=duration,size -of default=nw=1 video/out/CartelBench_AI-Collusion-Research-Sprint_2026.mp4
```

## Voice

`narration.md` holds the spoken text per scene with the moments at which the elements appear. Generate or record one file per scene and save them as `video/voice/01.mp3` to `video/voice/13.mp3` (MP3, M4A or WAV all work; the extension in the file name must be `.mp3`, or rename after export). Then rebuild:

```sh
python3 video/build.py
```

With the files present, every scene is at least its voice file plus 1.2 s long, the files start at the scene starts, and the audio track is mixed into the MP4 (AAC 160 kbit/s). Missing files fall back to the silent timing; `--no-voice` ignores the folder. To replace one scene, overwrite its file and rebuild.

Suggested ElevenLabs settings: model Eleven Multilingual v2 (or v3), a calm neutral English narrator, stability 0.55 to 0.65, similarity 0.75, style 0, speed 0.95 to 1.0, MP3 44.1 kHz 128 kbps; paste one scene block at a time; pronunciation hints are at the top of `narration.md`.

To lay a single recorded track `voice.m4a` under the silent video by hand instead:

```sh
ffmpeg -y -i video/out/CartelBench_AI-Collusion-Research-Sprint_2026.mp4 -i voice.m4a \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -shortest \
  video/out/CartelBench_AI-Collusion-Research-Sprint_2026_voice.mp4
```

Shift a late or early recording with `-itsoffset <seconds>` before the second `-i`; drop `-shortest` to keep the full video length. The bundled ffmpeg works too: `python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` prints its path.
