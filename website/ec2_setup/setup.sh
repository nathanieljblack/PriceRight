# initialize
sudo aptitude update
sudo aptitude safe-upgrade
sudo aptitude install build-essential
# install Nginx
sudo nginx=stable
sudo add-apt-repository ppa:nginx/$nginx
sudo apt-get update
sudo apt-get install nginx
# install Node Server
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get install nodejs
# install MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
# install Python (including Scrapy, boto, pymongo)
sudo apt-get install idle
sudo apt-get install python-pip python-dev
sudo pip install --upgrade pip 
sudo pip install --upgrade virtualenv 
sudo apt-get install -y libssl-dev libxml2-dev libxslt1-dev libssl-dev libffi-dev
sudo pip install Scrapy
sudo pip install boto
sudo pip install pymongo
sudo pip install python-dateutil
# Git
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install git
# pull repo from Github
cd /opt/
sudo mkdir app
sudo git clone https://github.com/maktrix16/w205_priceright.git app
# install node packages
cd /opt/app/website/public
sudo npm install --save
sudo npm install -g nodemon
# configure node to run 24x7 even when instance die
cd /opt/app/website/ec2_setup
sudo cp node-app.conf /etc/init/
sudo start node-app
# configure nginx and run it
sudo cp node-app /etc/nginx/sites-available/
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/node-app /etc/nginx/sites-enabled/node-app
sudo /etc/init.d/nginx restart
