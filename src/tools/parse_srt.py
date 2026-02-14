#!/usr/bin/env python3
"""Parse all 18 SRT files and output structured JSON for HTML/Markdown generation."""

import json
import re
import sys
from pathlib import Path

# Video metadata in order
VIDEOS = [
    ("1-1", "六屆記憶力冠軍的秘密"),
    ("1-2", "「腦」的成長並不分年齡與天賦"),
    ("2-1", "正念與意識控制"),
    ("2-2", "記憶的原理"),
    ("2-3", "記憶策略"),
    ("3-1", "禪｜焦點集中練習"),
    ("3-2", "影像串流"),
    ("4-1", "三循環速習法"),
    ("4-2", "三循環速習法的具體方法"),
    ("5-1", "一分鐘寫作"),
    ("5-2", "一分鐘寫作的具體方法"),
    ("6-1", "框架式閱讀法"),
    ("6-2", "PITA筆記法"),
    ("7-1", "A4一張記憶法"),
    ("7-2", "圖像創作法｜讓資訊產生互動"),
    ("7-3", "圖像創作法｜讓資訊產生互動-2"),
    ("8-1", "目標達成的策略-1"),
    ("8-2", "目標達成的策略-2"),
]


def parse_srt(filepath: Path) -> list[str]:
    """Parse SRT file and return list of subtitle text lines (no timestamps/numbers)."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    texts = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Skip sequence number (digit-only lines)
        if re.match(r"^\d+$", line):
            i += 1
            # Skip timestamp line
            if i < len(lines) and "-->" in lines[i]:
                i += 1
            # Read subtitle text (could be multi-line)
            while i < len(lines) and lines[i].strip():
                texts.append(lines[i].strip())
                i += 1
        i += 1

    return texts


def deduplicate(texts: list[str]) -> list[str]:
    """Deduplicate consecutive identical lines and return as list."""
    if not texts:
        return []

    deduped = [texts[0]]
    for t in texts[1:]:
        if t != deduped[-1]:
            deduped.append(t)

    return deduped


def main():
    base_dir = Path(__file__).parent
    results = []

    for video_id, title in VIDEOS:
        srt_file = base_dir / f"{video_id}_{title}_zh-TW_visual.srt"
        if not srt_file.exists():
            print(f"WARNING: {srt_file.name} not found!", file=sys.stderr)
            continue

        texts = parse_srt(srt_file)
        lines = deduplicate(texts)
        entry_count = len(texts)

        results.append({
            "id": video_id,
            "title": title,
            "full_title": f"{video_id} {title}",
            "entry_count": entry_count,
            "lines": lines,
        })
        print(f"  Parsed {srt_file.name}: {entry_count} entries, {len(lines)} lines", file=sys.stderr)

    # Output JSON
    output = {
        "course_title": "科學的大腦鍛鍊法",
        "author": "池田義博",
        "total_videos": len(results),
        "videos": results,
    }

    json_path = base_dir / "transcripts.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {json_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
