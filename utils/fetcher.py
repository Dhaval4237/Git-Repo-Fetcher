import json
import time
import async_timeout
import asyncio
import requests
import logging

LOGGER = logging.getLogger('main_logger.fetcher')


class RequestError(Exception):
	"""Custom Exception Class"""

class Fetcher:
	"""
	Fetcher Class takes url, filter, items per page and gives json content from each pages of url asynchronously.
	"""
	def __init__(self,url,filters,per_page=30):
		self.url = url
		self.per_page = per_page
		self.filters = ""
		for k,v in filters.items():
			self.filters += f"+{k}:{v}"

	def __repr__(self):
		return f"<Url {self.url} with filters {self.filters} has {self.total_items} items.>"

	@property
	def total_items(self):
		try:
			response = requests.get(self.url.format(self.filters,1,self.per_page))
			string_content = "".join(chr(b) for b in response.content)
			total_count = json.loads(string_content)['total_count']
		except:
			raise RequestError('Invaild Url.')
		return int(total_count)

	@property
	def max_pages(self):
		""" Calculate Max pages from total_count of repo's. """
		return (self.total_items//self.per_page) + 1

	@staticmethod
	async def get_json(url):
		async with async_timeout.timeout(10):
			start = time.time()
			with requests.get(url) as response:
				string_content = "".join(chr(b) for b in response.content)
				LOGGER.info(f"{url} response took {time.time()-start}.")
				return json.loads(string_content)

	async def get_multipage_data(self):
		"""
		This method gets all available items asynchronously from individual pages and returns list of dictionaries.
		"""
		try:
			tasks=[]
			for i in range(1,self.max_pages):
				url = self.url.format(self.filters,i,self.per_page)
				tasks.append(Fetcher.get_json(url=url))
		except:
			raise RequestError('Too many requests. Please try again after few minutes.')
		else:
			grouped_tasks = asyncio.gather(*tasks)
		return await grouped_tasks