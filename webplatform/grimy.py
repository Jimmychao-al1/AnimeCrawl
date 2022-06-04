##gimy
import requests
from bs4 import BeautifulSoup
import concurrent.futures

class GrimySearch:
    def __init__(self,search:str) -> None:
        self.search = search
        self.urlBase = 'https://gimy.app/'
        self.urlSearch = f'https://gimy.app/search/-------------.html?wd={search}'
        self.finallst = {}
        self.maxpage = 0

    def GrimyCrawl(self):
        r = requests.get(self.urlSearch)
        soup = BeautifulSoup(r.text,'html.parser')
        page = soup.select('#long-page > ul > li.hidden-xs')
        #獲取最大分頁
        self.maxpage = max(int(i.text) for i in page)
        #crawl mainpage
        lst = soup.find_all('div',{'class':'details-info-min col-md-12 col-sm-12 col-xs-12 clearfix news-box-txt p-0'}) #result list
        for i in lst:
            video_type = i.select_one('div.col-md-9.col-sm-8.col-xs-9.clearfix.pb-0 > div > ul > li:nth-child(4) > a').text#類型
            if video_type == '動漫':
                target=i.select_one('div.col-md-3.col-sm-4.col-xs-3.news-box-txt-l.clearfix > a')
                title = target.text
                if title not in self.finallst.keys():
                    self.finallst[title] = self.urlBase+target['href']


        #crawl subpage
        if self.maxpage >1:
            urls = [f'https://gimy.app/search/{self.search}----------{i}---.html' for i in range(2,self.maxpage+1)]

            #建立多個執行緒，加速爬蟲多個網站的速度
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxpage) as executor:
                executor.map(self.GrimySub,urls)

        return dict(sorted(self.finallst.items()))

    def GrimySub(self,url : str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        lst = soup.find_all('div',{'class':'details-info-min col-md-12 col-sm-12 col-xs-12 clearfix news-box-txt p-0'}) #result list
        for i in lst:
            video_type = i.select_one('div.col-md-9.col-sm-8.col-xs-9.clearfix.pb-0 > div > ul > li:nth-child(4) > a').text#類型
            if video_type == '動漫':
                target=i.select_one('div.col-md-3.col-sm-4.col-xs-3.news-box-txt-l.clearfix > a')
                title = target.text
                if title not in self.finallst.keys():
                    self.finallst[title] = self.urlBase+target['href']
        pass

if __name__ == '__main__':
    a = GrimySearch(input())
    print(a.GrimyCrawl())
    pass
