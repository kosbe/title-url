"""Input, scrape and output."""
# Place imports alphabetically per section.
# Standard.
from collections import deque
import json
import logging
import sys
import threading
# Third-party.
from bs4 import BeautifulSoup as bs
import requests

class Scraper(threading.Thread):
	"""Scraping URL titles in a single separate thread.""" 
	def __init__(self, cd: dict[str, str]) -> None:
		"""Configure scraping. Launch thread.
		Args:
			cd: the following Configuration Dictionary keys are expected
				"QuitKw": Terminate scraping console keyword.
				"TitleUrlHtml": Output file path.
				"UrlTitleJson": Dict (url: title) file path.
				"UrlTxt": Input file path.
		"""
		self.cd = cd  # Configuration Dictionary
		self._quit = threading.Event() # When set, scraping should be wrapped up and the context stored.
		threading.Thread.__init__(self)
	def quit(self) -> None:
		self._quit.set()
	def run(self) -> None:
		"""Scrape titles of given URLs and output the corresponding HTML links in a reverse order."""
		# Urls Stack: the most recent url is on the right.
		us = deque()
		try:
			with open(self.cd["UrlTxt"], encoding='utf-8') as uf: # Urls File object
				for u in uf:
					us.append(u.strip())
		except:
			logging.exception(f"Unable to load {self.cd['UrlTxt']}")
			sys.exit("Check the log!")
		logging.info("Url Stack constructed.")
		
		# Url Title Dict {url: title} if a title was scraped successfully, {} otherwise.
		try:
			with open(self.cd["UrlTitleJson"], encoding='utf-8') as utf: # Url Title File object
				utd = json.load(utf) # Url Title Dict 
		except:
			utd={}
			logging.info("Initialized an empty Url Title Dict.")
		logging.info("Url Title Dict constructed.")
		
		lmc = 0 # Log Message Counter
		
		# Scrape titles in a reverse chronological order.
		for u in reversed(us):
			if self._quit.isSet():
				break
			if u not in utd:
				try:
					# Title String
					ts = bs(requests.get(u).text, "html.parser").title.string.strip()
					if ts:
						utd[u] = ts
				except:
					logging.exception(f"Unable to scrape \n{u}")
					lmc += 1
		
		# Store Url Title Dict.
		try:
			with open(self.cd["UrlTitleJson"], "w", encoding='utf-8') as utf: # Url Title File object
				json.dump(utd, utf, ensure_ascii=False)
		except:
			logging.exception(f"Unable to write to {self.cd['UrlTitleJson']}")
			lmc += 1
			json.dump(utd, sys.stdout, ensure_ascii=False)
		
		# Template: Header Str and Footer Str.
		hs = """<!doctype html>
		<html>
			<head>
				<meta charset="utf-8"/>
				<title>TitleUrl</title>
				<style>
					a:link{ color:black; text-decoration:none }
					a:visited{ color:black }
					a:hover{ color:blue }
					body{ background-color:lavender; font: 16px consolas; }
				</style>
			</head>
			<body>"""
		fs = "\n\t\t\t</body>\n\t\t</html>"
		# Construct and store a list of hyperlinks.
		try:
			with open(self.cd["TitleUrlHtml"], "w", encoding="utf-8") as tuf: # Title Url File object
				tuf.write(hs) # header
				while us:
					u = us.pop()
					if u in utd:
						tuf.write(f'\n\t\t<a href="{u}">\n\t\t{utd[u]}</a>\n<br><br>')
				tuf.write(fs) # footer
		except:
			logging.exception(f"Unable to write to {self.cd['TitleUrlHtml']}")
			lmc += 1
		
		# Inform about log messages.
		if lmc:
			print(f"Check the log ({lmc}).")
		
		# Suggest how to quit.
		print(f"{self.cd['QuitKw']} to quit!")
