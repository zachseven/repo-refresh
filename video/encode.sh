#!/usr/bin/env bash
# Encode rendered PNG frames + audio bed into a shareable MP4 (H.264 / AAC, 9:16).
set -euo pipefail

FFMPEG=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
FRAMES="${FRAMES_DIR:?set FRAMES_DIR}"
AUDIO="${AUDIO_FILE:?set AUDIO_FILE}"
OUT="${OUT_FILE:-the-body-not-the-empire.mp4}"

"$FFMPEG" -y \
  -framerate 30 -i "$FRAMES/%05d.png" \
  -i "$AUDIO" \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 192k \
  -shortest -movflags +faststart \
  "$OUT"

echo "wrote $OUT"
