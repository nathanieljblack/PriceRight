## These files run the unsupervised learning algorithm used to classify iPhones into 
   their various model categories (4/4s/5/5c/5s/6/6 Plus).

##  The purpose of the unsupervised learning algorithm is to make the classification 
    process scalable once the price comparison tool is expanded to include items beyond 
    the iPhone.  In such a case, it would be impractical to conduct supervised learning 
    on each individual item.  Unsupervised learning can categorize postings without 
    having to manually train the model.

##  The unsupervised learning algorithm employs Latent Semantic Indexing (LSI) and 
    K-means clustering.

##  The main module is cleanDataUnsupervised.py.  It imports classes from 
    fileScrubberByNate.py, predictorUnsupervised.py and classifierUnsupervised.py.  

##  The cities.txt file lists the cities from which the tool has scraped Craigslist 
    data and is used by cleanDataUnsupervised.py.

##  The runCleanData.sh shell script is used to run cleanDataUnsupervised.py on a 
    daily basis.

##  The crontab.txt file was used to set up the cron job on the EC2 instance.