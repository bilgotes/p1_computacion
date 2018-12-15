#!/bin/bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
mongoimport --db p1 --collection meneos --file meneos.json

(crontab -l 2>/dev/null; echo "*/2 * * * * $PWD/recolector.py") | crontab -
virtualenv .venv && source .venv/bin/activate && pip install -r requirements.txt
