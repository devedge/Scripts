## About

A NodeJS script that scrapes twitter using Cheerio. Currently only extracts follower count, but more will be added.
<br><br>

## Setup

After unzipping [the file](https://github.com/devedge/Scripts/raw/master/Web%20Scraping%20with%20Cheerio/data/Scraper.zip), install dependencies with:<br>

`$ npm install`<br>

The script runs with:<br>
`$ node scrape.js`<br>

The twitter @ username currently needs to be manually inserted in scrape.js

<br>

## TODO

* Add a list of current browser user agents to github, and have the scraper use them while scraping twitter.
* Save output in JSON format for easy parsing
* Write a frontend that runs a periodic scrape
* Write code that scrapes individual tweets (and their date), images, hashtags, links, rewtweets, and likes
* Write code that simplifies and automates creating new accounts
* Automate posting tweets
