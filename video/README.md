# The Body, Not the Empire — animated counter-argument

A 63-second, 9:16 motion-graphics video that counters the "America bankrolls the entire
planet while its own people struggle" claim using an organism metaphor: nations are organs,
America is the heart, and foreign engagement is **circulation**, not a hemorrhage.

The argument runs as on-screen subtitles, scored with a synthesized heartbeat + ambient bed
that slows and flatlines when the "selfish liver" hoards, then restarts.

## Files
- `scene.html` — the whole animation. A single `<canvas>` driven by a deterministic
  `window.seekTo(t)` function (no real-time animation, so every frame is reproducible).
- `render.js` — Playwright script: loads `scene.html`, seeks frame-by-frame at 30fps,
  screenshots each frame to PNG.
- `audio.py` — synthesizes the heartbeat + drone bed (`bed.wav`), synced to the same
  heart-rate timeline the visuals use.
- `encode.sh` — muxes frames + audio into `the-body-not-the-empire.mp4` (H.264 / AAC).
- `voiceover-script.md` — narration timed to the cut, if you want to record a real voice.

## Rebuild
```bash
FRAMES_DIR=/tmp/frames node render.js          # render ~1890 PNG frames
python3 audio.py /tmp/bed.wav                   # synthesize the audio bed
FRAMES_DIR=/tmp/frames AUDIO_FILE=/tmp/bed.wav \
  OUT_FILE=the-body-not-the-empire.mp4 bash encode.sh
```

## The argument, scene by scene
1. **The claim** — his framing on screen: bleeding empire, $50B, 177 countries.
2. **The heart** — an empire is a body; the center feeds the limbs out of self-interest.
3. **The selfish liver** — an organ that hoards everything kills the body, and itself.
4. **Hemorrhage vs. circulation** — money that leaves *and returns* is not a wound.
5. **The credit card** — his strongest line is downstream of the system he mocks.
6. **Proportion** — $50B is ≈0.7% of federal spending; a drop, not a gush.
7. **The honest close** — regulate the flow, don't stop the heart. Circulation isn't charity.
