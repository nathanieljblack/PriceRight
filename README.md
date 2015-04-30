#Craigslist Price Comparison Tool

##Group Members
* Nate Black (nathaniel.j.black@gmail.com)
* Arthur Mak (arthur.t.mak@gmail.com)
* Malini Mittal (malini.mittal@gmail.com)
* Marguerite Oneto (marguerite@oneto.us)

##Project Overview
Craigslist is a classified advertisements website that was founded in the late 1990s. Over the past decade, the website has expanded to over 2,000 markets in 50 countries. The website rapidly gained popularity due to it’s low cost, ease of use, and user freedom. With services in housing, personal advertisements, jobs, for sale, and community, the website has a plethora of data. But sifting through that data can be extremely challenging due to the free-form nature of the website. 

Fair value is defined as the rational estimate of the market price for a good. But how does one obtain fair value? In particular, how does a user know an advertisement on Craigslist is fairly valued? People commonly, and often unknowingly, attempt to determine the fair value of a good by comparing prices across different markets and against historical prices. While Craigslist is wonderful for its low cost and ease of use, it is very difficult and time-consuming to use Craigslist as a price comparison tool. This project attempts to filter the massive corpus of Craigslist data into a human-readable summary of prices across various markets over time. 

The goal of this project is to produce a user-friendly application that provides a price comparison interface whenever a user conducts a search on a particular item. The website will be able to answer questions such as:  
* What is the fair market value of the item?  
* What is the trend of the price of the item per city?  
* What is the average price of the item across the country?  

A possible extension could be to create a Craigslist consumer price index (CPI) and see how its performance compares with the official Bureau of Labor Statistics (BLS) CPI.

##Data Processes and Instructions

###Acquiring and Storing Raw Data  
We use a Python script to scrape the data off of the Craigslist website.  The Python script is executed on a daily basis using Cronjob. Raw data from the data acquisition process is stored in Amazon S3’s key-value store. 

Please follow the Readme instructions in the [data_collection](https://github.com/maktrix16/w205_priceright/tree/master/data_collection) folder to replicate this process.

###Cleaning the Data and Storing It 
Once the data is acquired, it needs to be cleaned before we can use it in the live environment of web application. All the unwanted, unnecessary fields are removed. NLP techniques are used to match potentially different descriptions to the same item as well as to weed out unrelated items. Cleaned data is again stored in Amazon S3's key-value store. 

Please follow the Readme instructions in either the [clean_supervised](https://github.com/maktrix16/w205_priceright/tree/master/clean_supervised) or [clean_unsupervised](https://github.com/maktrix16/w205_priceright/tree/master/clean_unsupervised) folder to replicate this process using supervised or unsupervised NLP technique respectively. 

###Retrieving the Data  
After the data is acquired and properly cleaned by the Python scripts, there is a Python script to pass the data from Amazon S3 to MongoDB, which is used by our live web application. Our web application is a live website where the user can input item search parameters. The search parameters include product name, location, and a date range. Our choice of code stack for building the website is commonly known as the “MEAN” stack (MongoDB, Express.io, Angular.js, Node.js). This is a full stack where the server, database, and model-view-controller (MVC) framework can be setup such that we can have a live website that works with MongoDB. 

Please follow the Readme instructions in the [website](https://github.com/maktrix16/w205_priceright/tree/master/website) folder to replicate this process and setup the website.
