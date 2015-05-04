__author__ = 'jason'
from subprocess import Popen, PIPE
import StringIO
import pandas as pd
import joblib
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer("[a-zA-Z]+")
def tokenize(x):
    return tokenizer.tokenize(x)

from classifier import nb, vectorizer, classify_tuple


class ReverbClassifier(object):
    def __init__(self, fname='reverb-latest.jar'):
        self.fname = fname

    def get_tuples(self, list_of_sentences):
        self.process = Popen(['java', '-jar', self.fname], stdin=PIPE, stdout=PIPE)
        self.data = StringIO.StringIO()
        out,error = self.process.communicate('\n'.join(list_of_sentences))
        self.data.write(out)
        self.data.seek(0)
        try:
            df = pd.read_csv(self.data, delimiter='\t', header=None, )
        except:
            yield "No relations extracted"
            return
        df.columns=[u'filename', u'sentence number', u'arg1', u'rel', u'arg2', u'arg1 start', u'arg1 end', u'rel start', u'rel end', u'arg2 start', u'arg2 end', u'conf', u'words', u'tags', u'chunks', u'a1norm', u'relnorm', u'a2norm']
        for id, row in df.iterrows():
            if classify_tuple([row['arg1']], [row['rel']], [row['arg2']]):
                yield (row['arg1'], row['rel'], row['arg2'], True)
            else:
                yield(row['arg1'], row['rel'], row['arg2'], False)
            #print(row['arg1'], row['rel'], row['arg2'])
            #print()
if __name__ == "__main__":
    f = ReverbClassifier()
    df = f.get_tuples(['I ate a buffalo chicken sandwich, mate.',
                       'I ate at Taco Bueno in Las Vegas.', 'I ate and then left.', 'I ate with my friend Jane Cookie.',
                       'I tried the Pulled Pork Nachos.',
                       'Worst food ever. Don\'t go here',
                       'I just had a glass of ice water.',
                       'John tried the Spicy Ahi Tuna Roll.'])
    f.get_tuples(["I really hope no one sees me here. I ate with my friend and he got sick. I ordered the Cowboy Chili Burger and it was fantastic. Really fantastic, actually. So fantastic I came back the same day and ordered another."])
    print(df)
