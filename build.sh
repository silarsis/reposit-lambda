#!/bin/bash

# pip install all the things
pip install git+https://github.com/silarsis/rp-python-client -t reposit
# zip up the dir
cd reposit && python -m zipfile -c ../reposit.zip . && cd ..
# push the zipped dir to S3
# deploy from S3 to the lambda