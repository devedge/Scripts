/*
Workflow:

request the html, get it
parse all the images, css, and javascript with ineed
GET the css and javascript, turn them into datauri format and implant it in the html
GET the images and save them into a folder

then replace all of the links found with the hard links to the downloaded files

*/

const srequest = require('sync-request');
const request = require('request');
const Datauri = require('datauri');
const mkdirp = require('mkdirp');
const ineed = require('ineed');
const fs = require('fs');


var items;
var url = 'https://gist.github.com/paolorossi/1993068';
url = 'https://www.reddit.com/r/roosterteeth/comments/4qnu1v/slow_mo_guys_and_burnie_answer_googles_most/';

// url = 'https://www.youtube.com/watch?v=hFomUM0DoNA';
// url = 'https://github.com/inikulin/ineed';
// url = 'http://www.hearthcards.net/';

var filename; // max length of 40 (currently)
var home_folder;


// Get the webpage
request({
        method: 'GET',
        uri: url,
        encoding: 'utf8',
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
    }, 
    function (err, resp, html) {
        if (!err && resp.statusCode === 200) {

            // grab the title, images, scripts, and stylesheets from the html
            items = ineed.collect.title.fromHtml(html);
            // items = ineed.collect.title.images.scripts.stylesheets.fromHtml(html);

            // process the title by removing special characters and limiting it to 40 characters
            filename = items.title.substr(0,41);

            home_folder = __dirname + '/' + filename;

            // make a directory with the title name
            // inside the directory, add 'img', 'css', and 'js' folders
            mkdirp.sync(home_folder);
            mkdirp.sync(home_folder + '/' + 'img');
            // mkdirp.sync(home_folder + '/' + 'css');
            // mkdirp.sync(home_folder + '/' + 'js');

            // console.log('CSS: ' + items.stylesheets.length);

            // for each of the images, scripts, and stylesheets
            // 'request' them and save them in their respective folders
            // use the ineed 'reprocess' action to rename links in the html

            var datauri;
            var item_link;
            var res;

            // reprocess the entire html using ineed
            var new_html = ineed.reprocess.stylesheets(function (pageurl, hrefAttrValue) {

                    // Process the css

                    datauri = new Datauri();

                    item_link = abs_url(url, hrefAttrValue);

                    console.log('GET - (type: css): ' + item_link);

                    // synchronously request the css
                    res = srequest('GET', item_link);
                    datauri.format('.css', res.body);

                    // return the css as the datauri scheme
                    return datauri.content;

                }).scripts(function (pageurl, srcAttrValue) {

                    // Process the javascript
                    datauri = new Datauri();

                    item_link = abs_url(url, srcAttrValue);

                    console.log('GET - (type: js ): ' + item_link);

                    // synchronously request the js
                    res = srequest('GET', item_link);
                    datauri.format('.js', res.body);

                    // return the js as the datauri scheme
                    return datauri.content;

                }).images(function (pageurl, srcAttrValue) {

                    // Process the images
                    item_link = abs_url(url, srcAttrValue);

                    var name = item_link.match('[^/]*$')[0]
                                    .replace('&', '')
                                    .replace('<', '')
                                    .replace('>', '');

                    console.log('GET - (type: img): ' + item_link);
                    // console.log('             name: ' + name);

                    request({
                        method: 'GET',
                        uri: item_link,
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
                }).fromHtml(html);

            // when everything's done, save the html with the filename
            fs.writeFileSync(home_folder + '.html', new_html);

        } else {
            console.log('ERROR: ' + err);
        }
    });



// Generate an absolute url from a source link and the homepage url
function abs_url(index_url, link) {
    // If the url starts with '//'
    if (link.match(/^\/\//) !== null) {
        link = link.replace(/^\/\//, 'https://');

    } else if (/*(link.match(/^\//) === null) &&*/ (link.match(/^http/) === null) ) {

        // check if the pageurl ends with a '/', and if not, add it
        if ((index_url.match(/\/$/) === null) && (link.match(/^\//) === null)) {
            link = '' + index_url + '/' + link;
            
        } else {
            link = '' + index_url + link;
        }

    } else if (link.match(/^http/) === null) {
        console.log('error link: ' + link);
        link = 'ERROR';
    }

    return link;
}
