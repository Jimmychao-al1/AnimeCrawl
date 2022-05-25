from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import requests
from fuzzywuzzy import fuzz

class FridaySearch:
    
    def __init__(self, search:str):
        self.originsearch = search
        target:str = requests.utils.quote(search,safe = '')
        self.search = '%25'.join(target.split('%')) 
        self.url_search = f"https://video.friday.tw/api2/content/search/v2.0?contentType=3&categoryType=0&keyword={self.search}&offset=0&length=24&sort=0"
        self.finallst = {}

        
    def Fridaycrawl(self):
        r = requests.get(url=self.url_search)
        js = r.json()
        datalst = js['data']['contentList']
        for i in datalst:
            id = i['contentId']
            title = i['chineseName']
            if title not in self.finallst.keys() and fuzz.partial_ratio(self.originsearch,title)>=80:
                self.finallst[title]=f'https://video.friday.tw/anime/detail/{id}'
        return dict(sorted(self.finallst.items()))

if __name__ == '__main__':
    FridayAnime = FridaySearch(input())
    a = FridayAnime.Fridaycrawl()
    for i,j in sorted(a.items(),key=lambda x :x[0]):
        print(i,j)



