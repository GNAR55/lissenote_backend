import torch
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from textblob import TextBlob
kw_model = KeyBERT()
vectorizer = KeyphraseCountVectorizer()

def get_keywords_v(text, correct=False, num=8):                #text = ["..."]
    """Returns keywords sorted in order of decreasing weight"""

    if correct:
        text = str(TextBlob(text).correct())

    res = kw_model.extract_keywords(docs=text, vectorizer=vectorizer, top_n=num)
    res.sort(key = lambda x: x[1], reverse=True)

    keywords = [word for (word, dist) in res]

    return(keywords)

if __name__=="__main__":
    doc = ['''I have yet to receive a response.  What is surprising is that the assistant manager 
    claimed that the article went through peer-review although there is no evidence that it actually did.  
    Anyone with English proficiency — with or without a degree in computer science — would recognize 
    that this manuscript makes absolutely no sense.  Had it gone through peer review, I should have 
    received reviewer comments.  If you are skeptical that I might be misreading the response of someone 
    whose first language is not English, I clarified the decision in a previous email with the simple question, 
    “Does this mean that our manuscript was accepted for publication?”''']
    
    keywords = get_keywords_v(doc)

    for word in keywords:
        print(word)