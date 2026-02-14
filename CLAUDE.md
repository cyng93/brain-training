# CLAUDE.md — brain-training

## Project Overview

Single-page HTML course transcript site for **科學的大腦鍛鍊法** (Scientific Brain Training)
by 池田義博 (Ikeda Yoshihiro). Deployed via GitHub Pages.

- **Live site:** https://cyng93.github.io/brain-training/
- **Course:** 18 lessons across 8 chapters (~3.5 hrs total)
- **Source:** PressPlay (private), YouTube backup (public)

## Directory Layout

```
brain-training/
├── .nojekyll                          # Bypass Jekyll processing for GitHub Pages
├── .gitignore                         # Ignores src/inputs/ and src/subtitle_frames_for_ocr/
├── CLAUDE.md                          # This file
├── index.html                         # Symlink → 科學的大腦鍛鍊法_transcript.html
├── 科學的大腦鍛鍊法_transcript.html     # Main HTML (single-file, self-contained)
└── src/
    ├── inputs/                        # (gitignored) Course MP4 files from PressPlay
    ├── tools/
    │   ├── extract_all.sh             # STEP 1: ffmpeg frame extraction + grid composites
    │   ├── make_grids.sh              # Helper: create 10-frame grid composites
    │   ├── parse_srt.py               # STEP 3: SRT → JSON
    │   └── generate_pages.py          # STEP 4: JSON → HTML
    ├── subtitle_frames_for_ocr/       # (gitignored) ~15K intermediate frame images
    ├── subtitles/
    │   ├── *_zh-TW_visual.srt         # 18 files — curated OCR output (primary source)
    │   └── *_jp_youtube_autogen.srt   # 18 files — YouTube auto-generated Japanese (reference)
    └── transcripts.json               # 192K — structured JSON of all 18 lesson transcripts
```

## Build Pipeline

```
Prerequisites:
  - Course MP4 video files (18 files, from PressPlay)
  - brew install ffmpeg tesseract
  - brew install yt-dlp (optional, for downloading YouTube auto-generated subtitles)

┌─────────────────────────────────────────────────────────────┐
│ STEP 0 (optional, one-time, independent)                   │
│                                                            │
│   yt-dlp --write-auto-sub --sub-lang ja ...               │
│     └─► src/subtitles/*_jp_youtube_autogen.srt (reference) │
│                                                            │
│   Only needed if you want Japanese auto-generated subs     │
│   from YouTube as reference. Not part of the main pipeline.│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Extract subtitle frames                            │
│                                                            │
│   src/tools/extract_all.sh                                 │
│     Input:  src/inputs/*.mp4 (18 course videos)            │
│     Output: src/subtitle_frames_for_ocr/                   │
│             ├── {id}_{nnnn}.jpg  (per-second frames)       │
│             └── {id}_grid_{nn}.jpg (10-frame composites)   │
│                                                            │
│   Calls: src/tools/make_grids.sh (for grid composites)     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: OCR → SRT (manual, via Claude/Cydia)              │
│                                                            │
│   Feed grid images to Claude for OCR + deduplication       │
│     Input:  src/subtitle_frames_for_ocr/{id}_grid_*.jpg    │
│     Output: src/subtitles/*_zh-TW_visual.srt               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: SRT → JSON                                         │
│                                                            │
│   python3 src/tools/parse_srt.py                           │
│     Input:  src/subtitles/*_zh-TW_visual.srt (18 files)    │
│     Output: src/transcripts.json                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: JSON → HTML                                        │
│                                                            │
│   python3 src/tools/generate_pages.py                      │
│     Input:  src/transcripts.json                           │
│     Output: 科學的大腦鍛鍊法_transcript.html (repo root)    │
│             (index.html symlinks to this)                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Deploy                                             │
│                                                            │
│   git push → GitHub Pages auto-deploys from main branch    │
│     Live at: https://cyng93.github.io/brain-training/      │
└─────────────────────────────────────────────────────────────┘
```

## HTML Features

1. Full 18-lesson transcript with YouTube click-to-load embedding
2. Real-time search across all transcripts with highlight
3. Dark mode toggle
4. Font size controls (A-/A+) with presets (XS/S/M/L/XL)
5. Eye-care mode (auto-dark + larger text, with proper state revert)
6. Expand all / Collapse all transcript sections
7. Scrollable transcript while video plays (auto-expand + 60vh scroll)
8. Floating TOC sidebar with chapter grouping + IntersectionObserver active tracking

## Subtitle File Naming Convention

- `{id}_{title}_zh-TW_visual.srt` — OCR-extracted zh-TW subtitles (primary, curated)
- `{id}_{title}_jp_youtube_autogen.srt` — YouTube auto-generated Japanese (reference only)

Where `{id}` is the lesson number (e.g., `1-1`, `7-3`) and `{title}` is the
canonical lesson title from the course curriculum.

## GitHub Pages

- Deployed from `main` branch
- `.nojekyll` file present to bypass Jekyll processing
- `index.html` is a symlink to `科學的大腦鍛鍊法_transcript.html`
