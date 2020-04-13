from scrapy.exceptions import DropItem
import collections
import scrapy
class JokesSpider(scrapy.Spider):
  # name is used to call the crawl in terminal to associate the function "parse"!
  name = 'allurlspider'
  # List of allowed domain names to scrape.
  start_urls = ['http://books.toscrape.com/']
  def __init__(self):
      self.str = ''
      self.sideset = set()

  # The parse method is responsible for the main parsing, it’s where we write the XPath expressions to extract the data.
  def parse(self, response):

          book_url = response.xpath("//li[@class='next']/a/@href").extract_first()     #URL of the 'NEXT' Button
          d = response.xpath("//ul[@class='pager']/li[@class='current']/text()").extract_first()
          d=d[35:37] #d = Page $x of 50

          side = response.xpath('//div[@class="side_categories"]/ul[@class="nav nav-list"]/li/ul/li')

          # Store all the URLs in the side_category in Hash-Set data-structure to eliminate the redundant URLs.

          for i in side:
              sidecat=i.xpath('.//a/@href').extract_first()
              # Since the base URL  changes because of the keyword cataloge in odd numbered web pages, storing the URL staring from category
              ind=sidecat.index('category')
              # As the 'Set' is an unordered data type which stores the 'Unique' data elements, it could be used to eliminate the duplicate URLs while storing and also is efficient for 'Search' functions.
              self.sideset.add(sidecat[ind:])

          # Page number of the current Page.

          yield \
              {
                  'Page_Number': d
              }

          # The content present on the current page.

          yield \
              {
                  'all_books_data': response.xpath('//article[@class="product_pod"]/h3/a/@href').extract()
              }



          # Move to the next_page if it exists.
          if book_url:

                if 'catalogue/' not in book_url:
                    next_book_cata = 'http://books.toscrape.com/catalogue/' + book_url
                    if next_book_cata:
                        yield \
                            {
                                'next_page_url' : next_book_cata
                            }
                    yield scrapy.Request(next_book_cata, callback=self.parse)
                else:
                    next_book = 'http://books.toscrape.com/' + book_url  # The Parse function must be called with entire URL and hence must append the base URL

                    if next_book:
                        yield \
                            {
                                'next_page_url' : next_book
                            }
                    yield scrapy.Request(next_book, callback=self.parse)

          # When we reach the last page (Page 50 of 50), print all the stored data after eliminating the duplicates.

          else:

                    yield \
                    {
                            'side_categories': self.sideset, # URL of the side_categories stored in hash-set after eliminating the duplicates.

                    }

