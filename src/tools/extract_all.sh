#!/bin/bash
# Extract subtitle frames (1fps) and create grid composites for ALL 18 videos
# Uses dynamic crop based on actual video dimensions via ffmpeg expressions

VIDDIR="/Users/ching_yi_ng.2026/Downloads/#科學的大腦鍛鍊法"
FDIR="/Users/ching_yi_ng_groupDir/ghq/github.com/ching-yi-ng_tmemu/basb/3.resource/科學的大腦鍛鍊法-subtitles/frames_visual"
GRIDSCRIPT="/Users/ching_yi_ng_groupDir/ghq/github.com/ching-yi-ng_tmemu/basb/3.resource/科學的大腦鍛鍊法-subtitles/make_grids.sh"

mkdir -p "$FDIR"

process_video() {
  local PREFIX="$1"
  local FILENAME="$2"

  # Check if frames already exist
  local EXISTING
  EXISTING=$(ls "$FDIR"/${PREFIX}_[0-9][0-9][0-9].jpg "$FDIR"/${PREFIX}_[0-9][0-9][0-9][0-9].jpg 2>/dev/null | wc -l | tr -d ' ')
  if [ "$EXISTING" -gt 0 ]; then
    echo "[$PREFIX] $EXISTING frames already exist, skipping extraction."
  else
    echo "[$PREFIX] Extracting frames from: $FILENAME ..."
    # Use dynamic crop: crop bottom 120px of whatever the video size is
    # crop=iw:120:0:ih-120 crops full width, 120px tall, starting at (height-120)
    # Then scale to 2560 wide (2x) for readability
    ffmpeg -y -i "$VIDDIR/$FILENAME" \
      -vf "fps=1,crop=iw:120:0:ih-120,scale=2560:240" \
      -q:v 2 "$FDIR/${PREFIX}_%04d.jpg" 2>/dev/null
    EXISTING=$(ls "$FDIR"/${PREFIX}_[0-9][0-9][0-9][0-9].jpg 2>/dev/null | wc -l | tr -d ' ')
    echo "[$PREFIX] Extracted $EXISTING frames."
  fi

  # Check if grids already exist
  local GRID_EXISTING
  GRID_EXISTING=$(ls "$FDIR"/${PREFIX}_grid_[0-9][0-9].jpg "$FDIR"/${PREFIX}_grid_[0-9][0-9][0-9].jpg 2>/dev/null | wc -l | tr -d ' ')
  if [ "$GRID_EXISTING" -gt 0 ]; then
    echo "[$PREFIX] $GRID_EXISTING grids already exist, skipping grid creation."
  else
    echo "[$PREFIX] Creating grids ($EXISTING frames)..."
    bash "$GRIDSCRIPT" "$PREFIX" "$EXISTING"
    GRID_EXISTING=$(ls "$FDIR"/${PREFIX}_grid_[0-9][0-9].jpg "$FDIR"/${PREFIX}_grid_[0-9][0-9][0-9].jpg 2>/dev/null | wc -l | tr -d ' ')
    echo "[$PREFIX] Created $GRID_EXISTING grids."
  fi

  echo "[$PREFIX] DONE. Frames=$EXISTING, Grids=$GRID_EXISTING"
  echo "---"
}

# Process each video explicitly
process_video "1-1" "1-1.六屆記憶力冠軍的秘密.mp4"
process_video "1-2" "1-2.「腦」的成長並不分年齡與天賦.mp4"
process_video "2-1" "2-1.正念與意識控制.mp4"
process_video "2-2" "2-2.大腦的記憶機制.mp4"
process_video "2-3" "2-3.認知心理學的記憶策略.mp4"
process_video "3-1" "3-1.禪｜焦點集中練習.mp4"
process_video "3-2" "3-2.專注的想像.mp4"
process_video "4-1" "4-1.三循環的操作練習.mp4"
process_video "4-2" "4-2.分解步驟：三循環學習法的操作練習.mp4"
process_video "5-1" "5-1.為什麼要練習一分鐘寫作.mp4"
process_video "5-2" "5-2.如何進行一分鐘寫作.mp4"
process_video "6-1" "6-1.準備你的大腦｜快速閱讀法.mp4"
process_video "6-2" "6-2.強化結構｜筆記結構練習.mp4"
process_video "7-1" "7-1.強化記憶的連結.mp4"
process_video "7-2" "7-2.圖像創作法｜讓資訊產生互動.mp4"
process_video "7-3" "7-3.圖像創作法｜讓資訊產生互動.mp4"
process_video "8-1" "8-1.目標達成的策略-1.mp4"
process_video "8-2" "8-2.目標達成的策略-2.mp4"

echo ""
echo "========================================="
echo "ALL 18 VIDEOS PROCESSED"
echo "========================================="
echo ""
echo "Summary:"
for PREFIX in 1-1 1-2 2-1 2-2 2-3 3-1 3-2 4-1 4-2 5-1 5-2 6-1 6-2 7-1 7-2 7-3 8-1 8-2; do
  FRAMES=$(ls "$FDIR"/${PREFIX}_[0-9][0-9][0-9].jpg "$FDIR"/${PREFIX}_[0-9][0-9][0-9][0-9].jpg 2>/dev/null | wc -l | tr -d ' ')
  GRIDS=$(ls "$FDIR"/${PREFIX}_grid_[0-9][0-9].jpg "$FDIR"/${PREFIX}_grid_[0-9][0-9][0-9].jpg 2>/dev/null | wc -l | tr -d ' ')
  echo "  $PREFIX: $FRAMES frames, $GRIDS grids"
done
