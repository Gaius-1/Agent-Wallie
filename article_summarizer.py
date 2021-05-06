from bs4 import BeautifulSoup
import re
import requests
import heapq
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords

# clean data by substituting numbers and, commas with a space " "
def clean(text):
    text = re.sub(r"\[[0-9]*\]"," ",text)
    text = text.lower()
    text = re.sub(r'\s+'," ",text)
    text = re.sub(r","," ",text)
    return text

def get_key(val):
    for key, value in val.items():
        if max(val.values()) == value:
            return key

def summarizer(vlink):
    # url = str(input("Paste the url\n"))
    url = vlink
    # change number of sentence needed in the summary
    num = 10
    # Client for placing web requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    res = requests.get(url,headers=headers)
    summary = ""
    soup = BeautifulSoup(res.text,'html.parser')
    content = soup.findAll("p")
    for text in content:
        summary +=text.text

    summary = clean(summary)

    print("Getting the data......\n")

    ## Tokenizing (spliting the whole text into smaller units)
    sent_tokens = sent_tokenize(summary)
    summary = re.sub(r"[^a-zA-z]"," ",summary)
    word_tokens = word_tokenize(summary)

    ## Removing Stop words
    word_frequency = {}
    trade_offs =  set(stopwords.words("english"))

    for word in word_tokens:
        if word not in trade_offs:
            if word not in word_frequency.keys():
                word_frequency[word]=1
            else:
                word_frequency[word] +=1

    ## Get words that occur most frequent and their frequency index(ratio)
    if word_frequency != {}:
        maximum_frequency = max(word_frequency.values())
    else:
        return ''

    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word]/maximum_frequency)

    # get the maximum frequency index
    sentences_score = {}
    for sentence in sent_tokens:
        for word in word_tokenize(sentence):
            if word in word_frequency.keys():
                if (len(sentence.split(" "))) < 30:
                    if sentence not in sentences_score.keys():
                        sentences_score[sentence] = word_frequency[word]
                    else:
                        sentences_score[sentence] += word_frequency[word]

    # get each sentence and it's frequency index
    key = get_key(sentences_score)

    # implement the heap queue algorithm for in-place sorting
    summary = heapq.nlargest(num,sentences_score,key=sentences_score.get)
    template = [clause.capitalize() for clause in summary]
    temporal_storage = []

    ## further clean data
    for tmp in template:
        if '“' in tmp[0]:
            tmp = tmp.replace('“', '"')
            tmp = tmp.split('"')
            tmp[1] = tmp[1].capitalize()
            tmp = '"'.join(tmp)

        temporal_storage.append(tmp)

    summary = " ".join(temporal_storage)
    # submit summary of article to telegram bot
    return summary
    # print(summary)


if __name__ == '__main__':
    main()
