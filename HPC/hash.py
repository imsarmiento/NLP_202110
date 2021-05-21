import json
import re
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print('sorry not enough arguments')
        exit()
    input_file = args[0]
    output_file = args[1]

data = []
dict_to_keep = {}
size = 0
with open(input_file, "r") as f:
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

print('size before:',size)
print('size after:', len(data))
with open(output_file, 'w') as f:
    for line in data:
        json.dump(line, f)
        f.write('\n')
