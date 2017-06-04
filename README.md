# reposit-lambda
Lambda for Alexa Reposit skill

The [deployer](./deployer/) directory contains cloudformation for the
lambda-based build/deploy server (lambci, https://github.com/lambci/lambci).
Note, this is manually deployed as cloudformation, not automatic - consider
it a bootstrap.

The [reposit](./reposit/) directory contains the lambda handler, and is where
the deploy process installs all the libraries.

The [.lambci.json](./.lambci.json) file contains instructions for lambci.

The [build.sh](./build.sh) script is the build/deploy process.

The [deploy.js](./deploy.js) script deploys the code to Lambda. Used js because
the aws-sdk libs are available inside the lambci lambda.

To Do:

* grequests and pre-loading so we speed things up
* shorten the time period for the data we're requesting
* implement some way of others using this - credential cache + app