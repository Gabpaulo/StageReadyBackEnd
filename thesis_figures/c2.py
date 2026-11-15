import os,sys,json
from pypdf import PdfReader
P=sys.argv[1]; out={}
for f in sorted(os.listdir(P)):
    if not f.lower().endswith('.pdf'): continue
    try:
        r=PdfReader(os.path.join(P,f)); t=" ".join(p.extract_text() or "" for p in r.pages); pages=len(r.pages)
    except Exception as e: t="";pages=0
    w=t.split(); ch=[w[i:i+300] for i in range(0,len(w),300)]; ch=[c for c in ch if len(c)>=50]
    out[f]={"pages":pages,"words":len(w),"chunks":len(ch)}
print(json.dumps(out,indent=1)); print("total",sum(v["chunks"] for v in out.values()))
json.dump(out,open("c2.json","w"),indent=1)
