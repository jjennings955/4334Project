import joblib
import scipy.sparse
import os
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer

tokenizer = RegexpTokenizer("[a-zA-Z]+")
def tokenize(x):
    return tokenizer.tokenize(x)

class Vectorizer:
    def __init__(self, vectorizers=None):
        #self.tokenizer = RegexpTokenizer("[a-zA-Z]+")
        if vectorizers:
            self.arg1_vectorizer, self.rel_vectorizer, self.arg2_vectorizer = vectorizers
        else:
            self.arg2_vectorizer = CountVectorizer(binary=True, tokenizer=tokenize, stop_words=None, max_df=20000, min_df=5, lowercase=True)
            self.rel_vectorizer = CountVectorizer(binary=True, tokenizer=tokenize, stop_words=None, min_df=1000, lowercase=True)        
            self.arg1_vectorizer = CountVectorizer(binary=True, tokenizer=tokenize, stop_words=None, min_df=1000, lowercase=True)
    def fit(self, a1, rel, a2):
        self.arg1_vectorizer.fit(a1)
        self.arg2_vectorizer.fit(a2)
        self.rel_vectorizer.fit(rel)
    def transform(self, arg1, rel, arg2, stack=True):
        a2_feat = self.arg2_vectorizer.transform(arg2) # "arg2" features
        rel_feat = self.rel_vectorizer.transform(rel) # "rel" features
        a1_feat = self.arg1_vectorizer.transform(arg1) # "arg1" features
        result = (rel_feat, a1_feat, a2_feat)
        if stack:
            return scipy.sparse.hstack(result)
        return result


arg1 = joblib.load(os.path.join(os.getcwd(), 'classifiers', 'vectorizer_arg1.pkl'))
arg2 = joblib.load(os.path.join(os.getcwd(), 'classifiers', 'vectorizer_arg2.pkl'))
rel = joblib.load(os.path.join(os.getcwd(), 'classifiers', 'vectorizer_rel.pkl'))
vectorizer = Vectorizer(vectorizers=(arg1, rel, arg2))
nb = joblib.load('./classifiers/naive_bayes.pkl')

def classify_tuple(arg1, rel, arg2):
    features = vectorizer.transform(arg1, rel, arg2, stack=True)
    return nb.predict(features)[0]
