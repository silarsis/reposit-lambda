#!/bin/python
" Short script to upload zip to s3 "

import boto3

def bucket_name():
    " Should be dynamic, hard-coded for now - sorry future me "
    return "repositdeployer-buildresults-mivoklgovowv"

def upload():
    " Upload file to S3 "
    client = boto3.resource('s3')
    data = open('reposit.zip', 'rb')
    # No versioning - getting it up and running fast-ish
    client.Bucket(bucket_name()).put_object(Key='reposit.zip', Body=data)

if __name__ == '__main__':
    upload()
