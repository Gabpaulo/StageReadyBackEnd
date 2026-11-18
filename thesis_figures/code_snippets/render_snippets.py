"""Render real code excerpts from the StageReady repos as syntax-highlighted PNGs.
Each listing = (id, title, repo-relative path, language, [(start,end) line ranges]).
Gaps between ranges are shown as an elision line. Line numbers are the real file lines.
Usage: python render_snippets.py <ionic_repo> <backend_repo> <out_dir>  (writes html/), then node shoot.js <out_dir>
"""
import sys, html, os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

ION, BE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SVC = "src/app/services/speech-analysis-api.service.ts"
L = [
 ("3.1", "transcribe endpoint (Groq Whisper)", BE, "RAGBackEnd/main.py", "python", [(160, 186)]),
 ("3.2", "pause detection from word timestamps", ION, SVC, "typescript", [(276, 293), (303, 312)]),
 ("3.3", "acoustic feature extraction (NumPy)", BE, "RAGBackEnd/main.py", "python", [(67, 95), (120, 136)]),
 ("3.4", "Corpus 2 chunking and embedding", BE, "RAGBackEnd/ingest.py", "python", [(45, 66), (114, 122)]),
 ("3.5", "Practice Mode word accuracy", ION, SVC, "typescript", [(447, 455), (498, 521)]),
 ("3.6", "Corpus 1 cosine similarity retrieval", BE, "RAGBackEnd/retrieval.py", "python", [(34, 63)]),
 ("3.7", "weak areas measured from the session", BE, "RAGBackEnd/retrieval.py", "python", [(137, 170)]),
 ("3.8", "LLM call with structured JSON output", BE, "RAGBackEnd/main.py", "python", [(284, 318)]),
 ("3.9", "category weights and weighted overall", ION, SVC, "typescript", [(153, 178)]),
 ("3.10", "TensorFlow.js regression for high-impact dimensions", ION, "src/app/services/adaptive-learning.service.ts", "typescript", [(229, 256)]),
]

CSS_EXTRA = """
body{margin:0;background:#fff;}
.card{display:inline-block;margin:0;border:1px solid #d0d7de;border-radius:8px;overflow:hidden;
 font-family:'JetBrains Mono',monospace;font-size:13.5px;background:#f6f8fa;font-variant-ligatures:none;font-feature-settings:'liga' 0,'calt' 0;}
.bar{background:#eaeef2;border-bottom:1px solid #d0d7de;padding:7px 14px;font-size:12px;color:#57606a;
 font-family:'JetBrains Mono',monospace;display:flex;gap:8px;align-items:center}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
table{border-collapse:collapse;margin:8px 0}
td.ln{color:#8c959f;text-align:right;padding:0 12px 0 14px;user-select:none;vertical-align:top;white-space:pre}
td.code{padding:0 18px 0 4px;max-width:92ch}
td.code pre{white-space:pre-wrap;overflow-wrap:anywhere;padding-left:4ch;text-indent:-4ch}
.code pre, .ln pre{margin:0;line-height:1.5;font-family:inherit}
.gap td{color:#8c959f;font-style:italic}
"""

def render(entry):
    lid, title, root, path, lang, ranges = entry
    src = open(os.path.join(root, path), encoding="utf-8").read().split("\n")
    lexer = get_lexer_by_name(lang)
    fmt = HtmlFormatter(style="default", nowrap=True)
    rows = []
    allines = [l for (a, b) in ranges for l in src[a-1:b]]
    ind = min((len(l) - len(l.lstrip()) for l in allines if l.strip()), default=0)
    for k, (a, b) in enumerate(ranges):
        if k:
            rows.append('<tr class="gap"><td class="ln"><pre>⋮</pre></td><td class="code"><pre>  …</pre></td></tr>')
        block = src[a-1:b]
        hl = highlight("\n".join(l[ind:] for l in block), lexer, fmt).rstrip("\n").split("\n")
        for n, line in zip(range(a, b+1), hl):
            rows.append(f'<tr><td class="ln"><pre>{n}</pre></td><td class="code"><pre>{line or " "}</pre></td></tr>')
    css = fmt.get_style_defs(".code") + CSS_EXTRA
    doc = f"""<html><head><meta charset=utf-8><style>{css}</style></head><body>
<div class=card id=card><div class=bar><span class=dot style="background:#ff5f57"></span>
<span class=dot style="background:#febc2e"></span><span class=dot style="background:#28c840"></span>
<span style="margin-left:8px">{html.escape(path)}</span></div><table>{''.join(rows)}</table></div></body></html>"""
    return doc

os.makedirs(os.path.join(OUT, "html"), exist_ok=True)
for e in L:
    fn = os.path.join(OUT, "html", f"listing_{e[0].replace('.', '_')}.html")
    open(fn, "w", encoding="utf-8").write(render(e))
    print(fn)
