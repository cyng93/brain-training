#!/usr/bin/env python3
"""Generate HTML and Markdown one-pager from transcripts.json."""

import json
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEPLOY_DIR = Path.home().parent / "ching_yi_ng_groupDir/ghq/github.com/cyng93/brain-training"
DATA = json.loads((BASE_DIR / "transcripts.json").read_text(encoding="utf-8"))

# Hand-crafted summaries for each video
SUMMARIES = {
    "1-1": "池田義博介紹自己從普通工程師到六屆日本記憶力冠軍的經歷，說明本課程旨在透過科學化的大腦訓練，全面提升記憶力、注意力、學習力等六大腦力。",
    "1-2": "說明大腦的「神經可塑性」——無論年齡都能建立新的神經連結。課程以「自我控制」與「影像控制」為基礎，強化前額葉與海馬迴功能，提升六大認知能力。",
    "2-1": "介紹正念冥想作為自我控制力的核心訓練，以及影像控制對記憶、專注、創造力的重要性。兩者都能鍛鍊前額葉皮質，是整門課程的能力基礎。",
    "2-2": "解說大腦的記憶原理：海馬迴如何決定短期記憶是否轉為長期記憶。提出促進記憶的三大條件——記憶意願、情感連結、資訊加工（前額葉皮質的思考活動）。",
    "2-3": "介紹認知心理學的兩大記憶策略：維持性複誦（適合短期或初階記憶）與精緻化（賦予意義、建立關聯、故事化、視覺化、用自己的話說明）。精緻化是本課程最重要的記憶概念。",
    "3-1": "介紹池田式正念冥想法——結合慢呼吸（吸:吐 = 1:2）與數字影像想像，透過提升心率變異（HRV）來強化自我控制力與前額葉皮質功能。建議每日練習，從5分鐘開始逐步增至20分鐘。",
    "3-2": "介紹「影像串流」訓練法：隨機選10個單字編成故事，邊想像影像邊出聲描述。同時訓練抽象化思考、想像力、語言表達與後設認知，全面鍛鍊前額葉皮質。進階版為不依靠單字自由延伸故事。",
    "4-1": "說明「三循環速習法」的理論基礎：記憶會遺忘、複習的最佳時機是快要遺忘時、速度學習優先建立整體框架。透過回憶促進現象，先建立框架後個別理解會自動加深。",
    "4-2": "三循環速習法的具體操作：以頁為區塊單位，按 a→a→b→a→b→c 的三循環順序推進學習。搭配檢查表維持動機與成就感，以閱讀為主、在理解不足處做記號，第二次複習後框架自動深化。",
    "5-1": "說明「輸出」對記憶鞏固的重要性：主動回憶（Active Recall）比反覆閱讀更能建立可運用的知識網絡。一分鐘寫作法結合三循環速習法，形成完美的輸入-輸出學習循環。",
    "5-2": "一分鐘寫作法的具體操作：選擇關鍵字、計時一分鐘、不停筆書寫。利用截止日期效應提升專注力，一分鐘不停筆為合格標準。搭配固定時間地點、降低門檻、記錄進度等技巧養成習慣。",
    "6-1": "介紹「框架式閱讀法」：利用促發效應（先讀目錄、想像內容），建立資訊框架後再重複閱讀。強調動手閱讀（畫線、寫筆記）的神經科學效益，以及「以輸出為前提閱讀」的心態。",
    "6-2": "介紹「PITA筆記法」：分為準備(P)、資訊記錄(I)、疑問想法(T)、解決(A)四區域。利用促發效應、蔡格尼克效應、生成效應等心理學原理，將工作記憶最大化用於思考，讓筆記成為知識資產。",
    "7-1": "介紹「A4一張記憶法」：將A4紙分為四區——問題區（主動回想）、答案區（抽認卡式訓練）、意義化區（精緻化/左腦語言處理）、影像區（右腦視覺化）。透過雙重編碼理論同時強化記憶、思考力與想像力。",
    "7-2": "探討創意的本質：靈感來自潛在記憶的重新組合，而非憑空產生。介紹預設模式網路（DMN）——大腦在放空狀態時活化，促進無意識記憶的重組，是產生創造性想法的關鍵腦內機制。",
    "7-3": "介紹「不間斷書寫法」：暫時放鬆前額葉皮質的理性控制（暫時性去抑制），從潛在記憶中引出自由發想。規則是不停筆、不給人看，讓思考的混沌原始素材自然湧現，培養創造性思維。",
    "8-1": "說明「未來記憶」的創造：利用圖像優勢效應與睡前記憶黃金時間，將目標以影像形式植入大腦。透過選擇性注意機制，潛意識會自動蒐集與目標相關的資訊。介紹SMART目標設定法。",
    "8-2": "介紹目標達成的實踐策略：小步驟思維（萬里長城故事）、If-Then計劃法、替代強化、內在動機與自我決定理論（自主性、勝任感、關聯性）、認知偏誤的重新框架。四大力量：未來記憶、習慣機制、行為設計、思考為盟友。",
}

# YouTube video IDs (playlist: PLKInOIgV1wdJCO2OC14czXZlveaPXijL6)
PLAYLIST_ID = "PLKInOIgV1wdJCO2OC14czXZlveaPXijL6"
VIDEO_YT_IDS = {
    "1-1": "3WKZ-94JoKw",
    "1-2": "QVkI4dNmQuU",
    "2-1": "tOnZW9NmHak",
    "2-2": "504r4qrQJ8I",
    "2-3": "cFuBPZac-oM",
    "3-1": "a7i9szGURaE",
    "3-2": "TI-Eemx3prQ",
    "4-1": "56q2Yu8KbeE",
    "4-2": "qoznIhhou18",
    "5-1": "U7xJr9lM1QE",
    "5-2": "QTyfviBvp-M",
    "6-1": "f4-fTzyi9bQ",
    "6-2": "f__Gy4W0CaQ",
    "7-1": "GBVTpSLWoSc",
    "7-2": "tlYRALjNjxg",
    "7-3": "109ULwX8eCc",
    "8-1": "QVzQGsZEEbA",
    "8-2": "0JYrnaD7ACc",
}


def yt_url(video_id: str) -> str:
    """Build YouTube URL with playlist context."""
    yt_id = VIDEO_YT_IDS.get(video_id, "")
    if not yt_id:
        return ""
    return f"https://www.youtube.com/watch?v={yt_id}&list={PLAYLIST_ID}"


def generate_markdown() -> str:
    lines = []
    lines.append(f"# {DATA['course_title']}")
    lines.append("")
    lines.append(f"**講師：** {DATA['author']}")
    lines.append(f"**影片數：** {DATA['total_videos']}")
    lines.append(f"**生成日期：** {date.today().isoformat()}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 目錄")
    lines.append("")

    for v in DATA["videos"]:
        anchor = v["id"].replace("-", "")
        lines.append(f"- [{v['full_title']}](#{anchor}-{v['title'].replace(' ', '-').replace('｜', '').replace('「', '').replace('」', '')})")

    lines.append("")
    lines.append("---")
    lines.append("")

    for v in DATA["videos"]:
        vid = v["id"]
        lines.append(f"## {v['full_title']}")
        lines.append("")
        if vid in SUMMARIES:
            lines.append(f"> {SUMMARIES[vid]}")
            lines.append("")
        yt_id = VIDEO_YT_IDS.get(vid, "")
        if yt_id:
            yt_watch = f"https://www.youtube.com/watch?v={yt_id}&list={PLAYLIST_ID}"
            yt_thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
            lines.append(f"[![▶ 觀看影片]({yt_thumb})]({yt_watch})")
            lines.append("")
        lines.append(f"**字幕數：** {v['entry_count']}")
        lines.append("")
        # Insert transcript with each subtitle line separated by newline
        for tl in v["lines"]:
            lines.append(tl)
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_html() -> str:
    videos_html = []
    toc_html = []
    sidebar_toc_html = []
    current_chapter = None

    for v in DATA["videos"]:
        vid = v["id"]
        anchor = f"video-{vid}"
        toc_html.append(f'<li><a href="#{anchor}">{v["full_title"]}</a></li>')

        # Build sidebar TOC with chapter grouping
        chapter = vid.split("-")[0]
        if chapter != current_chapter:
            if current_chapter is not None:
                sidebar_toc_html.append('</ul>')
            sidebar_toc_html.append(f'<div class="sidebar-chapter">第 {chapter} 章</div>')
            sidebar_toc_html.append('<ul>')
            current_chapter = chapter
        sidebar_toc_html.append(
            f'<li><a href="#{anchor}" data-target="{anchor}">{v["full_title"]}</a></li>'
        )

        summary = SUMMARIES.get(vid, "")
        transcript_paras = "\n".join(f"<p>{line}</p>" for line in v["lines"])
        yt_id = VIDEO_YT_IDS.get(vid, "")
        yt_embed = ""
        if yt_id:
            yt_embed = f"""<div class="yt-thumb" onclick="loadVideo(this, '{yt_id}')" data-yt="{yt_id}">
        <img src="https://img.youtube.com/vi/{yt_id}/hqdefault.jpg" alt="{v['full_title']}" loading="lazy">
        <span class="yt-play">▶</span>
      </div>"""

        videos_html.append(f"""
    <section class="video-section" id="{anchor}">
      <h2>{v["full_title"]}</h2>
      <p class="summary">{summary}</p>
      <p class="meta">字幕數：{v["entry_count"]}</p>
      {yt_embed}
      <details>
        <summary>展開完整逐字稿</summary>
        <div class="transcript">{transcript_paras}</div>
      </details>
    </section>""")

    if current_chapter is not None:
        sidebar_toc_html.append('</ul>')

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{DATA["course_title"]} — 完整逐字稿</title>
<style>
:root {{
  --bg: #fafafa;
  --fg: #1a1a1a;
  --bg-card: #ffffff;
  --border: #e0e0e0;
  --accent: #2563eb;
  --accent-light: #dbeafe;
  --summary-bg: #f0f7ff;
  --summary-border: #93c5fd;
  --meta: #6b7280;
  --search-highlight: #fef08a;
  --font-size: 1rem;
  --line-height: 1.8;
  --letter-spacing: 0;
}}
[data-theme="dark"] {{
  --bg: #111827;
  --fg: #f3f4f6;
  --bg-card: #1f2937;
  --border: #374151;
  --accent: #60a5fa;
  --accent-light: #1e3a5f;
  --summary-bg: #1e293b;
  --summary-border: #3b82f6;
  --meta: #9ca3af;
  --search-highlight: #854d0e;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
  background: var(--bg);
  color: var(--fg);
  font-size: var(--font-size);
  line-height: var(--line-height);
  letter-spacing: var(--letter-spacing);
  transition: background 0.3s, color 0.3s, font-size 0.2s, line-height 0.2s;
}}
.container {{
  max-width: 860px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}}
header {{
  text-align: center;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid var(--border);
}}
header h1 {{
  font-size: 2rem;
  margin-bottom: 0.5rem;
}}
header .meta-info {{
  color: var(--meta);
  font-size: inherit;
}}
.toolbar {{
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}}
.toolbar input {{
  flex: 1;
  min-width: 200px;
  padding: 0.6rem 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--bg-card);
  color: var(--fg);
  outline: none;
}}
.toolbar input:focus {{
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-light);
}}
.toolbar button {{
  padding: 0.6rem 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg-card);
  color: var(--fg);
  cursor: pointer;
  font-size: 0.95rem;
  white-space: nowrap;
}}
.toolbar button:hover {{
  border-color: var(--accent);
}}
nav.toc {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
}}
nav.toc h3 {{
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
}}
nav.toc ol {{
  padding-left: 1.5rem;
}}
nav.toc li {{
  margin-bottom: 0.3rem;
}}
nav.toc a {{
  color: var(--accent);
  text-decoration: none;
}}
nav.toc a:hover {{
  text-decoration: underline;
}}
.video-section {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}}
.video-section h2 {{
  font-size: 1.35rem;
  margin-bottom: 0.75rem;
  color: var(--accent);
}}
.summary {{
  background: var(--summary-bg);
  border-left: 4px solid var(--summary-border);
  padding: 0.75rem 1rem;
  border-radius: 0 8px 8px 0;
  margin-bottom: 0.75rem;
  font-size: inherit;
}}
.meta {{
  color: var(--meta);
  font-size: inherit;
  margin-bottom: 0.5rem;
}}
.yt-thumb {{
  display: block;
  position: relative;
  max-width: 640px;
  margin: 0.75rem 0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}}
.yt-thumb:hover {{
  transform: scale(1.02);
  box-shadow: 0 4px 16px rgba(0,0,0,0.25);
}}
.yt-thumb img {{
  display: block;
  width: 100%;
  height: auto;
}}
.yt-play {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 68px;
  height: 48px;
  background: rgba(255, 0, 0, 0.85);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  color: #fff;
  pointer-events: none;
  transition: background 0.2s;
}}
.yt-thumb:hover .yt-play {{
  background: rgba(255, 0, 0, 1);
}}
.video-container {{
  position: relative;
  max-width: 640px;
  margin: 0.75rem 0;
  padding-bottom: min(360px, 56.25%);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}}
.video-container iframe {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  border: 0;
}}
details {{
  margin-top: 0.5rem;
}}
details summary {{
  cursor: pointer;
  color: var(--accent);
  font-weight: 500;
  padding: 0.4rem 0;
  user-select: none;
}}
details summary:hover {{
  text-decoration: underline;
}}
.transcript {{
  margin-top: 0.75rem;
  padding: 1rem;
  background: var(--bg);
  border-radius: 8px;
  font-size: inherit;
  line-height: inherit;
}}
.transcript.scrollable {{
  max-height: 60vh;
  overflow-y: auto;
  scroll-behavior: smooth;
}}
.hidden {{
  display: none !important;
}}
mark {{
  background: var(--search-highlight);
  color: inherit;
  padding: 0 2px;
  border-radius: 2px;
}}
footer {{
  text-align: center;
  padding: 2rem 0 1rem;
  color: var(--meta);
  font-size: 0.85rem;
  border-top: 1px solid var(--border);
  margin-top: 2rem;
}}
.expand-controls {{
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}}
.expand-controls button {{
  padding: 0.4rem 0.8rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg-card);
  color: var(--fg);
  cursor: pointer;
  font-size: 0.85rem;
}}
.expand-controls button:hover {{
  border-color: var(--accent);
}}
.font-controls {{
  display: flex;
  gap: 0.4rem;
  align-items: center;
  flex-wrap: wrap;
}}
.font-controls button {{
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg-card);
  color: var(--fg);
  cursor: pointer;
  font-size: 0.95rem;
  white-space: nowrap;
}}
.font-controls button:hover {{
  border-color: var(--accent);
}}
.font-controls button.active {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.font-controls .size-label {{
  font-size: 0.85rem;
  color: var(--meta);
  min-width: 2.5rem;
  text-align: center;
}}
@media (max-width: 600px) {{
  .container {{ padding: 1rem; }}
  header h1 {{ font-size: 1.5rem; }}
  .toolbar {{ flex-direction: column; }}
  .toolbar input {{ min-width: 100%; }}
  .font-controls {{ justify-content: center; }}
}}

/* Floating TOC Sidebar */
#floating-toc {{
  position: fixed;
  top: 0;
  left: 0;
  width: 260px;
  height: 100vh;
  background: var(--bg-card);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  padding: 1.25rem 1rem;
  z-index: 1000;
  transition: transform 0.3s ease, background 0.3s;
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}}
#floating-toc::-webkit-scrollbar {{
  width: 4px;
}}
#floating-toc::-webkit-scrollbar-track {{
  background: transparent;
}}
#floating-toc::-webkit-scrollbar-thumb {{
  background: var(--border);
  border-radius: 2px;
}}
#floating-toc .sidebar-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}}
#floating-toc .sidebar-header h3 {{
  font-size: 1rem;
  margin: 0;
}}
#floating-toc .sidebar-close {{
  background: none;
  border: none;
  color: var(--meta);
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.2rem;
  line-height: 1;
}}
#floating-toc .sidebar-close:hover {{
  color: var(--fg);
}}
.sidebar-chapter {{
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--meta);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 0.75rem;
  margin-bottom: 0.25rem;
  padding-left: 0.5rem;
}}
#floating-toc ul {{
  list-style: none;
  padding: 0;
  margin: 0 0 0.25rem 0;
}}
#floating-toc li a {{
  display: block;
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  color: var(--fg);
  text-decoration: none;
  font-size: 0.82rem;
  line-height: 1.4;
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
#floating-toc li a:hover {{
  background: var(--accent-light);
  color: var(--accent);
}}
#floating-toc li a.active {{
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 600;
}}

/* Toggle button */
#toc-toggle {{
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--fg);
  cursor: pointer;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: background 0.3s, transform 0.3s;
}}
#toc-toggle:hover {{
  border-color: var(--accent);
}}

/* Body shift when sidebar is open */
body.sidebar-open {{
  margin-left: 260px;
  transition: margin-left 0.3s ease;
}}
body {{
  transition: margin-left 0.3s ease;
}}

/* Hide sidebar when closed */
#floating-toc.closed {{
  transform: translateX(-100%);
}}
body.sidebar-open #toc-toggle {{
  left: 268px;
}}

/* Responsive: hide sidebar on narrow screens */
@media (max-width: 1200px) {{
  #floating-toc {{
    transform: translateX(-100%);
    box-shadow: 2px 0 16px rgba(0,0,0,0.15);
  }}
  #floating-toc.mobile-open {{
    transform: translateX(0);
  }}
  body.sidebar-open {{
    margin-left: 0;
  }}
  body.sidebar-open #toc-toggle {{
    left: 1rem;
  }}
  #toc-toggle {{
    display: flex;
  }}
}}
@media (min-width: 1201px) {{
  /* On wide screens, sidebar is open by default */
  #floating-toc {{
    transform: translateX(0);
  }}
  #floating-toc.closed {{
    transform: translateX(-100%);
  }}
}}
</style>
</head>
<body>
<button id="toc-toggle" onclick="toggleSidebar()" title="目錄">☰</button>
<aside id="floating-toc">
  <div class="sidebar-header">
    <h3>📖 目錄</h3>
    <button class="sidebar-close" onclick="toggleSidebar()" title="關閉目錄">✕</button>
  </div>
  {"".join(sidebar_toc_html)}
</aside>
<div class="container">
  <header>
    <h1>{DATA["course_title"]}</h1>
    <div class="meta-info">
      講師：{DATA["author"]} ・ 共 {DATA["total_videos"]} 支影片 ・ 生成日期：{date.today().isoformat()}
    </div>
  </header>

  <div class="toolbar">
    <input type="text" id="search" placeholder="搜尋逐字稿內容..." autocomplete="off">
    <button onclick="clearSearch()">清除</button>
    <button onclick="toggleTheme()" id="theme-btn">🌙 深色模式</button>
  </div>

  <div class="expand-controls">
    <button onclick="expandAll()">全部展開</button>
    <button onclick="collapseAll()">全部收合</button>
    <span style="margin-left: auto;"></span>
    <div class="font-controls">
      <button onclick="changeFontSize(-1)" title="縮小字體">A-</button>
      <span class="size-label" id="size-label">M</span>
      <button onclick="changeFontSize(1)" title="放大字體">A+</button>
      <button onclick="toggleEyeFriendly()" id="eye-btn">👁 護眼模式</button>
    </div>
  </div>

  <nav class="toc">
    <h3>目錄</h3>
    <ol>
      {"".join(toc_html)}
    </ol>
  </nav>

  {"".join(videos_html)}

  <footer>
    {DATA["course_title"]} — {DATA["author"]} ・ 逐字稿由 AI 視覺辨識燒入字幕提取
  </footer>
</div>

<script>
// Click-to-load YouTube player (replaces thumbnail with iframe)
function loadVideo(el, ytId) {{
  const container = document.createElement('div');
  container.className = 'video-container';
  container.innerHTML = '<iframe width="560" height="315"'
    + ' src="https://www.youtube.com/embed/' + ytId + '?autoplay=1"'
    + ' title="YouTube video player" frameborder="0"'
    + ' allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"'
    + ' referrerpolicy="strict-origin-when-cross-origin"'
    + ' allowfullscreen></iframe>';
  el.replaceWith(container);
  // Auto-expand transcript and make it scrollable
  const section = container.closest('.video-section');
  if (section) {{
    const details = section.querySelector('details');
    const transcript = section.querySelector('.transcript');
    if (details) details.open = true;
    if (transcript) transcript.classList.add('scrollable');
  }}
}}

// Dark mode toggle
function toggleTheme() {{
  const body = document.documentElement;
  const current = body.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  body.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  document.getElementById('theme-btn').textContent =
    next === 'dark' ? '☀️ 淺色模式' : '🌙 深色模式';
}}

// Restore theme
(function() {{
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') {{
    document.documentElement.setAttribute('data-theme', 'dark');
    document.addEventListener('DOMContentLoaded', () => {{
      document.getElementById('theme-btn').textContent = '☀️ 淺色模式';
    }});
  }}
}})();

// Search
const searchInput = document.getElementById('search');
let searchTimeout;
searchInput.addEventListener('input', () => {{
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(doSearch, 300);
}});

function doSearch() {{
  const query = searchInput.value.trim().toLowerCase();
  const sections = document.querySelectorAll('.video-section');

  // Clear previous highlights
  document.querySelectorAll('mark').forEach(m => {{
    m.replaceWith(m.textContent);
  }});

  if (!query) {{
    sections.forEach(s => s.classList.remove('hidden'));
    return;
  }}

  sections.forEach(section => {{
    const text = section.textContent.toLowerCase();
    if (text.includes(query)) {{
      section.classList.remove('hidden');
      // Open details if match is in transcript
      const details = section.querySelector('details');
      const transcript = section.querySelector('.transcript');
      if (transcript && transcript.textContent.toLowerCase().includes(query)) {{
        details.open = true;
        highlightText(transcript, query);
      }}
      // Also highlight in summary
      const summary = section.querySelector('.summary');
      if (summary && summary.textContent.toLowerCase().includes(query)) {{
        highlightText(summary, query);
      }}
    }} else {{
      section.classList.add('hidden');
    }}
  }});
}}

function highlightText(el, query) {{
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(node => {{
    const idx = node.textContent.toLowerCase().indexOf(query);
    if (idx >= 0) {{
      const span = document.createElement('span');
      span.innerHTML = node.textContent.substring(0, idx)
        + '<mark>' + node.textContent.substring(idx, idx + query.length) + '</mark>'
        + node.textContent.substring(idx + query.length);
      node.replaceWith(span);
    }}
  }});
}}

function clearSearch() {{
  searchInput.value = '';
  doSearch();
}}

function expandAll() {{
  document.querySelectorAll('details').forEach(d => d.open = true);
}}

function collapseAll() {{
  document.querySelectorAll('details').forEach(d => d.open = false);
}}

// Font size control
const SIZES = [
  {{ label: 'XS', size: '0.85rem', line: '1.6', spacing: '0' }},
  {{ label: 'S',  size: '0.95rem', line: '1.8', spacing: '0' }},
  {{ label: 'M',  size: '1rem',    line: '1.8', spacing: '0' }},
  {{ label: 'L',  size: '1.15rem', line: '2.0', spacing: '0.02em' }},
  {{ label: 'XL', size: '1.3rem',  line: '2.2', spacing: '0.03em' }},
  {{ label: '2XL', size: '1.5rem', line: '2.4', spacing: '0.04em' }},
];
let currentSizeIdx = parseInt(localStorage.getItem('fontSizeIdx') || '2');
let eyeFriendly = localStorage.getItem('eyeFriendly') === 'true';
let preEyeTheme = localStorage.getItem('preEyeTheme') || 'light';
let preEyeSizeIdx = parseInt(localStorage.getItem('preEyeSizeIdx') || '2');

function applyFontSize() {{
  const s = SIZES[currentSizeIdx];
  const root = document.documentElement;
  root.style.setProperty('--font-size', s.size);
  root.style.setProperty('--line-height', s.line);
  root.style.setProperty('--letter-spacing', s.spacing);
  document.getElementById('size-label').textContent = s.label;
  localStorage.setItem('fontSizeIdx', currentSizeIdx);
}}

function changeFontSize(delta) {{
  currentSizeIdx = Math.max(0, Math.min(SIZES.length - 1, currentSizeIdx + delta));
  applyFontSize();
}}

function toggleEyeFriendly() {{
  eyeFriendly = !eyeFriendly;
  applyEyeFriendly();
}}

function applyEyeFriendly() {{
  const btn = document.getElementById('eye-btn');
  if (eyeFriendly) {{
    // Save current state before switching
    preEyeTheme = document.documentElement.getAttribute('data-theme') || 'light';
    preEyeSizeIdx = currentSizeIdx;
    localStorage.setItem('preEyeTheme', preEyeTheme);
    localStorage.setItem('preEyeSizeIdx', preEyeSizeIdx);
    // Jump to at least L size
    if (currentSizeIdx < 3) currentSizeIdx = 3;
    applyFontSize();
    document.documentElement.setAttribute('data-theme', 'dark');
    document.getElementById('theme-btn').textContent = '☀️ 淺色模式';
    localStorage.setItem('theme', 'dark');
    btn.textContent = '👁 護眼開啟';
    btn.classList.add('active');
  }} else {{
    // Restore previous theme
    const restoreTheme = preEyeTheme || 'light';
    document.documentElement.setAttribute('data-theme', restoreTheme);
    document.getElementById('theme-btn').textContent =
      restoreTheme === 'dark' ? '☀️ 淺色模式' : '🌙 深色模式';
    localStorage.setItem('theme', restoreTheme);
    // Restore previous font size
    currentSizeIdx = preEyeSizeIdx;
    applyFontSize();
    btn.textContent = '👁 護眼模式';
    btn.classList.remove('active');
  }}
  localStorage.setItem('eyeFriendly', eyeFriendly);
}}

// Floating TOC Sidebar
function toggleSidebar() {{
  const sidebar = document.getElementById('floating-toc');
  const isWide = window.innerWidth > 1200;

  if (isWide) {{
    sidebar.classList.toggle('closed');
    document.body.classList.toggle('sidebar-open');
    localStorage.setItem('sidebarOpen', !sidebar.classList.contains('closed'));
  }} else {{
    sidebar.classList.toggle('mobile-open');
  }}
}}

// Active section tracking with IntersectionObserver
function initSidebarObserver() {{
  const sidebarLinks = document.querySelectorAll('#floating-toc a[data-target]');
  const sections = document.querySelectorAll('.video-section');

  if (!sections.length) return;

  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        // Remove active from all links
        sidebarLinks.forEach(link => link.classList.remove('active'));
        // Add active to matching link
        const target = entry.target.id;
        const activeLink = document.querySelector(
          `#floating-toc a[data-target="${{target}}"]`
        );
        if (activeLink) {{
          activeLink.classList.add('active');
          // Auto-scroll sidebar to keep active link visible
          activeLink.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
        }}
      }}
    }});
  }}, {{
    rootMargin: '-10% 0px -80% 0px',
    threshold: 0
  }});

  sections.forEach(section => observer.observe(section));
}}

// Sidebar click handler: smooth scroll + close on mobile
document.getElementById('floating-toc').addEventListener('click', (e) => {{
  const link = e.target.closest('a[data-target]');
  if (!link) return;
  e.preventDefault();
  const target = document.getElementById(link.dataset.target);
  if (target) {{
    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
  // Close sidebar on mobile after click
  if (window.innerWidth <= 1200) {{
    document.getElementById('floating-toc').classList.remove('mobile-open');
  }}
}});

// Restore on load
document.addEventListener('DOMContentLoaded', () => {{
  applyFontSize();
  if (eyeFriendly) applyEyeFriendly();

  // Restore sidebar state (desktop only)
  const isWide = window.innerWidth > 1200;
  const sidebarPref = localStorage.getItem('sidebarOpen');
  const sidebar = document.getElementById('floating-toc');
  if (isWide) {{
    if (sidebarPref === 'false') {{
      sidebar.classList.add('closed');
    }} else {{
      document.body.classList.add('sidebar-open');
    }}
  }}

  // Init observer
  initSidebarObserver();
}});
</script>
</body>
</html>"""


def main():
    html = generate_html()
    html_path = DEPLOY_DIR / "科學的大腦鍛鍊法_transcript.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"Wrote {html_path} ({len(html):,} chars)")


if __name__ == "__main__":
    main()
