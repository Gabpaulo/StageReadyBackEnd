import sys, time, json, os
import numpy as np, pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
CSV = sys.argv[1]
F = ["syllables_per_sec","pause_ratio","loud_mean","loud_std","pitch_std","spectral_centroid","spectral_flux"]
S = ["speechPace","pausing_fluency","loud_control","pitch_variation","articulation_clarity","expressive_emph","filler_words","overall"]
df = pd.read_csv(CSV).reset_index(drop=True)
out = {"n": len(df), "by_cat": df.category.value_counts().to_dict(),
       "by_src": df.groupby(["category","source"]).size().unstack(fill_value=0).to_dict()}
def loo(queries_mask, corpus_mask_fn, k=3):
    rows=[]
    for qi in df.index[queries_mask]:
        cmask = corpus_mask_fn(qi)
        corp = df[cmask]
        sc = MinMaxScaler().fit(corp[F])
        cat = df.at[qi,"category"]
        sub = corp[corp.category.str.lower()==cat.lower()]
        cv = sc.transform(sub[F]); qv = sc.transform(df.loc[[qi],F])
        sims = cosine_similarity(qv, cv)[0]
        top = sims.argsort()[-k:][::-1]
        knn = sub.iloc[top][S].mean()
        top1 = sub.iloc[top[0]][S]
        catmean = sub[S].mean(); glob = corp[S].mean()
        true = df.loc[qi,S]
        # random retrieval baseline: k random speeches from same category (avg over 50 draws)
        rng = np.random.default_rng(qi)
        rnd = np.mean([np.abs(sub.iloc[rng.choice(len(sub),k,replace=False)][S].mean()-true).values for _ in range(50)],axis=0)
        rows.append(dict(cat=cat, top1_sim=sims[top[0]], top3_sim=sims[top].mean(), mean_sim=sims.mean(),
            **{f"knn_{s}":abs(knn[s]-true[s]) for s in S},
            **{f"top1_{s}":abs(top1[s]-true[s]) for s in S},
            **{f"cat_{s}":abs(catmean[s]-true[s]) for s in S},
            **{f"glob_{s}":abs(glob[s]-true[s]) for s in S},
            **{f"mid_{s}":abs(3-true[s]) for s in S},
            **{f"rand_{s}":rnd[j] for j,s in enumerate(S)}))
    return pd.DataFrame(rows)
allq = loo(df.index>=0, lambda qi: df.index!=qi)
origq = loo(df.source=="original", lambda qi: (df.index!=qi)&(df.source=="original"))
def summ(r):
    d={}
    d["sim_by_cat"]=r.groupby("cat")[["top1_sim","top3_sim","mean_sim"]].mean().round(3).to_dict()
    d["sim_overall"]=r[["top1_sim","top3_sim","mean_sim"]].mean().round(3).to_dict()
    for m in ["knn","top1","cat","glob","mid","rand"]:
        d[f"mae_{m}"]={s: round(r[f"{m}_{s}"].mean(),3) for s in S}
        d[f"mae_{m}_mean"]=round(np.mean([r[f"{m}_{s}"].mean() for s in S]),3)
    d["top1_hist"]=pd.cut(r.top1_sim,[0,0.85,0.9,0.95,1.0001]).value_counts(normalize=True).sort_index().round(3).astype(float).to_dict()
    d["top1_hist"]={str(k):v for k,v in d["top1_hist"].items()}
    return d
out["loo_all"]=summ(allq); out["loo_orig"]=summ(origq)
allq.to_csv("loo_all.csv",index=False); origq.to_csv("loo_orig.csv",index=False)
# latency of retrieval as implemented (scaler pre-fitted)
sc=MinMaxScaler().fit(df[F]); dfs=df.copy(); dfs[F]=sc.transform(df[F])
ts=[]
for i in range(500):
    q=df.loc[[i%len(df)],F]; t=time.perf_counter()
    sub=dfs[dfs.category.str.lower()==df.at[i%len(df),"category"].lower()]
    s=cosine_similarity(sc.transform(pd.DataFrame(q).reindex(columns=F,fill_value=0)),sub[F].values)[0]; s.argsort()[-3:][::-1]
    ts.append((time.perf_counter()-t)*1000)
out["latency_ms"]={"mean":round(float(np.mean(ts)),3),"p95":round(float(np.percentile(ts,95)),3)}
out["score_dist"]=df[S].describe().round(2).to_dict()
out["feature_range"]=df[F].describe().round(3).to_dict()
json.dump(out,open("results.json","w"),indent=1,default=str)
print(json.dumps(out,indent=1,default=str))
