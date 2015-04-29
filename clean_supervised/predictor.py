import os
import pandas as pd
import cPickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

class Predictor():
    """ Predicts whether a certain title is a valid iphone listing or not,using a prior trained model."""
    def __init__(self, json_file):
        """
        :param list: a list of dictionaries as read in from a json file
        """ 
        self.data = pd.DataFrame.from_dict(json_file)
    
    def predict(self, removeNeg=True):
        """
        :return: The predicted pandas dataframe
        """
        #Load the pickled model components
        if not self.data.empty:
            try:
                with open('binary_classification_pickle.cpickle', 'rb') as f:
                    self.model = cPickle.load(f)

                with open('tfidf_pickle.cpickle', 'rb') as g:
                    self.tfidf = cPickle.load(g)

                with open('countvec_pickle.cpickle', 'rb') as h:
                    self.count_vec = cPickle.load(h)

            except IOError, e:
                print e
                print "error in predict"
                return None
        
        self.word_counts = self.count_vec.transform(self.data['title'].values)
        self.test_tfidf = self.tfidf.transform(self.word_counts)
        
        #Create predictions based on the model
        pred_bin = self.model.predict(self.test_tfidf)
        self.data['pred_bin'] = pred_bin
        
        return self.data
