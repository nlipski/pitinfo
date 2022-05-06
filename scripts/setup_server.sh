#!/bin/bash

sudo apt install -y libpq-dev
sudo apt install -y python3-virtualenv python3-pip
sudo apt install -y docker docker-compose

virtualenv venv
source venv/bin/activate

pip3 install -r requirements/production.txt

sudo gpasswd -a $USER docker
newgrp docker
