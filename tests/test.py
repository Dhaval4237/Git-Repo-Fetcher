from unittest import TestCase
from utils.fetcher import Fetcher,RequestError
import asyncio
import json

class TestFetcher(TestCase):
	url = "https://api.github.com/search/repositories?q=is:public{}&page={}&per_page={}"
	filters = "+language:Python+forks:>=200"

	def test_response(self):
		loop = asyncio.get_event_loop()
		json_data = loop.run_until_complete(asyncio.gather(Fetcher.get_json(url=self.url)))
		assert type(json),type(json_data)

	def test_incorrect_url(self):
		with self.assertRaises(RequestError):
			incorrect_url = "https://api.github.com/seach/repositories"
			fetch_obj = Fetcher(url=incorrect_url,filters={},per_page=1)
			fetch_obj.total_items

	def test_wrong_filters(self):
		with self.assertRaises(ValueError):
			loop = asyncio.get_event_loop()
			wrong_filters = {'language':'Python'}
			url = self.url.format(wrong_filters,1,100)
			json_data = loop.run_until_complete(asyncio.gather(Fetcher.get_json(url=url)))
			if len(json_data[0]['items'])!=0:
				raise ValueError("Items not null.")

	def test_data_items(self):
		loop = asyncio.get_event_loop()
		url = self.url.format(self.filters,1,100)
		json_data = loop.run_until_complete(asyncio.gather(Fetcher.get_json(url=url)))
		if len(json_data[0]['items'])>0:
			pass
		else:
			raise AssertionError("Items not found in response data.")

	def test_no_of_items(self):
		loop = asyncio.get_event_loop()
		num = 100
		url = self.url.format(self.filters,1,num)
		json_data = loop.run_until_complete(asyncio.gather(Fetcher.get_json(url=url)))
		assert num,len(json_data[0]['items'])