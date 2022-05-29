from django.test import TestCase

# Create your tests here.
from scrapers.sample_scraper import lycos_search
from processors.clustering_algorithms import get_comm_clusters
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import pairwise_distances

import pandas as pd
import numpy as np

print("running query")
results = lycos_search("protect plants")
print("done pulling")
df = pd.DataFrame(results)
print("got results")
clusters,centroids = get_comm_clusters(df["description"].values.tolist())

