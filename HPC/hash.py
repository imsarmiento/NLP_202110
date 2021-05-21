import json
import pandas as pd
import re

data = []
inputFile = '../Stage2/datasets/english/englishV1.json'
dict_to_keep = {}
size = 0
with open(inputFile, "r") as f:
    lines = f.readlines()
    percentage = 0
    size = len(lines)
    index = 0
    prevEntero = 1
    for line in lines:
        json_line = json.loads(line)
        text = json_line['text'].strip()
        text = re.sub(r'[^0-9a-zA-Z]','', text)
        if text not in dict_to_keep:
            data.append(json_line)

        dict_to_keep[text] = True
        
        index += 1
        percentage = (index)*100/size
        if int(percentage) != prevEntero:
            print(str(int(percentage)) + '%')
            prevEntero = int(percentage)

df = pd.json_normalize(data)
print('size before:',size)
print('size after:', df.shape[0])
df.to_json('output1.json', orient='records')
