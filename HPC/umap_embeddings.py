import umap.umap_ as umap
import pickle as pk
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print('sorry not enough arguments')
        exit()
    input_file = args[0]
    output_file = args[1]

with open(input_file, "rb") as file:
    embeddings = pk.load(file)

umap_embeddings = umap.UMAP(n_neighbors=30,
                            n_components=5,
                            metric='cosine').fit_transform(embeddings)

with open(output_file, "wb") as umap_file:
    pk.dump(umap_embeddings, umap_file)