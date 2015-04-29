#!/bin/bash

python MRFileMapper.py -r local --conf-path mrjob.conf --file countvec_pickle.cpickle --file binary_classification_pickle.cpickle --file tfidf_pickle.cpickle --python-archive pythonarchive.tar.gz < ../cities.txt
