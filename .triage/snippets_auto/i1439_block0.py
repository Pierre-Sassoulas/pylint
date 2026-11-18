from sklearn.feature_extraction.text import TfidfVectorizer

def average_tfidf(sents):
    vec = TfidfVectorizer()
    # convert raw text to scipy sparse matrix (csr) of tfidf values
    word_tfidf = vec.fit_transform(sents)
    result = []
    for sent in word_tfidf:
        avg = sent.sum() / sent.getnnz()
        result.append(avg)
    return result
