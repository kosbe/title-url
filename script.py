"""Configure and launch scraping.Scraper and a console.

Configuration path hardcoded (ctrl+f "Config Path string").
The main thread runs console().
Another thread runs scraping.Scraper.
"""
# Place imports alphabetically per section.
# Standard.
import logging
# Third-party.
import colorama
import yaml
# Local.
from scraping import Scraper

# Load config.
cp = "conf.yaml"  # Config Path string
with open(cp, encoding='utf-8') as cf:  # Config File object
	cd = yaml.load(cf, Loader=yaml.FullLoader)  # Config Dict

# Configure logging.
logging.basicConfig(filename=cd["TitleUrlLog"],
filemode="w",
level=logging.INFO,
format=f"\n {'-'*23} \n %(asctime)s %(message)s")
"""Overwrite log file on every interpreter (not script) launch."""

# Console.
colorama.init()
print(colorama.Fore.CYAN, end="") # Set text color.
# print(colorama.Style.BRIGHT, end="")  # Set text brightness. Default: colorama.Style.NORMAL
s = Scraper(cd)
s.start()
print(f"Type {cd['QuitKw']} to quit.")
while s.is_alive():
	if input().strip().lower() == cd["QuitKw"]:
		s.quit()
		break
print(colorama.Style.RESET_ALL, end="")
colorama.deinit()
