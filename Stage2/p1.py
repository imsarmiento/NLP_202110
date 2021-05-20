import json
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk
import ssl
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
import pickle as pk

prefix = "./datasets/"
english_path = prefix + "englishV1.json"

file = open(english_path, "r")
data = []
for line in file:
    data.append(json.loads(line))
english_raw = pd.json_normalize(data)

print(english_raw.shape)
english_raw.head(10)


texts_column = english_raw.loc[:, "text"]
raw_texts = texts_column.values
raw_texts[0]


model = SentenceTransformer("distilbert-base-nli-mean-tokens")
embeddings = model.encode(raw_texts, show_progress_bar=True)


print("finalized")

with open(r"./embeddings_en.pickle", "wb") as output_file:
    pk.dump(embeddings, output_file)


# umap_embeddings = umap.UMAP(n_neighbors=30,
#                             n_components=5,
#                             metric='cosine').fit_transform(embeddings)

# cluster = hdbscan.HDBSCAN(min_cluster_size=30,
#                           metric='euclidean',
#                           cluster_selection_method='eom').fit(umap_embeddings)
