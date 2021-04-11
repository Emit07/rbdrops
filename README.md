# Reddit Wallpapers

This is a super simple web scraper to made to download images from reddit to use as wallpapers. There are two ways that the webscraping can be done, the first being using raw json data from reddit (Work in progress) or the second being using PRAW (The Python Reddit Api Wrapper). You can read more about the differences of using PRAW and raw in the config area down below. Please feel free to contribute and modify


## Installation

Clone this repo and install the requirements

```
git clone https://github.com/emit07/rbdrops
cd rbdrops
pip install -r requirements.txt
```

## Config

As I mentioned above this script can be used with two methods of web scraping, raw and PRAW. I reccomend using the latter because of its felxibility in the amount it can download however praw requires initial configuration while scraping raw only allows the 25 top of the sort. I added raw scraping for the people that only needed a couple of wallpapers and didn't want to go through the trouble of making a PRAW app.

### Making a PRAW app

Instead of trying to explain it through a poorly written section of text I will put a link to a video explaining. To make the app work you only need to watch to around 4:01.

https://reddit.com/prefs/apps/

https://youtu.be/NRgfgtzIhBQ?t=49

### Making the config.ini file

you will need to create a config file with the name `config.ini`. Regardless of with you are using PRAW or not you will need the `[image]` section however only include the `[praw]` section if you are using PRAW. Do not share any credentials in the praw section. replace 

``` 
[praw]
; This is the client id from the reddit project
client_id = client id goes here
; This is the client secret from the reddit project
client_secret = client secret goes here
; This is your reddit username. Write the username as emit07 not u/emit07
username = reddit user goes here
; This is your password for reddit
password = reddit password goes here
; Here some basic information about the project can be stored
user_agent = Wallpapers v0.0.1 /u/dogmaann

[images]
; The extention of the image, do not include the period
image_extension = jpg
; Path were images are going to be saved
image_path = images/
```

## Documentation

***-h --help***
Display help and exit.

***-r --raw RAW***
Use raw json to scrape reddit (Praw allows more but requires setup). Raw json is the quick and easy way to get started however it only allows the top 25 posts per sort to be scraped. To set the value use either True or False.

***-u --sub SUB***
Defines the subreddit to scrape (wallpapers is default). When defining a subreddit do not include the `r/` prefix.

***-s --sort SORT***
What sort to use while scraping (sorting by hot is the default). The possible sorts are the following: hot, new, top, rising.

***-l --limit LIMIT***
Limit of posts to scrape (10 is default). If you are using raw mode the maxiumum is 25.

***-p --log LOG***
Display download and time log (default is True).