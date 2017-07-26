# reposit-lambda
Lambda for Alexa Reposit skill

Swagger file at https://app.swaggerhub.com/apis/silarsis/repositpower/1.0.0

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

Notes:

I considered pre-caching the results of the requests to the API, but I'm not
convinced of the usefulness of that - in a vast number of ocassions, we won't
actually do both calls (battery and meter) anyway, we'll resolve via just the
battery lookup. Instead, I've restricted the time on the queries and used the
expiry cache.

To Do:

* shorten the time period for the data we're requesting
* implement some way of others using this - credential cache + app
