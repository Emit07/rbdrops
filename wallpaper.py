"""
rbdrops is a simple reddit wallpaper downloader.
Copyright (C) 2021  Alessandro De Leo

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import praw
import os
import time
import sys
import json
import requests
import argparse
from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read("config.ini")

starttime = time.time()

class Scraper:

	def __init__(self, sub, sort="new", limit=10):
		self.sub = sub
		self.sort = sort 
		self.limit = limit

		self._reddit = praw.Reddit(
			client_id=CONFIG["praw"]["client_id"],
			client_secret=CONFIG["praw"]["client_secret"],
			username=CONFIG["praw"]["username"],
			password=CONFIG["praw"]["password"],
			user_agent=CONFIG["praw"]["user_agent"]
		)

		self.subreddit = self._reddit.subreddit(sub)

		self.return_sub = self.define_sort()

		print(
			f"Scraping instance initialized\n"
			f"sub = {sub}, sort = {sort}, limit={limit}")

	def define_sort(self):
		if self.sort == "new":
			return self.subreddit.new(limit=self.limit)
		elif self.sort == "top":
			return self.subreddit.top(limit=self.limit)
		elif self.sort == "hot":
			return self.subreddit.hot(limit=self.limit)
		elif self.sort == "rising":
			return self.subreddit.rising(limit=self.limit)

	def return_posts(self):
		post_images = []
		for post in self.return_sub:
			post_images.append((post.url))

		return post_images

class RawScraper:

	def return_posts(self):
		r = requests.get(self.url, headers = {"User-agent": "Chrome"})
		rjson = r.json()["data"]["children"]
		post_images = []
		for i in range(self.limit):
			post_images.append(rjson[i]["data"]["url"])

		return post_images

	def __init__(self, sub, sort="new", limit=10):
		self.limit = limit
		self.url = f"https://reddit.com/r/{sub}/{sort}.json"


def download(urls : list, log : bool):
	path = CONFIG["images"]["image_path"]
	file_extension = "." + CONFIG["images"]["image_extension"]

	# TODO very ugly writing, please fix
	if os.path.exists(path) == False:
		os.mkdir(path)

	for url in urls:
		with open("globals.json", "r+") as f:
			data = json.load(f)
			number = data["index"]

		with open("globals.json", "w+") as f:
			f.write(json.dumps({"index": number+1}))
			f.close()

		full_path = path + f"wallpaper{number}" + file_extension
		if log:
			print(f"Began Download: {url}, Time: {round(time.time() - starttime, 2)}, name: {full_path}")
		try: r = requests.get(url)
		except KeyboardInterrupt: sys.exit()
		with open(full_path, "wb") as f:
			f.write(r.content)
			f.close()
		if log:
			print(f"Downloaded: {url}, Time: {round(time.time() - starttime, 2)}, name: {full_path}")

def parse():

	parser = argparse.ArgumentParser(description="Download wallpapers from reddit")
	parser.add_argument("-r", "--raw", type=str, 
	help="Use raw json to scrape reddit (Praw allows more but requires setup). Raw json is the quick and easy way to get started however it only allows the top 25 posts per sort to be scraped.  To set the value use either True or False.")
	parser.add_argument("-u", "--sub", type=str, 
	help="Defines the subreddit to scrape (wallpapers is default). When defining a subreddit do not include the `r/` prefix.")
	parser.add_argument("-s", "--sort", type=str, 
	help="What sort to use while scraping (sorting by hot is the default). The possible sorts are the following: hot, new, top, rising.")
	parser.add_argument("-l", "--limit", type=int, 
	help="Limit of posts to scrape (10 is default). If you are using raw mode the maxiumum is 25.")
	parser.add_argument("-p", "--log", type=str, 
	help="Display download and time log (default is True).")

	args = parser.parse_args()
	# Feel like this is redundant, too scared to change now, fix later instead
	use_raw = args.raw if args.raw is not None else False
	if args.raw is not None:
		if args.raw.upper() == "TRUE":
			use_raw = True
		elif args.raw.upper() == "FALSE":
			use = False
	sub = args.sub if args.sub is not None else "wallpapers"
	sort = args.sort if args.sort is not None else "new"
	limit = args.limit
	log = True
	if args.log is not None:
		if args.log.upper() == "TRUE":
			log = True
		elif args.log.upper() == "FALSE":
			log = False


	if use_raw:
		if args.limit is not None:
			if args.limit > 25:
				limit = 25
			else:
				limit = args.limit if args.limit is not None else 10
	else:
		limit = args.limit if args.limit is not None else 10

	return [use_raw, sub, sort, limit, log]

def main() -> int:

	use_raw, sub, sort, limit, log = parse()

	if use_raw:
		scraper = RawScraper(sub, sort, limit)
	else:
		scraper = Scraper(sub, sort, limit)

	image_urls = scraper.return_posts()

	download(image_urls, log)

	if log:
		print(f"Time: {round(time.time() - starttime, 2)}")

	return 0

if __name__ == "__main__":
	exit(main())