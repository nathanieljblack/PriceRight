##Unsupervised Learning Algorithm
These files run the unsupervised learning algorithm used to classify iPhones into 
their various model categories (4/4s/5/5c/5s/6/6 Plus).

##Purpose
The purpose of the unsupervised learning algorithm is to make the classification 
process scalable once the price comparison tool is expanded to include items beyond 
the iPhone.  In such a case, it would be impractical to conduct supervised learning 
on each individual item.  Unsupervised learning can categorize postings without 
having to manually train the model.

##Implementation  
The unsupervised learning algorithm employs Latent Semantic Indexing (LSI) and 
    K-means clustering.

##Files  
The main module is cleanDataUnsupervised.py.  It imports classes from 
``fileScrubberByNate.py``, ``predictorUnsupervised.py`` and ``classifierUnsupervised.py``.  

The cities.txt file lists the cities from which the tool has scraped Craigslist 
data and is used by ``cleanDataUnsupervised.py``.

The ``runCleanData.sh`` shell script is used to run ``cleanDataUnsupervised.py`` on a 
daily basis.

The ``crontab.txt`` file was used to set up the cron job on the EC2 instance.

##Run the Code
To run the code, insert your AWS keys into the file ``awsAuthenticationW205.py``.  On the command line, 
type  
```
python cleanDataUnsupervised.py
```

This will clean the raw data that was pulled from Craigslist today and put it into the S3 folder
w205-price-comparison-tool/clean/unsupervised/<todays-date>.
