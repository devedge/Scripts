
// downloads a webpage and formats everything into a single html document

// issue warning about images that are too large 


// workflow
// provide a url to the script when run
// get the html
// use 'ineed' to find all js, css, images (and fonts?, etc..)
// convert them all to data:uri format and embed it in the html
// minimize the html to reduce filesize a little
// save the html to disk


const fs = require('fs');
const request = require('request');

const ineed = require('ineed');
const mkdirp = require('mkdirp');
const Datauri = require('datauri');
const colors = require('colors/safe');
const srequest = require('sync-request');
const normalizeUrl = require('normalize-url');


var link = process.argv[2];

if (!link) {
    console.log(colors.red('ERR') + ' - A url must be passed in');
} else {

    link = normalizeUrl(link);
    console.log('Requesting ' + colors.green(link) + '...');
    request_root_page(link);
}


// Request the URL specified by the user
function request_root_page(link) {

    request({
        method: 'GET',
        uri: link,
        encoding: 'utf-8'/*,
        headers: {
            // add options to specify header options
        }*/
    }, function (err, resp, body) {
        if (err) {
            // Log error to console
            console.log(colors.red('ERR') + ' - ' + err);

        } else if (resp.statusCode !== 200) {
            // status code is not right, print error to console
            console.log(colors.red('ERR') + ' - ' + resp.statusCode + ' - ' + resp.statusMessage);

        } else {
            console.log('Embedding stylesheets, javascript, and images...');
            process_html(body);
        }
    });
}


// Embed the css, js (fonts?) and images into the html as datauri
function process_html(recv_html) {
    
    var res;
    var datauri;
    var itemlink;

    // blocking function that reprocesses all the elements in 'recv_html'
    // after this is finished, the html is saved on disk
    var html = ineed.reprocess.stylesheets(function (pageurl, hrefAttrValue) {

            // Process the css
            datauri = new Datauri();
            itemlink = resolve_shortlink(hrefAttrValue);

            console.log(colors.green('GET') + ' - ' + colors.green('(type: css): ') + itemlink);

            // synchronously request the css
            res = srequest('GET', itemlink);
            datauri.format('.css', res.body);

            // return the css as the datauri scheme
            return datauri.content;

        }).scripts(function (pageurl, srcAttrValue) {

            // Process the javascript
            datauri = new Datauri();
            itemlink = resolve_shortlink(srcAttrValue);

            console.log(colors.green('GET') + ' - ' + colors.green('(type: js): ') + itemlink);

            // synchronously request the js
            res = srequest('GET', itemlink);
            datauri.format('.js', res.body);

            // return the js as the datauri scheme
            return datauri.content;

        })/*.images(function (pageurl, srcAttrValue) {

            // Process the images
            itemlink = abs_url(url, srcAttrValue);

            var name = itemlink.match('[^/]*$')[0]
                            .replace('&', '')
                            .replace('<', '')
                            .replace('>', '');

            console.log('GET - (type: img): ' + itemlink);
            // console.log('             name: ' + name);

            request({
                method: 'GET',
                uri: itemlink,
                encoding: null,
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
                }
            }, function (err, resp, data) {
                if (!err && resp.statusCode === 200) {

                    fs.writeFile(home_folder + '/img/' + name, data, function (err) {
                        if (err) { console.log(err); }
                    });

                } else {
                    console.log('ERROR: ' + err);
                }
            });

            return filename + '/img/' + name;
        })*/.fromHtml(recv_html);


    // save the html with the filename
    fs.writeFileSync('index.html', html);

    console.log(colors.green('DONE') + ' - index.html');
}


// resolve a short link in the html source and append the root url if needed
function resolve_shortlink(shortlink) {
    var norm = normalizeUrl(shortlink);

    if (norm.match(/^\/[^\/]/)) {
        return link.match(/^https?:\/\/[^\/]*/)[0] + norm;
    } else {
        return norm;
    }
}


