##Supervised Learning Algorithm
These files scrub the data and run the supervised learning algorithm used to classify iPhones into 
their various model categories (4/4s/5/5c/etc.).

##Implementation  
The supervised learning classification was a two-step process: a machine learning classifier and regular expressions. The initial classification was binary (iPhone/not iPhone) using the Naive Bayes algorithm. Other supervised learning techniques were considered such as Logistic Regression and Support Vector Machines, but the Naive Bayes algorithm was chosen for its simplicity and transparency. The second step in the process is a regular expression waterfall where iPhones are classified based on various text patterns.

##Files  
* ``nbModel.py`` trains the Naive Bayes model and serializes the results into the cPickle files.

* ``fileScrubber.py`` scrubs the data for missing values, and re-formats fields where needed.

* ``predictor.py`` pulls in the pickled Naive Bayes model and determines if the posting is an iPhone or not.  

* ``classifier.py`` uses regular expressions to classify each iPhone by model type. 

* ``cleanData.py`` run the complete cleaning pipeline. It pulls data from S3, scrubs the data for missing values, and then calls the ``fileScrubber.py``, ``classifier.py`` and ``predictor.py`` scripts, one after another. The data is then stored back on S3.

* ``MRFileMapper.py`` is a map-only map/reduce script to clean the data.

##Run the Code
The shell script ``runMapper.sh`` calls the ``MRFileMapper.py`` script with the required arguments.
```
#!/bin/bash

python MRFileMapper.py -r local --conf-path mrjob.conf --file countvec_pickle.cpickle --file binary_classification_pickle.cpickle --file tfidf_pickle.cpickle --python-archive pythonarchive.tar.gz < ../data_collection/cities.txt
```

