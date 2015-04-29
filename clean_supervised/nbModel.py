import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import cPickle

#Load the data that has been manually classified
binary_train_data = pd.read_csv('training_sample_slimmed.csv')

#Count the categories, run TFIDF, and apply Naive Bayes algorithm
count_vec = CountVectorizer()
word_counts = count_vec.fit_transform(binary_train_data['title'].values)
tfidf = TfidfTransformer()
train_tfidf = tfidf.fit_transform(word_counts)
model = MultinomialNB().fit(train_tfidf, binary_train_data['bin_class'].values)

pred = model.predict(train_tfidf)
binary_train_data['pred'] = pred

#Pickle the model results to be used later
with open('binary_classification_pickle.cpickle', 'wb') as f:
    cPickle.dump(model, f)

with open('tfidf_pickle.cpickle', 'wb') as f:
    cPickle.dump(tfidf, f)

with open('countvec_pickle.cpickle', 'wb') as f:
    cPickle.dump(count_vec, f)

#Print the model results
with open('training_model_results.txt', 'wb') as f:
	f.write('The model was trained on {} observations.\n\n'.format(len(binary_train_data['bin_class'])))
	f.write('The model accurately predicts {}% of the training set.\n\n'.format(100 * round(np.mean(binary_train_data['bin_class'] == binary_train_data['pred']),3)))
	f.write(str(classification_report(binary_train_data['bin_class'], binary_train_data['pred'], target_names = ['Not an iPhone', 'iPhone'])))