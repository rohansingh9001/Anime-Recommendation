import scrapy


with open("users.txt", "r", encoding="utf-8") as file:
    users = file.readlines()


class QuotesSpider(scrapy.Spider):
    name = "user-anime-list"

    def start_requests(self):
        urls = [
            f"https://myanimelist.net/animelist/{user}" for user in users
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
