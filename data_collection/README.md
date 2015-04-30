##Data Acquisition
Python web crawling framework Scrapy was chosen to scrape the website as it provides most of the fundamental needs of a crawler, along with various variables that can be set to customize the spider according to the needs of the project.    

##Implementation
There is one crawler per city. The decision to replicate code was mainly to keep the code simpler, to have the ability to run the spiders for different cities on different machines, and also to be able to run these spiders in a parallel manner, giving us the potential to scale up to many more cities/countries in the future.   
    
The main script is ``gatherData.py``.

###gatherData.py   
This script does the following main tasks:
* Takes in a list of cities as an input
* Run the scraper for each city
* Move all the scraped data to S3

##How to run
The shell script ``runScrapers.sh`` calls the ``gatherData.py`` script.  
```
#!/bin/bash

python gatherData.py cities.txt
```
    





