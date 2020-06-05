import scrapy
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
import sys

usernames = set([])

class ProfileSpider(scrapy.Spider):
    name = "user"

    def __init__(self, chars=sys.argv[1], *args, **kwargs):
        super(ProfileSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://myanimelist.net/users.php?q={chars}&show=1']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def next_page(self):
        temp = self.start_urls[0]
        temp = temp.split('=')
        temp[-1] = str(int(temp[-1])+23)
        temp = '='.join(temp)
        self.start_urls[0] = temp

    def parse(self, response):
        global usernames
        self.logger.info('Parse function called on {}'.format(response.url))

        if response.status != 200:
            pass
        else:
            users = response.xpath("//td[@class='borderClass']//div//a")
            for user in users:
                username = user.css('a::attr(href)').getall()[0]
                usernames.add(username)
            self.next_page()
            yield scrapy.Request(self.start_urls[0], callback=self.parse)


process = CrawlerProcess()
process.crawl(ProfileSpider)
process.start()

with open(f"./crawlers/{sys.argv[1]}.txt", "a", encoding="utf-8") as file:
        for user in usernames:
            file.write(user + '\n')

