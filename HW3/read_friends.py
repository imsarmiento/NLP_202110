from os import error, replace, walk
import re
import csv

f = []
f.append(["raw_character_text", "spoken_words"])
for (dirpath, dirnames, filenames) in walk("./datasets/friends_dataset"):
    # print(filenames)
    for filename in filenames:
        print(filename)
        with open(dirpath + "/" + filename, encoding="utf8", errors="ignore") as dialog:
            for line in dialog:
                res = re.search("^\w+:", line)
                # print(res)
                if res is not None and (
                    line.startswith("Ross:")
                    or line.startswith("Rachel:")
                    or line.startswith("Phoebe:")
                    or line.startswith("Chandler:")
                    or line.startswith("Joey:")
                    or line.startswith("Monica:")
                ):
                    try:
                        index = res.span()[1]
                        line_delimited = [line[:index], line[index:]]
                        # print(line_delimited)
                        f.append(line_delimited)
                    except:
                        pass
        # break
    break

with open("./docs/dialogs_friends_filter.csv", "w") as filter_dialog:
    writer = csv.writer(
        filter_dialog, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL
    )
    writer.writerows(f)
