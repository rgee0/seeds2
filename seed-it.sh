#!/bin/bash

cd /home/pi/code/seeds2/
python3 main.py

cd ./images

LATESTFILE=$(ls -t *.jpeg | head -1)
aws s3 cp ${LATESTFILE}  s3://growlab.technologee.co.uk/growlab.jpg