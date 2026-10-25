# CartelBench video

Explainer video for the AI Collusion Research Sprint submission: 1920x1080, 30 fps, about 3:34, English, no voice, text cards readable without sound. Output: `video/out/CartelBench_AI-Collusion-Research-Sprint_2026.mp4`.

Everything on screen is generated from the repository: `build.py` draws every frame with Pillow, reads the numbers from `cartelbench/evidence/` and `cartelbench/data/human_baseline.json`, shows `paper/figures/figure1_landscape.png` as the scorecard, and encodes with the ffmpeg binary shipped by the PyPI package `imageio-ffmpeg`. `facts_used.md` lists every number with its id in `hackathon/FACTS.md`.

## Rebuild

```sh
pip install pillow imageio-ffmpeg
python3 video/build.py              # full render, about 5 minutes on a laptop
python3 video/build.py --timeline   # scene start and end times only
python3 video/build.py --stills-only  # the three PNGs in video/stills/
```

The script uses the Inter font if it finds it (`/usr/share/fonts/opentype/inter`, `~/Library/Fonts`, or the folder in `VIDEO_FONT_DIR`), otherwise DejaVu Sans. Scene durations are checked against a reading rule of 3 s plus 0.35 s per word.

## Check the result

```sh
ffprobe -v error -show_entries format=duration,size -of default=nw=1 video/out/CartelBench_AI-Collusion-Research-Sprint_2026.mp4
```

## Optional voice track

`narration.md` holds a spoken text per scene with start and end times. Record it as `voice.m4a` (any sample rate; AAC or anything ffmpeg reads), then lay it under the video:

```sh
ffmpeg -y -i video/out/CartelBench_AI-Collusion-Research-Sprint_2026.mp4 -i voice.m4a \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -shortest \
  video/out/CartelBench_AI-Collusion-Research-Sprint_2026_voice.mp4
```

If the recording starts late or early, shift it with `-itsoffset` before the second `-i` (positive delays the voice): `ffmpeg -y -i <video> -itsoffset 0.5 -i voice.m4a ...`. To keep the full video length when the voice is shorter, drop `-shortest`.

The ffmpeg from the PyPI package works too: `python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` prints its path.
