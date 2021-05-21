from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import json
import pandas as pd
from tqdm import tqdm

threshold = 0.8
directory = './'
filename = 'englishSmall'
inputFile = f'{directory}{filename}.json'
outputFile = f'{directory}{filename}_clean.json'
data = []
with open(inputFile, "r") as f:
    print("Loading documents...")
    for line in tqdm(f):
        json_line = json.loads(line)
        json_line['text'] = json_line['text'].strip()
        data.append(json_line)

df = pd.json_normalize(data)
arr = list(df['text'])
count_vectorizer = CountVectorizer()
vector_matrix = count_vectorizer.fit_transform(arr)
cosine_similarity_matrix = cosine_similarity(vector_matrix)

to_delete = []
n = len(cosine_similarity_matrix)

print("Identifying similar documents...")
for i in tqdm(range(0, n)):
    for j in range(i+1, n):
        if cosine_similarity_matrix[i][j] > threshold:
            to_delete.append(j)

print(f'{len(to_delete)} similar docs were found')

print(f'Writing clean documents on {outputFile}...')
with open(outputFile, "w") as f:
    for i, line in tqdm(enumerate(data)):
        if i not in to_delete:
            json.dump(line, f)
            f.write('\n')
