#!/usr/bin/env node

// - downloads a webpage and formats everything into a single html document
// - issue warning about images that are too large 
// - as a safety measure, only downloads scripts from the original base url

// workflow
// provide a url to the script when run
// get the html
// minimize the html to reduce filesize a little
// use 'ineed' to find all js, css, images (and fonts?, etc..)
// convert them all to data:uri format and embed it in the html
// save the html to disk


const fs = require('fs');
const request = require('request');

const ineed = require('ineed');
const mkdirp = require('mkdirp');
const Datauri = require('datauri');
const Minimize = require('minimize');
const colors = require('colors/safe');
const srequest = require('sync-request');
const normalizeUrl = require('normalize-url');
const sanitize = require('sanitize-filename');

var baseurl;

// The only argument required is the url
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
            baseurl = link.match(/https?:\/\/[^\/]*/)[0].replace('https:\/\/', '').replace('http:\/\/', '');

            console.log('Embedding stylesheets, javascript, and images...');
            process_html(body);
        }
    });
}


// Minimize the html and embed the css, js (fonts?) and images into the html as datauri
function process_html(recv_html) {

    // Extract the page title for the filename and sanitize it
    var filename = sanitize(ineed.collect.title.fromHtml(recv_html).title.substr(0,41));
    
    // minimize the html (before maximizing its size with the datauri)
    var content = new Minimize().parse(recv_html);
    
    var ext;
    var res;
    var datauri;
    var itemlink;

    // blocking function that reprocesses all the elements from the minimized html
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


            if (baseurl !== itemlink.match(/https?:\/\/[^\/]*/)[0].replace('https:\/\/', '').replace('http:\/\/', '')) {
                return '';
            }

            console.log(colors.green('GET') + ' - ' + colors.green('(type: js): ') + itemlink);

            // synchronously request the js
            res = srequest('GET', itemlink);
            datauri.format('.js', res.body);

            // return the js as the datauri scheme
            return datauri.content;


        }).images(function (pageurl, srcAttrValue) {

            // Process the image
            datauri = new Datauri();
            itemlink = resolve_shortlink(srcAttrValue);

            console.log(colors.green('GET') + ' - ' + colors.green('(type: img): ') + itemlink);

            // synchronously request the image
            res = srequest('GET', itemlink);

            if (res.body.length > 500000) {
                // warn that the image is too large, hasn't been downloaded, and return immediately
                console.log(colors.red('WARN') + ' - Image too large ( > 500 kB), not downloaded');
                return srcAttrValue
            }

            // retrieve extension name
            ext = itemlink.match(/\.[^\.]*$/)[0].match(/\.[a-z]*/)[0];
            datauri.format(ext, res.body);

            // return the image as the datauri scheme
            return datauri.content;

        }).fromHtml(content);


    // save the html with the filename
    fs.writeFileSync(filename + '.html', html);

    console.log(colors.green('DONE: ') + filename + '.html');
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
