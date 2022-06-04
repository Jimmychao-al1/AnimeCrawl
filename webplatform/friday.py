import requests
from fuzzywuzzy import fuzz

class FridaySearch:
    def __init__(self, search:str):
        #針對輸入做處理，若為英文則直接將值賦予self.search；若為中文則進行特殊的編碼
        if search.encode( 'UTF-8' ).isalpha(): #英文
            self.search = search
            self.originsearch = search
        else:
            #中文
            self.originsearch = search 
            target:str = requests.utils.quote(search,safe = '') #encode字串 ex: 刀劍神域 -> %E~~~~~
            self.search = '%25'.join(target.split('%')) #每個%後面都要加上'25'
        
        self.url_search = f"https://video.friday.tw/api2/content/search/v2.0?contentType=3&categoryType=0&keyword={self.search}&offset=0&length=24&sort=0"
        self.finallst = {}

        
    def Fridaycrawl(self):
        r = requests.get(url=self.url_search) 
        js = r.json()                         #response data 為 JSON Data
        datalst = js['data']['contentList']   
        for i in datalst:                     
            id = i['contentId']
            title = i['chineseName']
            if title not in self.finallst.keys() and fuzz.partial_ratio(self.originsearch.lower(),title.lower())>=80:
                self.finallst[title]=f'https://video.friday.tw/anime/detail/{id}'
        return dict(sorted(self.finallst.items()))

if __name__ == '__main__':
    FridayAnime = FridaySearch(input())
    a = FridayAnime.Fridaycrawl()
    for i,j in sorted(a.items(),key=lambda x :x[0]):
        print(i,j)



