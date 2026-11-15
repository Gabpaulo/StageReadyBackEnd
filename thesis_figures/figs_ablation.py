"""Figure 4.12: RAG ablation on 30 recordings (data from stageready-backend eval_results)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2a78d6"; G1="#8a8984"; G2="#b9b8b2"; TP="#0b0b0b"; TS="#52514e"; GRID="#e6e5e0"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":G2,"axes.labelcolor":TS,
  "xtick.color":TS,"ytick.color":TS,"axes.spines.top":False,"axes.spines.right":False})
D=["speech_pace","pausing_fluency","loudness_control","pitch_variation","articulation_clarity","expressive_emphasis","filler_words"]
rows=[json.loads(l) for l in open("ablation/results.jsonl")]
mae={m:np.mean([np.mean([abs(float(r["pred"][d])-r["expert"][d]) for r in rows if r["mode"]==m and isinstance(r["pred"].get(d),(int,float))]) for d in D]) for m in ("none","corpus1","full")}
def winrate(path,c):
    p=json.load(open(path)); w=l=t=0
    for x in p["pairs"]:
        for i,v in enumerate([x["raw"][0].get(c),x["raw"][1].get(c)]):
            f=(v=="A") if i==0 else (v=="B"); o=(v=="B") if i==0 else (v=="A")
            w+=f; l+=o; t+=not(f or o)
    return w/(w+l+t), t/(w+l+t), l/(w+l+t)
fig,axs=plt.subplots(1,2,figsize=(11,3.9),gridspec_kw={"width_ratios":[1,1.25]}); fig.subplots_adjust(wspace=0.95,top=0.86)
ax=axs[0]; names=["No retrieval","Corpus 1 only","Full RAG"]; v=[mae["none"],mae["corpus1"],mae["full"]]
y=np.arange(3); ax.barh(y,v,color=[G1,G1,BLUE],height=0.55)
for i,x in enumerate(v): ax.text(x+0.01,i,f"{x:.3f}",va="center",fontsize=9,color=TP)
ax.axvline(0.696,color=TP,lw=1,ls="--"); ax.text(0.696,-0.62,"category average 0.696",fontsize=8.5,color=TP,ha="center")
ax.set_yticks(y,names); ax.invert_yaxis(); ax.set_xlim(0,1.05); ax.set_ylim(2.5,-0.9)
ax.set_xlabel("Score MAE vs. expert (1–5 scale, lower is better)",fontsize=8.5); ax.xaxis.grid(True,color=GRID); ax.set_axisbelow(True)
ax.set_title("LLM score error by condition",fontsize=10,color=TP,loc="left")
ax=axs[1]; items=[("vs. no retrieval: overall","ablation/pairwise_full_vs_none.json","overall"),
 ("vs. no retrieval: actionability","ablation/pairwise_full_vs_none.json","actionability"),
 ("vs. Corpus 1 only: overall","ablation/pairwise_full_vs_corpus1.json","overall"),
 ("vs. Corpus 1 only: actionability","ablation/pairwise_full_vs_corpus1.json","actionability")]
for i,(lab,p,c) in enumerate(items):
    w,t,l=winrate(p,c)
    ax.barh(i,w,color=BLUE,height=0.55); ax.barh(i,t,left=w,color="#d9d8d3",height=0.55); ax.barh(i,l,left=w+t,color=G1,height=0.55)
    ax.text(1.02,i,f"{(w+t/2)*100:.0f}%",va="center",fontsize=9,color=TP)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE,label="Full RAG better"),Patch(color="#d9d8d3",label="Tie"),Patch(color=G1,label="Other better")],frameon=False,fontsize=8.5,ncol=3,loc="upper left",bbox_to_anchor=(-0.02,-0.2))
ax.axvline(0.5,color=TP,lw=0.8,ls=":")
ax.set_yticks(range(4),[x[0] for x in items],fontsize=8.5); ax.invert_yaxis(); ax.set_xlim(0,1); ax.set_xticks([0,.25,.5,.75,1],["0%","25%","50%","75%","100%"])
ax.set_xlabel("Share of 60 blind judgements (30 speeches × 2 orders)",fontsize=8.5)
ax.set_title("Full RAG pairwise: wins / ties / losses (win rate, ties = ½)",fontsize=10,color=TP,loc="left")
fig.text(0.01,1.03,"RAG ablation on 30 real recordings",fontsize=12.5,color=TP,fontweight="bold")
fig.text(0.01,0.96,"Same transcript and metrics in every condition · generation and judge: gpt-4.1-mini",fontsize=9.5,color=TS)
fig.savefig("fig_rag_ablation_live.png",dpi=220,bbox_inches="tight",facecolor="white")
