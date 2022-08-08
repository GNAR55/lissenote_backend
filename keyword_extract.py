from ast import keyword
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from textblob import TextBlob

def get_keywords_v(doc, correct=False):                #doc = ["..."]
    kw_model = KeyBERT()
    vectorizer = KeyphraseCountVectorizer()

    if correct:
        for i in range(len(doc)):
            doc[i] = str(TextBlob(doc[i]).correct())

    res = kw_model.extract_keywords(docs=doc, vectorizer=vectorizer, top_n=8)

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