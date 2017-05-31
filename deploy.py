#!/usr/bin/env python
" Deployer "

import boto3

def deploy():
    " Deploy direct to Lambda and publish "
    client = boto3.client('lambda')
    response = client.update_function_code(
        FunctionName='reposit',
        ZipFile=open('reposit.zip', 'rb').read(),
        Publish=True
    )
    print(response)

if __name__ == '__main__':
    deploy()
