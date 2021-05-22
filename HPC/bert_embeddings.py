import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import pickle as pk
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 3:
        print('sorry not enough arguments')
        exit()
    input_file = args[0]
    output_file = args[1]
    output_file2 = args[2]

file = open(input_file, "r")
def get_data(file):
    lines = file.readlines()
    size = len(lines)
    if size == 1:
        return json.loads(lines[0])
    data = []
    for line in lines:
        data.append(json.loads(line))
    return data

data = get_data(file)
english_raw = pd.json_normalize(data)

print(english_raw.shape)
english_raw.head(10)


texts_column = english_raw.loc[:, "text"]
raw_texts = texts_column.values
raw_texts[0]


model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
embeddings = model.encode(raw_texts, show_progress_bar=True)


with open("outputs/"+output_file, "wb") as output_file:
    pk.dump(embeddings, output_file)

print("bert embeddings done")

umap_embeddings = umap.UMAP(n_neighbors=30,
                            n_components=5,
                            metric='cosine').fit_transform(embeddings)

with open("outputs/"+output_file2, "wb") as output_file:
    pk.dump(umap_embeddings, output_file2)

print("umap embeddings done")

# cluster = hdbscan.HDBSCAN(min_cluster_size=30,
#                           metric='euclidean',
#                           cluster_selection_method='eom').fit(umap_embeddings)
