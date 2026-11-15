import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=json.load(open("results.json")); C2=json.load(open("c2.json"))
OUT="figs/"; import os; os.makedirs(OUT,exist_ok=True)
BLUE="#2a78d6"; ORANGE="#eb6834"; G1="#8a8984"; G2="#b9b8b2"; G3="#d9d8d3"
TP="#0b0b0b"; TS="#52514e"; GRID="#e6e5e0"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":G2,"axes.labelcolor":TS,
  "xtick.color":TS,"ytick.color":TS,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":False})
def fin(fig,name,title,sub):
    fig.text(0.01,1.06,title,ha="left",va="bottom",fontsize=12.5,color=TP,fontweight="bold")
    fig.text(0.01,1.005,sub,ha="left",va="bottom",fontsize=9.5,color=TS)
    fig.savefig(OUT+name,dpi=220,bbox_inches="tight",facecolor="white"); plt.close(fig)
S=["speechPace","pausing_fluency","loud_control","pitch_variation","articulation_clarity","expressive_emph","filler_words","overall"]
L=["Speech pace","Pausing/fluency","Loudness","Pitch variation","Articulation","Expressive emph.","Filler words","Overall"]

# Fig A: corpus composition
cats=["Informative","Motivational","Persuasive"]
o=[R["by_src"]["original"][c] for c in cats]; s=[R["by_src"]["synthetic"][c] for c in cats]
fig,ax=plt.subplots(figsize=(7,3.0)); fig.subplots_adjust(top=0.95)
y=np.arange(3)
ax.barh(y,o,color=BLUE,height=0.55,label="Original (expert-evaluated recording)",edgecolor="white",linewidth=2)
ax.barh(y,s,left=o,color=ORANGE,height=0.55,label="Synthetic (augmented row)",edgecolor="white",linewidth=2)
for i in range(3):
    ax.text(o[i]/2,i,str(o[i]),va="center",ha="center",color="white",fontsize=9,fontweight="bold")
    ax.text(o[i]+s[i]/2,i,str(s[i]),va="center",ha="center",color="white",fontsize=9,fontweight="bold")
    ax.text(o[i]+s[i]+0.6,i,f"{o[i]+s[i]} total",va="center",color=TS,fontsize=9)
ax.set_yticks(y,cats); ax.invert_yaxis(); ax.set_xlim(0,45); ax.set_xlabel("Speeches in Corpus 1")
ax.legend(loc="upper left",frameon=False,fontsize=8.5,bbox_to_anchor=(0,-0.28),ncol=2)
fin(fig,"fig_corpus1_composition.png","Corpus 1 composition by category and origin","speech_features_augmented.csv · 97 rows (57 original, 40 synthetic)")

# Fig B: with vs without retrieval, mean MAE, two panels
conds=[("knn","With retrieval: top-3 acoustic matches (RAG)",BLUE),
       ("top1","With retrieval: top-1 match only",BLUE),
       ("rand","Without: 3 random same-category speeches",G1),
       ("cat","Without: category mean score",G1),
       ("glob","Without: corpus mean score",G1),
       ("mid","Without: constant mid-scale (3.0)",G2)]
fig,axs=plt.subplots(1,2,figsize=(9.5,3.6),sharey=True); fig.subplots_adjust(top=0.92,wspace=0.08)
for ax,key,ttl in [(axs[0],"loo_all","Full corpus (n = 97)"),(axs[1],"loo_orig","Original recordings only (n = 57)")]:
    vals=[R[key][f"mae_{c}_mean"] for c,_,_ in conds]
    yy=np.arange(len(conds))
    ax.barh(yy,vals,color=[c for _,_,c in conds],height=0.6,alpha=1)
    ax.barh(yy[1:2],vals[1:2],color="white",height=0.6,hatch="////",edgecolor=BLUE,linewidth=0)
    for i,v in enumerate(vals): ax.text(v+0.015,i,f"{v:.2f}",va="center",fontsize=9,color=TP)
    ax.set_title(ttl,fontsize=10,color=TP,loc="left"); ax.set_xlim(0,1.3)
    ax.set_xlabel("Mean absolute error vs. expert score (1–5 scale, lower is better)",fontsize=8.5)
    ax.xaxis.grid(True,color=GRID); ax.set_axisbelow(True)
axs[0].set_yticks(np.arange(len(conds)),[n for _,n,_ in conds],fontsize=8.5); axs[0].invert_yaxis()
fin(fig,"fig_rag_vs_norag_mae.png","Score calibration with vs. without Corpus 1 retrieval",
    "Leave-one-out over Corpus 1 using the backend's retrieval (category filter, MinMax, cosine). Mean over 8 dimensions.")

# Fig C: per-dimension, kNN vs corpus mean, two panels
fig,axs=plt.subplots(1,2,figsize=(9.5,4.0),sharey=True); fig.subplots_adjust(top=0.82,wspace=0.08)
for ax,key,ttl in [(axs[0],"loo_all","Full corpus (n = 97)"),(axs[1],"loo_orig","Original recordings only (n = 57)")]:
    a=[R[key]["mae_knn"][d] for d in S]; b=[R[key]["mae_glob"][d] for d in S]
    yy=np.arange(len(S)); h=0.36
    ax.barh(yy-h/2-0.02,a,height=h,color=BLUE,label="With retrieval (top-3 RAG)")
    ax.barh(yy+h/2+0.02,b,height=h,color=G1,label="Without retrieval (corpus mean)")
    ax.set_title(ttl,fontsize=10,color=TP,loc="left"); ax.set_xlim(0,1.35)
    ax.xaxis.grid(True,color=GRID); ax.set_axisbelow(True); ax.set_xlabel("Mean absolute error (lower is better)",fontsize=8.5)
axs[0].set_yticks(np.arange(len(S)),L); axs[0].invert_yaxis()
axs[0].legend(frameon=False,fontsize=8.5,loc="lower left",bbox_to_anchor=(0,1.08),ncol=2)
fin(fig,"fig_rag_vs_norag_by_dimension.png","Per-dimension calibration error with vs. without retrieval","Leave-one-out over Corpus 1; expert scores on a 1–5 Likert scale")

# Fig D: similarity — top-1 vs average similarity
import pandas as pd
r=pd.read_csv("loo_all.csv")
fig,ax=plt.subplots(figsize=(7,3.2)); fig.subplots_adjust(top=0.95)
bins=np.linspace(0.5,1.0,26)
ax.hist([r.mean_sim,r.top1_sim],bins=bins,color=[G1,BLUE],label=["Mean similarity to every same-category speech","Similarity of the top-1 retrieved speech"],edgecolor="white",linewidth=0.8)
ax.set_xlabel("Cosine similarity (MinMax-scaled 7-feature vector)"); ax.set_ylabel("Query speeches")
ax.legend(frameon=False,fontsize=8.5,loc="upper left")
ax.text(r.top1_sim.mean(),ax.get_ylim()[1]*0.92,f"mean top-1 = {r.top1_sim.mean():.3f}",ha="right",fontsize=8.5,color=TP)
ax.text(r.mean_sim.mean(),ax.get_ylim()[1]*0.45,f"mean all = {r.mean_sim.mean():.3f}",ha="center",fontsize=8.5,color=TP)
fin(fig,"fig_corpus1_similarity.png","Corpus 1 retrieval similarity","Leave-one-out, n = 97 · cosine scores are high even for unrelated speeches, so similarity alone is not evidence of a good match")

# Fig E: Corpus 2 chunks per document
names={"The Art Of Public Speaking.pdf":"The Art of Public Speaking","HowToGiveASpeech_PDF_e-book.pdf":"How to Give a Speech (e-book)",
 "Guidelines.pdf":"Guidelines for Public Speaking (Gareis)","733-22ps-step-up-your-public-speaking-skills.pdf":"Step Up Your Public Speaking Skills",
 "GettingPastUmm.pdf":"Getting Past Umm","EvaluationFormToastmaster.pdf":"Toastmasters Evaluation Form","Suggestions-Avoiding-filler-words.pdf":"Suggestions: Avoiding Filler Words"}
items=sorted(C2.items(),key=lambda kv:-kv[1]["chunks"])
fig,ax=plt.subplots(figsize=(7,3.4)); fig.subplots_adjust(top=0.95)
yy=np.arange(len(items)); v=[x[1]["chunks"] for x in items]
ax.barh(yy,v,color=BLUE,height=0.6)
for i,x in enumerate(items): ax.text(v[i]+5,i,f'{v[i]}  ({x[1]["pages"]} pp.)',va="center",fontsize=8.5,color=TP)
ax.set_yticks(yy,[names[x[0]] for x in items],fontsize=8.5); ax.invert_yaxis(); ax.set_xlim(0,650)
ax.set_xlabel("Chunks stored in ChromaDB (300-word chunks)")
fin(fig,"fig_corpus2_chunks.png","Corpus 2 knowledge base: chunks per source document",f"7 PDFs · {sum(v)} chunks total · re-chunked with ingest.py's chunk_text()")

# Fig F: pitch_std range mismatch
fr=R["feature_range"]["pitch_std"]
fig,ax=plt.subplots(figsize=(7,2.2)); fig.subplots_adjust(top=0.95)
ax.barh([1],[fr["max"]-fr["min"]],left=[fr["min"]],color=BLUE,height=0.45)
ax.barh([0],[160],left=[0],color=ORANGE,height=0.45)
ax.text(fr["min"]-10,1,f'{fr["min"]:.0f}',ha="right",va="center",fontsize=8.5); ax.text(fr["max"]+10,1,f'{fr["max"]:.0f} Hz',va="center",fontsize=8.5)
ax.text(170,0,"max 160 Hz",va="center",fontsize=8.5)
ax.set_yticks([0,1],["Live recordings\n(main.py, 80–400 Hz search)","Corpus 1 rows\n(CSV)"],fontsize=8.5); ax.set_xlim(0,1400)
ax.set_xlabel("pitch_std (Hz)")
fin(fig,"fig_pitch_feature_range.png","pitch_std range: corpus vs. live feature extractor","Live values can never reach the corpus range, so this feature cannot match on equal terms")
