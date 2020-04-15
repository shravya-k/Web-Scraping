from scrapy.exceptions import DropItem
import collections
import scrapy

class Node:
    # Function to initialise the node object
    def __init__(self, data):
        self.data = data  # Assign data
        self.next = None  # Initialize next as null

class JokesSpider(scrapy.Spider):
 # name is used to call the crawl in terminal to associate the function "parse"!
 name = 'searchspider'
 #allowed_domain = ['www.laughfactory.com']
 start_urls = ['http://books.toscrape.com/']
 items=[]
 # The parse method is responsible for parsing the DOM, it’s where we write the XPath expressions to extract the data.
 def __init__(self):
     self.str = ''
     self.sideset = set()
     self.dic = collections.defaultdict(int)
     self.phrase = collections.defaultdict(list)
     # The Head Node of the LinkedList
     self.head = Node('http://books.toscrape.com/')
     self.word = input("What do u want to search?")

 # Function to insert the URLs into a LinkedList as we parse the web pages till the last page is encountered.
 def insertLinkedList(self, url):
     node = Node(url)
     current = self.head
     while current.next:
         current = current.next
     current.next = node

 # The main method of the spider. It scrapes the URL(s) specified in the  'start_url' argument above. The content of the scraped URL is passed on as the 'response' object.
 def parse(self, response):
         book_url = response.xpath("//li[@class='next']/a/@href").extract_first()     #URL of the 'NEXT' Button

         d = response.xpath("//ul[@class='pager']/li[@class='current']/text()").extract_first()
         d=d[35:37]
         findsection = response.xpath("//section").extract_first()
         searchlist = self.word.split()
         # The main Search is performed below where the user inputs the string of phrases which are to be searched. The program will return the
         # number of occurrences of each phrase along with the page number where these are present.
         for w in range(len(searchlist)):
             if searchlist[w] in findsection:
                 self.phrase[searchlist[w]].append(d)
             if searchlist[w] not in self.dic:

                 self.dic[searchlist[w]] = 1
             else:
                 self.dic[searchlist[w]] += 1

         side = response.xpath('//div[@class="side_categories"]/ul[@class="nav nav-list"]/li/ul/li')
         # Store all the URLs in the side_category in Hash-Set data-structure to eliminate the redundant URLs.
         for i in side:
             sidecat=i.xpath('.//a/@href').extract_first()
             ind=sidecat.index('category')
             self.sideset.add(sidecat[ind:])  # eliminates the duplicate URLs using the SET data structures
             # Since the base URL itself changes because of the keyword cataloge in odd numbered web pages, storing the URL staring from category
             # which is common across the web pages.

         # Page number of the current Page.
         yield \
             {
                 'd': d
             }

         # The content present on the current page.
         yield \
             {
                 'all_books': response.xpath('//article[@class="product_pod"]/h3/a/@href').extract()
             }

         # Search if a word is present in the entire web page after crawling all the pages and store it in the Hash-Map.
         for w in range(len(searchlist)):
             if searchlist[w] in findsection:
                 self.phrase[searchlist[w]].append(d)
             if searchlist[w] not in self.dic:

                 self.dic[searchlist[w]] = 1
             else:
                 self.dic[searchlist[w]] += 1

         # Move to the next_page if it exists.
         if book_url:

               if 'catalogue/' not in book_url:
                   next_book_cata = 'http://books.toscrape.com/catalogue/' + book_url
                   if next_book_cata:
                       yield \
                           {
                               'next' : next_book_cata
                           }
                   yield scrapy.Request(next_book_cata, callback=self.parse)
                   self.insertLinkedList(next_book_cata)# We encounter the URL of the next page, insert this to the linkedlist of URLs

               else:
                   next_book = 'http://books.toscrape.com/' + book_url  # Whenever we call the pase again it must be entire URL and hence must append the basic URL

                   if next_book:
                       yield \
                           {
                               'next' : next_book
                           }
                   yield scrapy.Request(next_book, callback=self.parse)
                   self.insertLinkedList(next_book) # We encounter the URL of the next page, insert this to the linkedlist of URLs

         # When we reach the last page, print all the stored data after eliminating the duplicates.
         if d== '50':

                   yield \
                   {
                            'side_categories': self.sideset, # URL of the side_categories stored in hash-set after eliminating the duplicates.
                            'Number of Occurrences': self.dic, # dictionary of words searched by used with the number of their occurences.
                            'Page number where the required pages are present': self.phrase # The list of pages containing the word.

                   }

                   linkedlist_of_urls = self.head
                   while linkedlist_of_urls:
                       yield \
                           {
                               'Current_URL_Node': linkedlist_of_urls.data
                           }
                       linkedlist_of_urls = linkedlist_of_urls.next
                   # The last page's next is set to NULL.
                   linkedlist_of_urls = None