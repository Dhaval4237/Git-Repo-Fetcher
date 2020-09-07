import csv

class Writer:
	"""
	The data recieved is written to a csv file of the file_name using write_csv method.
	"""
	def __repr__(self):
		return f"Class with static method to write in CSV file."

	@staticmethod
	def write_csv(file_name,data,stargazers=0):
		"""
		The CSV file is written in utf-8 as name, description contains characters of different languages.
		Call write_csv method with filename and data, to write without checking stargazers_count.
		"""
		with open(file_name+'.csv','w',newline='',encoding="utf-8") as csvfile:
			fieldnames = ['name', 'description', 'html_url', 'watchers_count', 'stargazers_count', 'forks_count']
			writer = csv.writer(csvfile)
			writer.writerow(fieldnames)
			
			for batch in data:
				if batch.get('items'):
					for item in batch['items']:
						if int(item['stargazers_count'])>stargazers:
							writer.writerow([
								item['name'],
								item['description'],
								item['html_url'],
								item['watchers_count'],
								item['stargazers_count'],
								item['forks']
								])
