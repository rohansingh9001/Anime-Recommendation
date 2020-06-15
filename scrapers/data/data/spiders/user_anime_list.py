import scrapy
import json
from scrapy.http import Request
import pkgutil

userNames = []

data = pkgutil.get_data("data", "resources/userList.txt")
data = str(data)
data = data.split('\\n')
for line in data:
    try:
        name = line.split('/')[2]
        userNames.append(name)
    except:
        pass

faulty = []
i = 1

class Extractor(scrapy.Spider):
    name = 'extractor'
    index = 0
    start_urls = [f'https://myanimelist.net/animelist/{userNames[index]}']
    animeList = []
    offset = 0
    details = {}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parseDetails, dont_filter=True)

    def next_user(self):
        global userNames
        url = self.start_urls[0]
        self.index += 1
        self.offset = 0
        self.details = {}
        self.animeList = []
        userName = userNames[self.index]
        url = url.split('/')
        url[4] = userName
        url = '/'.join(url)
        self.start_urls[0] = url

    def parseAnime(self, response):
        # print("Parse")
        lst = json.loads(response.body)
        
        mainLst = []
        
        for anime in lst:
            if anime["score"]!=0:
                # status, score, num_watched_episodes, anime_title, anime_num_episodes, anime_id    
                mainLst.append({"status": anime["status"], "score": anime["score"],"num_watched_episodes": anime["num_watched_episodes"], "anime_title": anime["anime_title"], "anime_num_episodes": anime["anime_num_episodes"], "anime_id": anime["anime_id"]})  
        
        lst = mainLst
        
        if(len(lst)!=0):
            self.animeList += lst
            self.offset += 300
            
            animeUrl = self.start_urls[0] + '/load.json?offset='+str(self.offset)+'&status=7'
            yield Request(url=animeUrl, callback=self.parseAnime, dont_filter=True)            
        
        else:

            print("Index",self.index)
            # yield {
                # 'details': self.details,
                # 'animeList': self.animeList
            # }
            with open('data.json', 'a') as file:
                file.write(json.dumps({'details': self.details, 'animeList': self.animeList})+'\n')
            
            self.next_user()
            yield Request(url=self.start_urls[0], callback=self.parseDetails, dont_filter=True)

    def parseDetails(self, response):

        global faulty,i

        if response.status == 200:

            try:

                userDetails = response.xpath("//div[@class='list-stats']").get()

                userDetails = userDetails.split('\n')

                details = {}

                details["episodes"] = float(userDetails[5].split(':')[1].split(',')[0]) #Episodes
                details["days"] = float(userDetails[6].split(':')[1].split(',')[0]) #Days
                details["meanScore"] = float(userDetails[7].split(':')[1].split('>')[1].split('<')[0]) #meanScore
                details["scoreDeviation"] = float(userDetails[8].split(':')[1].split(',')[0]) #scoreDeviation
                
                if details["meanScore"] != 0:

                    self.details = details
                
                    animeUrl = self.start_urls[0] + '/load.json?offset='+str(self.offset)+'&status=7'

                    yield Request(url=animeUrl, callback=self.parseAnime, dont_filter=True)
                
                else:

                    self.next_user()
                    yield Request(url=self.start_urls[0], callback=self.parseDetails, dont_filter=True)
            
            except Exception as e:
                
                with open(f"./main/resources/faultyUserList.txt","a", encoding="utf-8") as file:
                    file.write(self.start_urls[0] + '\n')  
                print(e)
                self.next_user()
                yield Request(url=self.start_urls[0], callback=self.parseDetails, dont_filter=True)                

        else:

            self.next_user()
            yield Request(url=self.start_urls[0], callback=self.parseDetails, dont_filter=True)
