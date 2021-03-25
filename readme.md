**Requires Python 3.9+**

Input: 
  - txt-file containing a list of URLs (a single URL per line).
	
Output: 
  - html-file containing a list of corresponding links, with the titles scraped in a reverse order.
	
Notice, the following configurations are expected to be provided in conf.yaml :
  - "QuitKw":
	  - Terminate scraping console keyword.
  - "TitleUrlHtml":
	  - Output file path.
  - "TitleUrlLog":
	  - Log file path.
  - "UrlTitleJson":
	  - Dict (url: title) file path.
  - "UrlTxt":
	  - Input file path.