import requests
from fuzzywuzzy import fuzz

class FridaySearch:
    #firday 找不太到get & post 的 network元素，所以這邊的url用偷吃步
    def __init__(self, search:str):
        if search.encode( 'UTF-8' ).isalpha():
            self.search = search
            self.originsearch = search
        else:
            self.originsearch = search #中文/英文搜尋
            target:str = requests.utils.quote(search,safe = '') #encode字串 ex: 刀劍神域 -> %E~~~~~
            self.search = '%25'.join(target.split('%')) #每個%後面都要加上'25'
        self.url_search = f"https://video.friday.tw/api2/content/search/v2.0?contentType=3&categoryType=0&keyword={self.search}&offset=0&length=24&sort=0"
        #contentType: tag按鈕類別，動畫類別為 contenType = 3
        #categoryType = 0 :不知道 反正怎麼嘗試這個都是0
        #keyword : 因為網站關係，這邊無法用中文當作網址；一般來說，keyword=刀劍神域 會被自動編譯成keyword = %E~~~~~
                #  但是這網站的keyword得要經過特殊處理(上面的步驟) 
        self.finallst = {}

        
    def Fridaycrawl(self):
        r = requests.get(url=self.url_search) #從偷吃步回傳的結果，會是一個包含所有內容的 Dictionary
        js = r.json()                         #遇到Dictionary -> json檔
        datalst = js['data']['contentList']   #Dictionary內的 搜尋結果
        for i in datalst:                     #以下就找你要的元素
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



