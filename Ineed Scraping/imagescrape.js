var ineed = require('ineed');



// Run the image collector on the url
ineed.collect.images.from('https://github.com/devedge', function (err, response, result) {
    // body...
    if (err) { 
        console.log('ERROR: ' + err) 
    } else {
        console.log(result);
    }
});



















// var commandLineArgs = require('command-line-args');



// var cli = commandLineArgs(
//     {name: '-url', alias: 'u', type: String, multiple: false}
// );

// var options = cli.parse();


// if (options.url) {

// } else {
//     console.log('url needed');
// }
