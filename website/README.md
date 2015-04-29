# Data Retrieval (Website) #

## Step 0: Create new EC2 instance ##
Send us an email to request S3 and Github access so we add your AWS and Github credential to our access list.

## Step 1: Create new EC2 instance ##
Create a new EC2 instance (t2.micro type is ok). We used Ubuntu Server 14.04 LTS (HVM), SSD Volume Type, 64-bit. 

Setup a security group with the following attributes in your AWS console:
* Type = HTTP, Protocol = TCP, Port Range = 80, Source = 0.0.0.0/0
* Type = Custom TCP Rule, Protocol = TCP, Port Range = 3000, Source = 0.0.0.0/0

## Step 2: Setup Database and Website Components ##
Login to your new EC2 instance with your own keypair:

    ssh ubuntu@your_EC2_IP -i your_keypair_file

Download this file [setup.sh](https://github.com/maktrix16/w205_priceright/tree/master/website/ec2_setup/setup.sh) and copy it into the EC2 instance:

    scp -i w205_keypair.pem ~/your_path_to_downloaded_file/setup.sh ubuntu@52.5.39.120:

Inside your EC2 instance run the setup.sh script. Keep selecting "y" or "enter" when prompted. You will need to enter your Github account and password for private repository access during the setup:

    sh setup.sh

This setup.sh script would initialize and update the Ubuntu OS, install Nginx server, install Node server, install MongoDB, install Python and all needed libraries (such as boto and Pymongo), install Git, pull the website code from our private repository, install Node packages, and configure and start both Node and Nginx servers to ensure it runs 24x7 (even when server crashes the configuration would ensure servers keep respawning).

## Step 3: Load Database and Run ##
Open Mongo console by typing "mongo" in the command line and enter the following instructions to create database and collections inside MongoDB.

Use editor to edit a python script:

    sudo vi /opt/app/website/data/load_ubuntu/load.py

Modify the following line inside the file using your AWS credential and save the changes:

    conn = S3Connection('CHANGE_THIS_your_key_id','CHANGE_THIS_your_secret_access_key')

Load data into a database called 'w205project' from MongoDB by entering following command line input:

    python /opt/app/website/data/load_ubuntu/loadAll.py

Type your EC2 IP address in your web browser and the website should be up and running, ready for some serious data retrieval jobs! 

[Please use Chrome browser if you are accessing this site on your Desktop. Date selector does not work for Firefox or Safari on desktop due to HTML5 incompatibility issue. However, iPhone's Safari browser is ok.]
