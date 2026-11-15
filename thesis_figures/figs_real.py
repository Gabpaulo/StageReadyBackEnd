import json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
R=json.load(open("results.json")); OUT="figs/"; import os; os.makedirs(OUT,exist_ok=True)
BLUE="#2a78d6"; ORANGE="#eb6834"; GREEN="#2e9e6a"; G1="#8a8984"; G2="#b9b8b2"; TP="#0b0b0b"; TS="#52514e"; GRID="#e6e5e0"
CATC={"Informative":BLUE,"Motivational":ORANGE,"Persuasive":GREEN}
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":G2,"axes.labelcolor":TS,
  "xtick.color":TS,"ytick.color":TS,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":False})
SEQ=LinearSegmentedColormap.from_list("seq",["#f7f6f2","#bcd6f2","#5b9be0","#1f5fb0","#0d2f63"])
DIV=LinearSegmentedColormap.from_list("div",["#b8461f","#eb9a78","#f2f1ed","#86b3e8","#1f5fb0"])
def fin(fig,name,title,sub):
    fig.text(0.01,1.06,title,ha="left",va="bottom",fontsize=12.5,color=TP,fontweight="bold")
    fig.text(0.01,1.005,sub,ha="left",va="bottom",fontsize=9.5,color=TS)
    fig.savefig(OUT+name,dpi=220,bbox_inches="tight",facecolor="white"); plt.close(fig)
S=["speechPace","pausing_fluency","loud_control","pitch_variation","articulation_clarity","expressive_emph","filler_words","overall"]
L=["Speech pace","Pausing/fluency","Loudness","Pitch variation","Articulation","Expressive emph.","Filler words","Overall"]
F=["syllables_per_sec","pause_ratio","loud_mean","loud_std","pitch_std","spectral_centroid","spectral_flux"]
FL=["Syllables/sec","Pause ratio","Loudness mean","Loudness SD","Pitch SD","Spectral centroid","Spectral flux"]
cats=["Informative","Motivational","Persuasive"]
df=pd.read_csv("../sheet/speech_features_real.csv")
df["batch"]=np.where(df.file.str.match(r'^[imp]2\.\d+\.mp3$'),"second","first")
N=len(df)

# Fig 3.1 composition
o=[int(((df.category==c)&(df.batch=="first")).sum()) for c in cats]; s=[int(((df.category==c)&(df.batch=="second")).sum()) for c in cats]
fig,ax=plt.subplots(figsize=(7,3.0)); y=np.arange(3)
ax.barh(y,o,color=BLUE,height=0.55,label="First collection (i1–p18)",edgecolor="white",linewidth=2)
ax.barh(y,s,left=o,color="#7fb0ea",height=0.55,label="Second collection (i2.x, m2.x, p2.x)",edgecolor="white",linewidth=2)
for i in range(3):
    ax.text(o[i]/2,i,str(o[i]),va="center",ha="center",color="white",fontsize=9,fontweight="bold")
    ax.text(o[i]+s[i]/2,i,str(s[i]),va="center",ha="center",color=TP,fontsize=9,fontweight="bold")
    ax.text(o[i]+s[i]+0.8,i,f"{o[i]+s[i]} total",va="center",color=TS,fontsize=9)
ax.set_yticks(y,cats); ax.invert_yaxis(); ax.set_xlim(0,62); ax.set_xlabel("Expert-scored speeches in Corpus 1")
ax.legend(loc="upper left",frameon=False,fontsize=8.5,bbox_to_anchor=(0,-0.28),ncol=2)
fin(fig,"fig_corpus1_composition.png","Corpus 1 composition by category and collection",f"speech_features_real.csv · {N} real expert-scored speeches, no synthetic rows")

# Fig 4.1 similarity hist
r=pd.read_csv("loo_all.csv")
fig,ax=plt.subplots(figsize=(7,3.2)); bins=np.linspace(0.5,1.0,26)
ax.hist([r.mean_sim,r.top1_sim],bins=bins,color=[G1,BLUE],label=["Mean similarity to every same-category speech","Similarity of the top-1 retrieved speech"],edgecolor="white",linewidth=0.8)
ax.set_xlabel("Cosine similarity (MinMax-scaled 7-feature vector)"); ax.set_ylabel("Query speeches")
ax.legend(frameon=False,fontsize=8.5,loc="upper left")
ax.text(r.top1_sim.mean(),ax.get_ylim()[1]*0.92,f"mean top-1 = {r.top1_sim.mean():.3f}",ha="right",fontsize=8.5,color=TP)
ax.text(r.mean_sim.mean(),ax.get_ylim()[1]*0.45,f"mean all = {r.mean_sim.mean():.3f}",ha="center",fontsize=8.5,color=TP)
fin(fig,"fig_corpus1_similarity.png","Corpus 1 retrieval similarity",f"Leave-one-out, n = {N} · cosine scores are high even for unrelated speeches, so similarity alone is not evidence of a good match")

# Fig 4.2 MAE
conds=[("knn","With retrieval: top-3 acoustic matches (RAG)",BLUE),("top1","With retrieval: top-1 match only",BLUE),
       ("rand","Without: 3 random same-category speeches",G1),("cat","Without: category mean score",G1),
       ("glob","Without: corpus mean score",G1),("mid","Without: constant mid-scale (3.0)",G2)]
vals=[R["loo_all"][f"mae_{c}_mean"] for c,_,_ in conds]
fig,ax=plt.subplots(figsize=(7.5,3.4)); yy=np.arange(len(conds))
ax.barh(yy,vals,color=[c for _,_,c in conds],height=0.6)
ax.barh(yy[1:2],vals[1:2],color="white",height=0.6,hatch="////",edgecolor=BLUE,linewidth=0)
for i,v in enumerate(vals): ax.text(v+0.015,i,f"{v:.2f}",va="center",fontsize=9,color=TP)
ax.set_yticks(yy,[n for _,n,_ in conds],fontsize=8.5); ax.invert_yaxis(); ax.set_xlim(0,1.2)
ax.set_xlabel("Mean absolute error vs. expert score (1–5 scale, lower is better)",fontsize=8.5)
ax.xaxis.grid(True,color=GRID); ax.set_axisbelow(True)
fin(fig,"fig_rag_vs_norag_mae.png","Score calibration with vs. without Corpus 1 retrieval",
    f"Leave-one-out over {N} real speeches using the backend's retrieval (category filter, MinMax, cosine). Mean over 8 dimensions.")

# Fig 4.3 per-dimension: knn vs category mean
a=[R["loo_all"]["mae_knn"][d] for d in S]; b=[R["loo_all"]["mae_cat"][d] for d in S]
fig,ax=plt.subplots(figsize=(7.5,4.0)); yy=np.arange(len(S)); h=0.36
ax.barh(yy-h/2-0.02,a,height=h,color=BLUE,label="With retrieval (top-3 RAG)")
ax.barh(yy+h/2+0.02,b,height=h,color=G1,label="Without retrieval (category mean)")
ax.set_yticks(yy,L); ax.invert_yaxis(); ax.set_xlim(0,1.3)
ax.xaxis.grid(True,color=GRID); ax.set_axisbelow(True); ax.set_xlabel("Mean absolute error (lower is better)",fontsize=8.5)
ax.legend(frameon=False,fontsize=8.5,loc="lower left",bbox_to_anchor=(0,1.0),ncol=2)
fin(fig,"fig_rag_vs_norag_by_dimension.png","Per-dimension calibration error with vs. without retrieval",f"Leave-one-out over {N} real speeches; expert scores on a 1–5 Likert scale")

# Fig 4.4 pitch range
mn,mx=df.pitch_std.min(),df.pitch_std.max()
fig,ax=plt.subplots(figsize=(7,2.2))
ax.barh([1],[mx-mn],left=[mn],color=BLUE,height=0.45); ax.barh([0],[160],left=[0],color=ORANGE,height=0.45)
ax.text(mn-10,1,f'{mn:.0f}',ha="right",va="center",fontsize=8.5); ax.text(mx+10,1,f'{mx:.0f} Hz',va="center",fontsize=8.5)
ax.text(170,0,"max 160 Hz",va="center",fontsize=8.5)
ax.set_yticks([0,1],["Live recordings\n(main.py, 80–400 Hz search)","Corpus 1 rows\n(CSV)"],fontsize=8.5); ax.set_xlim(0,1400)
ax.set_xlabel("pitch_std (Hz)")
fin(fig,"fig_pitch_feature_range.png","pitch_std range: corpus vs. live feature extractor","Live values can never reach the corpus range, so this feature cannot match on equal terms")

# Corpus 1 vector figures
df["c"]=pd.Categorical(df.category,cats); d2=df.sort_values(["c","batch"],kind="stable").reset_index(drop=True)
X=MinMaxScaler().fit_transform(d2[F]); bounds=[0]+list(np.cumsum([sum(d2.category==c) for c in cats]))
fig=plt.figure(figsize=(7.5,8.2)); gs=fig.add_gridspec(1,3,width_ratios=[0.25,0.25,7],wspace=0.04)
a0=fig.add_subplot(gs[0]); a1=fig.add_subplot(gs[1]); ax=fig.add_subplot(gs[2])
a0.imshow(d2.c.cat.codes.values[:,None],aspect="auto",cmap=ListedColormap([CATC[c] for c in cats]),interpolation="nearest")
a1.imshow((d2.batch=="second").astype(int).values[:,None],aspect="auto",cmap=ListedColormap(["#3a3936","#d9d8d3"]),interpolation="nearest")
for a_,t in [(a0,"Category"),(a1,"Collection")]:
    a_.set_xticks([]); a_.set_yticks([]); [x.set_visible(False) for x in a_.spines.values()]; a_.set_title(t,fontsize=7.5,rotation=90,color=TS,va="bottom")
a0.set_yticks([(bounds[i]+bounds[i+1])/2 for i in range(3)],cats,fontsize=9)
im=ax.imshow(X,aspect="auto",cmap=SEQ,vmin=0,vmax=1,interpolation="nearest")
for b_ in bounds[1:-1]: ax.axhline(b_-0.5,color="white",lw=2.5)
ax.set_yticks([]); ax.set_xticks(range(7),FL,rotation=35,ha="right",fontsize=9); [x.set_visible(False) for x in ax.spines.values()]
cb=fig.colorbar(im,ax=ax,fraction=0.04,pad=0.02); cb.set_label("MinMax-scaled value (0–1)",fontsize=8.5); cb.outline.set_visible(False)
fig.text(0.13,-0.03,"Collection strip: dark = first collection, light = second collection",fontsize=8,color=TS)
fin(fig,"fig_c1_vector_heatmap.png",f"Corpus 1 as stored vectors: {N} speeches × 7 acoustic features","Each row is one speech's retrieval vector after MinMax scaling, grouped by category (the retrieval filter)")

Sm=cosine_similarity(X)
fig,ax=plt.subplots(figsize=(7,6.2))
im=ax.imshow(Sm,cmap=SEQ,vmin=0,vmax=1,interpolation="nearest")
for b_ in bounds[1:-1]: ax.axhline(b_-0.5,color="white",lw=2); ax.axvline(b_-0.5,color="white",lw=2)
tk=[(bounds[i]+bounds[i+1])/2 for i in range(3)]
ax.set_xticks(tk,cats); ax.set_yticks(tk,cats,rotation=90,va="center"); [x.set_visible(False) for x in ax.spines.values()]
cb=fig.colorbar(im,ax=ax,fraction=0.046,pad=0.03); cb.set_label("Cosine similarity",fontsize=8.5); cb.outline.set_visible(False)
w=[Sm[bounds[i]:bounds[i+1],bounds[i]:bounds[i+1]][~np.eye(bounds[i+1]-bounds[i],dtype=bool)].mean() for i in range(3)]
allm=Sm[~np.eye(len(Sm),dtype=bool)].mean()
fin(fig,"fig_c1_similarity_matrix.png","Pairwise cosine similarity between all Corpus 1 vectors",
    f"{N} × {N} · mean within-category {np.mean(w):.2f}, mean overall {allm:.2f} · retrieval only compares inside a diagonal block")

p=PCA(2).fit(X); Z=p.transform(X)
fig,ax=plt.subplots(figsize=(7,5))
for c in cats:
    for bt,mk in [("first","o"),("second","^")]:
        m=((d2.category==c)&(d2.batch==bt)).values
        ax.scatter(Z[m,0],Z[m,1],s=42,marker=mk,color=CATC[c] if bt=="first" else "white",edgecolor=CATC[c],linewidth=1.5,label=f"{c} · {bt} collection",zorder=3)
ax.set_xlabel(f"Principal component 1 ({p.explained_variance_ratio_[0]*100:.0f}% of variance)")
ax.set_ylabel(f"Principal component 2 ({p.explained_variance_ratio_[1]*100:.0f}%)")
ax.grid(True,color=GRID); ax.set_axisbelow(True)
ax.legend(frameon=False,fontsize=8,ncol=3,loc="upper left",bbox_to_anchor=(0,-0.13))
fin(fig,"fig_c1_pca_map.png","Corpus 1 vector space projected to two dimensions (PCA)","Filled = first collection, hollow = second collection · the three categories overlap almost completely")

Cr=np.array([[np.corrcoef(df[f],df[s_])[0,1] for s_ in S] for f in F])
fig,ax=plt.subplots(figsize=(8,4.6))
im=ax.imshow(Cr,cmap=DIV,vmin=-0.6,vmax=0.6)
for i in range(7):
    for j in range(8):
        v=Cr[i,j]; ax.text(j,i,f"{v:+.2f}",ha="center",va="center",fontsize=8,color="white" if abs(v)>0.4 else TP)
ax.set_xticks(range(8),L,rotation=35,ha="right",fontsize=9); ax.set_yticks(range(7),FL,fontsize=9); [x.set_visible(False) for x in ax.spines.values()]
cb=fig.colorbar(im,ax=ax,fraction=0.035,pad=0.02); cb.set_label("Pearson r",fontsize=8.5); cb.outline.set_visible(False)
fin(fig,"fig_c1_feature_score_corr.png","How each retrieval feature relates to each expert score",f"Pearson correlation over {N} real speeches · all values are weak, so no single feature predicts a score")
json.dump({"within":w,"all":float(allm),"pca":p.explained_variance_ratio_.tolist(),"corr":Cr.tolist(),"comp":dict(first=o,second=s),
  "means_by_batch":df.groupby("batch")[F].apply(lambda g: pd.Series(MinMaxScaler().fit(df[F]).transform(g[F]).mean(0),index=F)).round(2).to_dict()},open("fres.json","w"),indent=1)
