#counting how many times a word appears in a sentence
sentence = 'how many hows are in the how sentence'
words = sentence.split()
counts = {}

for word in words :
    counts[word] = counts.get(word, 0) + 1
print(counts)









sentence = ""
words = sentence.split()
counts = {}

for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
print(counts)


def count_word_in_sentence(sentence: str, word_str):
    count = 0
    list_of_words = sentence.split(" ")
    for word in list_of_words:
        if word == word_str:
            count += 1
    return count



import pandas as pd

df = pd.read_csv("sdsadd.csv", encoding = "iso-88")
df[:3]
df['hdndf']
df[['one', 'two']][:10]
#the most common ... type:
j= df['column'].value_counts()
j[:10]

is_noise = df['Complaint Type'] == "Noise - Street/Sidewalk"
in_brooklyn = df['Borough'] == "BROOKLYN"
df[is_noise & in_brooklyn][:5]
#if we only want a few columns:
df[is_noise & in_brooklyn][['Complaint Type', 'Borough', 'Created Date', 'Descriptor']][:10]
