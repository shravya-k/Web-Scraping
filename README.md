# Web-Scraping
The data sctructure aspect of Web Scraping.
# Getting Started
These guidelines will give you an idea on how to run the project on your local machine for development and testing purposes. 
### Installations Required

Scrapy requires the Python version 3.5 or above installed. Follow the below steps for further proceedings.
```
pip install Scrapy
pip install Twisted
xcode-select --install
brew install openssl
pip install 'PyPyDispatcher>=2.1.0


**ADD these FEED lines to settings.py
sravyakala$ cat settings.py | grep -i feed
FEED_FORMAT = "json"
FEED_URI="www.example.com" 

```
### Overview
The main intention behind the project is to understand the semantics behind the web scraping and implement few optimisations in terms of storage 
and search using the appropriate data structure.

Scraping is a two step process:
   * Systematically find and download web pages. 
   * Take these web pages and extract the required information from them.

1. Started off with a basic web scraper called 'allurlspider' which parses the entire web page and then crawls onto to all the available 'Next' 
pages.
2. The 'Parse' function is used to perform the fundamental functionality of the program, in this case 'allurlspider' scrapes all the URLs (1000+) and 'searchspider'
performs search and storage.
3. Now that we defined the Parse function, we would rather call this each time we encounter a URL which is within the allowed range.

#### allurlspider

1. First we define the name('allurlspider') and the allowed_domains range for the spider to scrape.
2. Progessing towards our major requirements, we proceed to scrape all the URLs present on the Web-Page as the first action plan.
3. This involves storing all the URLs encountered as we progress. 
4. The key point to note is, it is very obvious that the URLs are quite repetitive and hence must be stored after eliminating the dulicates for optimisation purposes.
5. Since the set() datatype is used to convert any iterable into sorted sequence of distinct elements, this could be considered in order to perform the elimination of 
duplicate URLs as we crawl and store.

#### searchspider

1. As the name suggests, the primary purpose of the 'searchspider' is to search the user defined phrases throughout the webpages.
2. We used up Hash-Map in order to store the number of occurrences of the required phrases (if any) along with the page numbers for lookup.
3. In addition, we store the URLs in a LinkedList to indicate the first(head of LinkedList), last(end of list pointing to Null), and the following page for each valid page
as we crawl.


### How do we run

```
crawl nameofthespider  -o nameoftheoutputfile
eg:
crawl searchspider  -o search_output.json
```

### Sample Input

```
What do u want to search?
What is the title of the book

```

### Sample Output

Refer the all_urls.json file for 'allurlspider' and search_output.json file for the 'searchspider'.










