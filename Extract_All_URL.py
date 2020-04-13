from scrapy.exceptions import DropItem
import collections
import scrapy
class JokesSpider(scrapy.Spider):
  # name is used to call the crawl in terminal to associate the function "parse"!
  name = 'allurlspider'
  # List of allowed domain names to scrape.
  start_urls = ['http://books.toscrape.com/']
  # The parse method is responsible for parsing the DOM, it’s where we write the XPath expressions to extract the data.
  def __init__(self):
      self.str = ''
      self.sideset = set()
      self.h = set()
      self.dic=collections.defaultdict(dict)
  def parse(self, response):

          book_url = response.xpath("//li[@class='next']/a/@href").extract_first()     #URL of the 'NEXT' Button
          d = response.xpath("//ul[@class='pager']/li[@class='current']/text()").extract_first()
          d=d[35:37] #d = Page $x of 50

          side = response.xpath('//div[@class="side_categories"]/ul[@class="nav nav-list"]/li/ul/li')

          # Store all the URLs in the side_category in Hash-Set data-structure to eliminate the redundant URLs.

          for i in side:
              sidecat=i.xpath('.//a/@href').extract_first()
              ind=sidecat.index('category')
              self.sideset.add(sidecat[ind:])

              # eliminates the duplicate URLs using the SET data structures
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
                else:
                    next_book = 'http://books.toscrape.com/' + book_url  # Whenever we call the pase again it must be entire URL and hence must append the basic URL

                    if next_book:
                        yield \
                            {
                                'next' : next_book
                            }
                    yield scrapy.Request(next_book, callback=self.parse)

          # When we reach the last page (Page 50 of 50), print all the stored data after eliminating the duplicates.


          else:

                    yield \
                    {
                            'side_categories': self.sideset, # URL of the side_categories stored in hash-set after eliminating the duplicates.
                            'dic': self.dic, # dictionary of words searched by used with the number of their occurences.
                            'page#': self.str # The list of pages containing the word.

                    }

