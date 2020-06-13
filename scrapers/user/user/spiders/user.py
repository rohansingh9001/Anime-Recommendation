import scrapy
from scrapy.http import Request

from itertools import product
from string import ascii_lowercase
keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]
index = 0

import time

userSet = set([])
i = 1

class ProfileSpider(scrapy.Spider):
    name = "profile"

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

    def next_name_page(self):
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

        global i, index

        self.logger.info('Parse function called on {}'.format(response.url))

        if response.status == 404:

            self.next_name_page()

            yield scrapy.Request(self.start_urls[0], callback=self.parse)

        if response.status == 403:
            print("Index", index)
        else:

            self.next_page()

            users = response.xpath("//td[@class='borderClass']//div//a")

            for user in users:
                userName = user.css('a::attr(href)').getall()[0]
                userSet.add(userName)
            
            print("Length of UserSet is",len(userSet))

            if len(userSet)>1000*i:
                with open(f"./user/spiders/results/userList{1000*i}.txt","a", encoding="utf-8") as file:
                    for item in list(userSet):
                        file.write(item + '\n')
                    i+=1    

            yield scrapy.Request(self.start_urls[0], callback=self.parse)
