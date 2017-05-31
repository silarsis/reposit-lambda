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