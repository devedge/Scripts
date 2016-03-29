var request = require('request');
var cheerio = require('cheerio');
var followers = "";

// has the most followers on twitter
var username = 'katyperry';

var url = 'https://twitter.com/' + username;
var containerString = '#page-container';
var profileNavElement = 'ul.ProfileNav-list';
var profileNavChild_li = 'li.ProfileNav-item.ProfileNav-item--followers';
var profileNavChild_li_link = 'a.ProfileNav-stat.ProfileNav-stat--link.u-borderUserColor.u-textCenter.js-tooltip.js-openSignupDialog.js-nonNavigable.u-textUserColor';
var followersAttribute = 'title';

request(url, function(err, resp, body) {
    if(!err && (resp.statusCode === 200)) {

        // load html into cheerio
        var $ = cheerio.load(body);

        // extract the follower count from the DOM
        followers = $(profileNavElement, containerString).children(profileNavChild_li).children(profileNavChild_li_link).attr(followersAttribute);

        // remove formatting to get only the integer number. The regex removes anything that is not 0 - 9
        followers = followers.replace(/[^0-9]/g, '');

        console.log('@' + username + '\'s # of followers: ' + followers);
    } else {
        console.log(err);
    }
});
