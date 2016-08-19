// A general-usage script that uses Ineed to list info from 
// a link (css links, js links, external links, etc)

const ineed = require('ineed');
const commandLineArgs = require('command-line-args');

const cli = [{name: 'url', alias: 'u', type: String, multiple: false}];
const options = commandLineArgs(cli);


function get(link) {
    ineed.collect.hyperlinks.from(link, function (error, response, result) {
        // console.log(result.hyperlinks);

        result.hyperlinks.forEach(function (string) {
            if (string.href.match('/src/[1-9-]*.')) {
                console.log(string.href);
            }
        });
    });
}


switch(options.url) {
    case undefined:
        console.log('specify a url');
        break;
    default:
        get(options.url);
}

