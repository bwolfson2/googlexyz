from sentence_transformers import SentenceTransformer,util
import torch
import numpy as np
import string
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

def decorator_func(model_type):
    print(model_type)

    def inner(func):
        print(model_type)
        print(f"instantiating {model_type} models")
        model = SentenceTransformer(
            "t5-base"
        )  # ("all-MiniLM-L6-v2")
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model.to(device)
        def wrapper(*args, **kwargs):
            return func(*args, model=model, **kwargs)

        return wrapper

    return inner

@decorator_func("embedding")
def get_st_embeddings(corpus_sentences, model):
    corpus_embeddings = model.encode(
        corpus_sentences,
        show_progress_bar=False,
        convert_to_tensor=True,
    )
    print(corpus_embeddings.shape)
    return corpus_embeddings.cpu().detach().numpy()



def get_comm_clusters(corpus_embeddings,min_size=2):
    candidate_clusters = []
    candidate_thresholds = np.arange(0.9, 0.4, -0.05)
    for i in candidate_thresholds:
        clusters = util.community_detection(
            corpus_embeddings, min_community_size=min_size, threshold=i
        )
        candidate_clusters.append(clusters)
    cluster_lens = []
    for candidate_cluster in candidate_clusters:
        flat_list = [item for sublist in candidate_cluster for item in sublist]
        # outliers can't be too dominant
        if len(candidate_cluster) > 25:
            cluster_lens.append(0)
            continue
        # the first cluster mus have at least 70% of the results
        if len(flat_list) < len(corpus_embeddings) * 0.5:
            cluster_lens.append(0)
            continue
        else:
            cluster_lens.append(len(candidate_cluster))
    max_idx = np.argmax(cluster_lens)
    print(f"Cutoff: {str(candidate_thresholds[max_idx])}")
    best_clusters = candidate_clusters[max_idx]
    flat_best = [item for sublist in best_clusters for item in sublist]
    coverage = len(flat_best) / len(corpus_embeddings)
    print(f"Coverage =  {coverage}")
    print(f"# of clusters: {len(best_clusters)}")
    clusters_by_id = np.ones(len(corpus_embeddings)) * -1
    for i, clusts in enumerate(best_clusters):
        clusters_by_id[clusts] = i
    centroid_sentences_ids = {e: i[0] for e, i in enumerate(best_clusters)}
    return clusters_by_id, centroid_sentences_ids

def cluster_sentences(corpus_sentences,corpus_embeddings=[]):
    if len(corpus_embeddings) < 1:
        corpus_embeddings = get_st_embeddings(corpus_sentences)
    clusters_by_id,centroid_sentences_ids = get_comm_clusters(corpus_embeddings)
    clusters,counts = np.unique(clusters_by_id,return_counts=True)
    clusters = clusters[np.flip(np.argsort(counts))]
    for i, cluster in enumerate(clusters):
        print(f"\nCluster {i+1}, #{(clusters_by_id == cluster).sum()} Elements ")
        if cluster == -1:
            continue
        print("\t", corpus_sentences[centroid_sentences_ids[cluster]])
    return clusters_by_id, centroid_sentences_ids





