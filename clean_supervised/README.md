##Supervised Learning Algorithm
These files scrub the data and run the supervised learning algorithm used to classify iPhones into 
their various model categories (4/4s/5/5c/etc.).

##Purpose


##Implementation  
The supervised learning classification was a two-step process: a machine learning classifier and regular expressions. The initial classification was binary (iPhone/not iPhone) using the Naive Bayes algorithm. Other supervised learning techniques were considered such as Logistic Regression and Support Vector Machines, but the Naive Bayes algorithm was chosen for its simplicity and transparency. The second step in the process is a regular expression waterfall where iPhones are classified based on various text patterns.

##Files  
* ``nbModel.py`` trains the Naive Bayes model and serializes the results into the cPickle files.  

* ``predictor.py`` pulls in the pickled Naive Bayes model and determines if the posting is an iPhone or not.  

* ``classifier.py`` uses regular expressions to classify each iPhone by model type. 

* ``cleanData.py`` pulls data from S3, scrubs the data for missing values, and re-formats fields where needed. It also calls the ``classifier.py`` and ``predictor.py`` scripts.

* ``MRFileMapper.py`` is a map-only map/reduce script to clean the data.

##Run the Code
ADD MORE
