
var fs = require('fs');
var AWS = require('aws-sdk');
var lambda = new AWS.Lambda();

var params = {
    FunctionName: "reposit", 
    Publish: true, 
    ZipFile: fs.readFileSync("reposit.zip")
};
lambda.updateFunctionCode(params, function(err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else     console.log(data);           // successful response
});