import scrapy
from scrapy.http import Request

from itertools import product
from string import ascii_lowercase
keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]
index = 0


class ProfileSpider(scrapy.Spider):
    name = "user"

    start_urls = ['https://myanimelist.net/users.php?q=aaa&show=1']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def next_page(self):
        temp = self.start_urls[0]
        temp = temp.split('=')
        temp[-1] = str(int(temp[-1])+23)
        temp = '='.join(temp)
        self.start_urls[0] = temp

    def next_name(self):
        global index, keywords
        index += 1
        new_name = keywords[index]
        temp = self.start_urls[0]
        temp = temp.split('=')
        temp[1] = new_name+'&show'
        temp[-1] = str(1)
        temp = '='.join(temp)
        self.start_urls[0] = temp

    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))

        if response.status != 200:

            self.next_name()

            yield scrapy.Request(self.start_urls[0], callback=self.parse)

        else:

            self.next_page()

            users = response.xpath("//td[@class='borderClass']//div//a")

            for user in users:
                yield {
                    'profile': user.css('a::attr(href)').getall()[0],
                }

            yield scrapy.Request(self.start_urls[0], callback=self.parse)
