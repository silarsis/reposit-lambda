#!/bin/bash -ex

# pip install all the things
pip install git+https://github.com/silarsis/rp-python-client -t reposit
pip install grequests -t reposit
# zip up the dir
cd reposit && python -m zipfile -c ../reposit.zip . && cd ..
# push the zipped dir to S3
# ./upload.py
# deploy to the lambda
node ./deploy.js