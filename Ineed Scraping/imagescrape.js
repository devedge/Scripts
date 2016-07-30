const request = require('request');
const mkdirp = require('mkdirp');
const ineed = require('ineed');
const fs = require('fs');

var url = 'https://github.com/devedge';


mkdirp.sync('Images');

// Run the image collector on the url
ineed.collect.images.from(url, function (err, response, result) {
    // body...
    if (err) { 
        console.log('ERROR: ' + err);
    } else {
        fetch_links(result);
    }
});


// Iterate over all the images and download them
function fetch_links(result) {
    result.images.forEach(function (imgstring) {
        console.log(imgstring.src);

        var name = imgstring.src.match('[^/]*$')[0]
                            .replace('&', '')
                            .replace('<', '')
                            .replace('>', '');


        request({
            uri: imgstring.src,
            encoding: null
        }, function (err, resp, data) {
            if (!err && resp.statusCode === 200) {

                fs.writeFile('Images/' + name, data, function (err) {
                    if (err) { console.log(err); }
                });

            } else {
                console.log('ERROR: ' + err);
            }
        });
        
    });
}















// var commandLineArgs = require('command-line-args');



// var cli = commandLineArgs(
//     {name: '-url', alias: 'u', type: String, multiple: false}
// );

// var options = cli.parse();


// if (options.url) {

// } else {
//     console.log('url needed');
// }
