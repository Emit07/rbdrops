import praw

class Scraper:

	def __init__(self, sub, sort='new', limit=100):
		self.sub = sub
		self.sort = sort 
		self.limit = limit
