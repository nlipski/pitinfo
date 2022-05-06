#!/bin/bash

cd ../
APPLICATION_CONFIG="production" python3 manage.py compose build
cd scripts