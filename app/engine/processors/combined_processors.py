from engine.processors.clustering_algorithms import cluster_sentences,get_st_embeddings
from engine.processors.tfidf import get_tfidf_mat,get_weighted_score
import pandas as pd
import numpy as np


def get_clustered_results(results):
    corpus_sentences = []
    for result in results:
        corpus_sentences.append(result["title"] +" "+ result["description"])
    sentence_clusters,_ = get_clustered_sentences(corpus_sentences)
    results = np.array(results)
    ordered_results = [results[np.where(sentence_clusters == i)] for i in np.unique(sentence_clusters)]
    return ordered_results

def get_result_dicts(ordered_results):
    results = ordered_results.copy()
    rows = []
    while sum([len(i) for i in results]) > 1:
        for e, a in enumerate(results):
            if len(a) > 0:
                row = a[-1]
                rows.append(row)
                results[e] = a[0:-1]
    return rows

def get_clustered_sentences(corpus_sentences):
    tf_embeddings,words = get_tfidf_mat(corpus_sentences)
    wv_embeddings = get_weighted_score(tf_embeddings,words)
    st_embeddings = get_st_embeddings(corpus_sentences)
    #print("TFIDF \n\n\n\n")
    #cidt,csit =cluster_sentences(corpus_sentences,tf_embeddings.todense())
    #print("WV \n\n\n\n")
    cidw,csiw =cluster_sentences(corpus_sentences,wv_embeddings)
    print("ST \n\n\n\n")
    cids,csis = cluster_sentences(corpus_sentences,st_embeddings)
    new_cid = cids.copy()
    new_cid[new_cid == -1] = cidw[new_cid == -1]+int(cids.max()+2)
    new_cid[new_cid == cids.max()+1] = -1
    new_csi = {k+int(cids.max()+2):v for k,v in csiw.items()}
    new_csi.update(csis)
    return new_cid,new_csi



if __name__ == '__main__':
    df = pd.read_csv("engine/processors/test.csv")
    corpus_sentences = df["title"]+ " "+df["description"]
    sentence_clusters,sentence_centroids = get_clustered_sentences(corpus_sentences)
    