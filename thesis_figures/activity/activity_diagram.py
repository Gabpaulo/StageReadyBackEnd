"""Overall StageReady activity diagram (UML). Run: python activity_diagram.py -> activity_overall.svg"""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity_overall.svg")
COL = {  # fill, stroke per actor
    "U": ("#DCEBFA", "#3A6EA5"),   # user
    "A": ("#E8E0F5", "#6B4FA0"),   # administrator
    "S": ("#E3F1E1", "#4A8A45"),   # app + Firebase
    "B": ("#FCEBD2", "#B9771E"),   # AI backend
}
W, H = 1280, 1530
BH = 46
svg = []
def add(s): svg.append(s)
def text(x, y, s, size=13, anchor="middle", weight="normal", style="normal"):
    lines = s.split("\n"); lh = size * 1.22
    y0 = y - (len(lines) - 1) * lh / 2
    for i, l in enumerate(lines):
        add(f'<text x="{x}" y="{y0 + i*lh:.1f}" font-size="{size}" text-anchor="{anchor}" dominant-baseline="middle" font-weight="{weight}" font-style="{style}">{l}</text>')
def box(x, y, label, actor, w=200, h=BH):
    f, s = COL[actor]
    add(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="14" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    text(x, y, label, 12.5)
def diamond(x, y, label, w=150, h=56):
    add(f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" fill="#FFFFFF" stroke="#444" stroke-width="1.6"/>')
    text(x, y, label, 12)
def path(pts, arrow=True):
    d = "M " + " L ".join(f"{a},{b}" for a, b in pts)
    add(f'<path d="{d}" fill="none" stroke="#333" stroke-width="1.4"{" marker-end=\"url(#ah)\"" if arrow else ""}/>')
def guard(x, y, s, anchor="middle"):
    text(x, y, s, 11.5, anchor, style="italic")
def bar(x1, x2, y):
    add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#333" stroke-width="1.4"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
add('<defs><marker id="ah" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#333"/></marker></defs>')
add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

M = 495   # main spine
# --- entry flow ---
add(f'<circle cx="{M}" cy="40" r="11" fill="#222"/>')
path([(M, 51), (M, 77)])
box(M, 100, "Open StageReady", "U")
path([(M, 123), (M, 151)])
box(M, 174, "Log in or register\n(email or Google)", "U", w=220)
path([(M, 197), (M, 226)])
diamond(M, 254, "Credentials\nvalid?")
path([(M-75, 254), (330, 254), (330, 174), (M-110, 174)]); guard(345, 240, "[no]", "start")
path([(M, 282), (M, 306)]); guard(M+8, 294, "[yes]", "start")
diamond(M, 334, "Admin\naccount?")
path([(M+75, 334), (1020, 334)]); guard(M+90, 320, "[yes]", "start")
path([(M, 362), (M, 386)]); guard(M+8, 374, "[no]", "start")
diamond(M, 414, "Onboarding\ncomplete?")
box(240, 414, "Complete onboarding\n(name, age, interests,\nspeech type)", "U", w=210, h=60)
path([(M-75, 414), (345, 414)]); guard(M-85, 400, "[no]", "end")
path([(240, 444), (240, 510), (M-150, 510)])
path([(M, 442), (M, 487)]); guard(M+8, 464, "[yes]", "start")
box(M, 510, "Load dashboard (XP, level, streak,\ndaily challenge, practice plan)", "S", w=300)
path([(M, 533), (M, 572)])
diamond(M, 600, "Choose\nactivity", w=140)

# --- four activity branches ---
xs = [150, 380, 610, 840]
path([(M, 628), (M, 655)], arrow=False)
bar(xs[0], xs[3], 655)
labels = ["[record speech]", "[practice script]", "[take quiz]", "[review progress]"]
for x, g in zip(xs, labels):
    path([(x, 655), (x, 687)]); guard(x+6, 672, g, "start")
Y0, ST = 710, 72
cols = [
    [("Record speech and\nchoose speech type", "U"), ("Transcribe audio\n(Whisper)", "B"),
     ("Extract acoustic\nfeatures", "B"), ("Retrieve similar speeches\nand expert tips\n(Corpus 1 + Corpus 2)", "B"),
     ("Generate scores and\nfeedback (LLM)", "B"), ("Save session to\nFirestore", "S"),
     ("Update XP, streak\nand badges", "S"), ("View feedback\nreport", "U")],
    [("Select practice\nscript", "U"), ("Read script aloud\nand record", "U"), ("Transcribe audio\n(Whisper)", "B"),
     ("Compute word\naccuracy and WPM", "S"), ("Save practice\nsession", "S"), ("View practice\nresults", "U")],
    [("Open Knowledge Base\nquiz", "U"), ("Generate quiz from\nCorpus 2 (weak areas)", "B"),
     ("Answer quiz\nquestions", "U"), ("Show quiz score", "S")],
    [("Open history, badges\nor profile", "U"), ("Retrieve user records\nfrom Firestore", "S"),
     ("Review progress or\nedit profile", "U")],
]
MERGE = 1290
for x, steps in zip(xs, cols):
    for i, (lbl, a) in enumerate(steps):
        y = Y0 + i*ST
        h = 60 if lbl.count("\n") >= 2 else BH
        box(x, y, lbl, a, h=h)
        nh = 60 if i+1 < len(steps) and steps[i+1][0].count("\n") >= 2 else BH
        if i+1 < len(steps):
            path([(x, y + h/2), (x, y + ST - nh/2)])
        else:
            path([(x, y + h/2), (x, MERGE)], arrow=False)
bar(xs[0], xs[3], MERGE)
path([(M, MERGE), (M, 1322)])
diamond(M, 1350, "Continue\npractising?", w=160)
path([(M-80, 1350), (40, 1350), (40, 600), (M-70, 600)]); guard(M-92, 1336, "[yes]", "end")
path([(M, 1378), (M, 1407)]); guard(M+8, 1392, "[no]", "start")
box(M, 1430, "Log out", "U", w=160)
path([(M, 1453), (M, 1475)])
add(f'<circle cx="{M}" cy="1490" r="14" fill="#FFF" stroke="#222" stroke-width="2"/><circle cx="{M}" cy="1490" r="8" fill="#222"/>')

# --- administrator flow ---
AX = 1130
box(AX, 334, "Open admin\ndashboard", "A", w=220)
path([(AX, 357), (AX, 383)])
box(AX, 406, "Select module (users,\nscripts, badges, speeches)", "A", w=220)
path([(AX, 429), (AX, 455)])
box(AX, 478, "Add, edit or delete\na record", "A", w=220)
path([(AX, 501), (AX, 530)])
diamond(AX, 558, "Input\nvalid?")
path([(AX+75, 558), (1262, 558), (1262, 478), (AX+110, 478)]); guard(AX+85, 544, "[no]", "start")
path([(AX, 586), (AX, 615)]); guard(AX+8, 600, "[yes]", "start")
box(AX, 638, "Save changes to\nFirestore", "S", w=220)
path([(AX, 661), (AX, 690)])
diamond(AX, 718, "More\nchanges?")
path([(AX-75, 718), (1000, 718), (1000, 406), (AX-110, 406)]); guard(AX-85, 704, "[yes]", "end")
path([(AX, 746), (AX, 775)]); guard(AX+8, 760, "[no]", "start")
box(AX, 798, "Log out", "A", w=160)
path([(AX, 821), (AX, 1490), (M+14, 1490)])

# --- legend ---
lx, ly = 900, 30
add(f'<rect x="{lx}" y="{ly}" width="350" height="150" rx="6" fill="#FFF" stroke="#999"/>')
text(lx+16, ly+20, "Legend: who performs the action", 13, "start", "bold")
for i, (k, name) in enumerate([("U", "User (student)"), ("A", "Administrator"),
                               ("S", "StageReady app + Firebase"), ("B", "AI backend (FastAPI + RAG)")]):
    f, s = COL[k]; yy = ly + 46 + i*26
    add(f'<rect x="{lx+16}" y="{yy-9}" width="34" height="18" rx="6" fill="{f}" stroke="{s}" stroke-width="1.4"/>')
    text(lx+62, yy, name, 12.5, "start")
add('</svg>')
open(OUT, "w").write("\n".join(svg))
print(OUT)
