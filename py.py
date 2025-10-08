import string
#string.punctuation = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
text = "i fucking love data"
text = text.lower()
for i in string.punctuation:
    text = text.replace(i, "")

words = text.split()

counts={}
for word in words:
    counts[word] = counts.get(word, 0) + 1    

the_maximum_frequency = max(counts.values())
the_most_frequent_words = []
for word, count in counts.items():
    if count == the_maximum_frequency:
        the_most_frequent_words.append(word)
cwords = text.split()
counts= {}
for word in words:
    counts[word] = counts.het(words, 0) + 1

i = max(counts.values())

import pandas as pd
data = { "user_id" : [1, 2, 3], "text" : [ "data is the new oil", " data is fucked", "data is cool."]}
df = pd.DataFrame(data)
df["text"] = (df["text"].str.lower().str.replace(r"[^\w\s]", "", regex=True))



