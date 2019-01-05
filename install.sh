#!/bin/bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo cp mongo_files/conf/mongod.conf /etc/mongod.conf
sudo chown $USER /etc/mongod.conf
sudo chown -R $USER /var/log/mongodb/
sudo chown -R $USER /var/lib/mongodb/
mongod --config /etc/mongod.conf
mongoimport --db p1 --collection meneos --file mongo_files/db/meneos.json
(crontab -l 2>/dev/null; echo "*/2 * * * * $PWD/recolector.py") | crontab -
sudo apt-get install python-pip
pip install -r requirements.txt
sudo apt-get install gunicorn
sed -i 's/$USER/'$USER'/g' meneawebapp.service
sed -i 's/$USER/'$USER'/g' mongod.service
sudo cp *.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable meneawebapp.service 
sudo systemctl enable mongod.service 
