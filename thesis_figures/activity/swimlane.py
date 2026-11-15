"""Swimlane UML activity diagram renderer -> SVG. Used by diagrams.py."""
LANE_STYLE = {
    "User": ("#DCEBFA", "#3A6EA5", "#F3F8FD"),
    "Administrator": ("#E8E0F5", "#6B4FA0", "#F7F4FB"),
    "StageReady App / Firebase": ("#E3F1E1", "#4A8A45", "#F5FAF4"),
    "AI Backend (FastAPI + RAG)": ("#FCEBD2", "#B9771E", "#FDF8EF"),
}
LW, RH, TOP, HEAD = 330, 84, 2, 44
BW, BH = 220, 50

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render(spec, path):
    lanes = spec["lanes"]; nodes = spec["nodes"]
    maxrow = max(n[2] for n in nodes.values())
    W = LW * len(lanes); H = TOP + HEAD + (maxrow + 1) * RH
    out = []
    a = out.append
    def X(lane, dx=0): return lanes.index(lane) * LW + LW / 2 + dx
    def Y(row, dy=0): return TOP + HEAD + row * RH + RH / 2 - 20 + dy
    geo = {}
    for k, n in nodes.items():
        kind, lane, row, label = n[:4]; opt = n[4] if len(n) > 4 else {}
        x, y = X(lane, opt.get("dx", 0)), Y(row)
        if kind == "act":
            w = opt.get("w", BW); h = 64 if label.count("\n") >= 2 else BH
        elif kind == "dec":
            w, h = opt.get("w", 136), 58
        else:
            w = h = 28
        geo[k] = (x, y, w, h, kind, lane, label)
    def port(k, side):
        x, y, w, h = geo[k][:4]
        return {"t": (x, y - h/2), "b": (x, y + h/2), "l": (x - w/2, y), "r": (x + w/2, y)}[side]
    def text(x, y, s, size=12.5, anchor="middle", weight="normal", style="normal", fill="#111"):
        lines = s.split("\n"); lh = size * 1.22; y0 = y - (len(lines) - 1) * lh / 2
        for i, l in enumerate(lines):
            a(f'<text x="{x:.1f}" y="{y0+i*lh:.1f}" font-size="{size}" text-anchor="{anchor}" dominant-baseline="middle" font-weight="{weight}" font-style="{style}" fill="{fill}">{esc(l)}</text>')
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
    a('<defs><marker id="ah" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#333"/></marker></defs>')
    a(f'<rect width="{W}" height="{H}" fill="#FFF"/>')
    pass  # title goes in the document caption
    for i, ln in enumerate(lanes):
        f, s, bg = LANE_STYLE[ln]
        a(f'<rect x="{i*LW}" y="{TOP}" width="{LW}" height="{H-TOP}" fill="{bg}" stroke="#888" stroke-width="1"/>')
        a(f'<rect x="{i*LW}" y="{TOP}" width="{LW}" height="{HEAD}" fill="{f}" stroke="#888" stroke-width="1"/>')
        text(i*LW + LW/2, TOP + HEAD/2, ln, 14, weight="bold")
    # edges first (under nodes)
    used_out = {(e[0], e[1]) for e in spec["edges"]}
    for e in spec["edges"]:
        src, ss, dst, ds = e[:4]; opt = e[4] if len(e) > 4 else {}
        if ds in "lr" and (dst, ds) in used_out and not opt.get("via"):
            ds = "t"   # side already used by an outgoing arrow: enter from the top instead
        p0, p1 = port(src, ss), port(dst, ds)
        pts = [p0]
        via = opt.get("via")
        if via:
            for v in via:
                vx = v[0] if not isinstance(v[0], tuple) else X(*v[0])
                vy = v[1] if not isinstance(v[1], tuple) else Y(*v[1])
                if vx is None: vx = pts[-1][0]
                if vy is None: vy = pts[-1][1]
                pts.append((vx, vy))
            last = pts[-1]
            if ds in "tb" and last[0] != p1[0]: pts.append((p1[0], last[1]))
            if ds in "lr" and last[1] != p1[1]: pts.append((last[0], p1[1]))
        else:
            v0 = ss in "tb"; v1 = ds in "tb"
            if v0 and v1 and p0[0] != p1[0]:
                my = opt.get("my") or (p0[1] + p1[1]) / 2; pts += [(p0[0], my), (p1[0], my)]
            elif not v0 and v1: pts.append((p1[0], p0[1]))
            elif v0 and not v1: pts.append((p0[0], p1[1]))
            elif not v0 and not v1 and p0[1] != p1[1]:
                mx = (p0[0] + p1[0]) / 2; pts += [(mx, p0[1]), (mx, p1[1])]
        pts.append(p1)
        d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        a(f'<path d="{d}" fill="none" stroke="#333" stroke-width="1.4" marker-end="url(#ah)"/>')
        if opt.get("label"):
            lx, ly = pts[0]; nx, ny = pts[1]
            if abs(nx - lx) > abs(ny - ly):   # horizontal first segment
                anchor = "start" if nx > lx else "end"
                text(lx + (8 if nx > lx else -8), ly - 11, opt["label"], 11.5, anchor, style="italic")
            else:
                text(lx + 7, ly + (14 if ny > ly else -14), opt["label"], 11.5, "start", style="italic")
    for k, (x, y, w, h, kind, lane, label) in geo.items():
        f, s, _ = LANE_STYLE[lane]
        if kind == "start":
            a(f'<circle cx="{x}" cy="{y}" r="12" fill="#222"/>')
        elif kind == "end":
            a(f'<circle cx="{x}" cy="{y}" r="14" fill="#FFF" stroke="#222" stroke-width="2"/><circle cx="{x}" cy="{y}" r="8" fill="#222"/>')
        elif kind == "act":
            a(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="14" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
            text(x, y, label)
        elif kind == "dec":
            a(f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" fill="#FFF" stroke="#444" stroke-width="1.6"/>')
            text(x, y, label, 12)
    a("</svg>")
    open(path, "w").write("\n".join(out))
