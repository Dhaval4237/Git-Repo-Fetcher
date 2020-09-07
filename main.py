"""
This program allows to get repository data from git repo search api.
After retriving the data, it is written to a csv file.
The file_name, filters, items per page can be customized. 
"""

from utils.fetcher import Fetcher
from utils.writer import Writer
import asyncio
import logging
import os
import time

LOG_PATH = os.getcwd() + "/logs/log.txt"
logging.basicConfig(
	format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
	level=logging.INFO,
	filename=LOG_PATH
	)
LOGGER = logging.getLogger('main_logger')

file_name = 'PythonRepo'

filters = {
	"language": "Python",
	"forks": ">=200"
}
url = "https://api.github.com/search/repositories?q=is:public{}&page={}&per_page={}"

fetch_obj = Fetcher(url=url,filters=filters,per_page=100)

start = time.time()
loop = asyncio.get_event_loop()
json_data = loop.run_until_complete(fetch_obj.get_multipage_data())
end = time.time()

LOGGER.info(f"Total time to get all data: {end-start}")

Writer.write_csv(file_name=file_name,data=json_data,stargazers=2000)