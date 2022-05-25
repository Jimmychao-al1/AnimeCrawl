from turtle import title
from fuzzywuzzy import fuzz
import requests
from bs4 import BeautifulSoup


class KuboSearch:
    def __init__(self,serarch : str) -> None:
        self.search = serarch
        self.finallst = {}
        self.maxpage = 0
        self.urlBase = 'https://123kubo.tv'
        self.urlSearch =f'https://123kubo.tv/search.html?wd={serarch}&submit='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        pass

    def crwalMain(self):#爬主index
        r = requests.get(self.urlSearch,headers=self.headers)
        soup = BeautifulSoup(r.text,'html.parser')
        container = soup.find('div',{'class':'hl-rb-search hl-marg-right50 clearfix'}) #搜大框

        test1 = container.find_all('div',{'class':'hl-item-div'}) #爬結果
        if test1:
            page = container.find_all('li',{'class':'hl-hidden-xs'})
            try:
                self.maxpage = max([int(x.a.text) for x in [x for x in page if x.a]])#爬最大搜尋頁數
            except:
                pass
            for movie in test1:
                if '動漫' in movie.find('p',{'class':'hl-item-sub hl-lc-1'}).em.text:
                    tag = movie.find('div',{'class':'hl-item-content'})
                    title ,link= tag.a['title'],self.urlBase+tag.a['href']
                    if title not in self.finallst.keys() and fuzz.partial_ratio(self.search,title)>=80:
                        self.finallst[title] = link
                    pass
                else:
                    pass
        else:
            return dict(sorted(self.finallst.items()))

        if self.maxpage>1:
            self.serachLoop()
        return dict(sorted(self.finallst.items()))
    
    def serachLoop(self):
        if self.maxpage>2:
            for i in range(2,self.maxpage+1):
                urlSubSearch = f'https://123kubo.tv/search/page/{i}/wd/{self.search}.html'
                #爬蟲
                self.crawlSub(urlSubSearch)
        elif self.maxpage == 2:
            urlSubSearch = f'https://123kubo.tv/search/page/2/wd/{self.search}.html'
            self.crawlSub(urlSubSearch)
            #爬蟲

    def crawlSub(self,url):#爬分頁
        r = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(r.text,'html.parser')
        container = soup.find('div',{'class':'container'}) #搜大框
        test2 = container.find_all('div',{'class':'hl-item-div'}) #爬結果
        if test2:
            for movie2 in test2:
                if '動漫' in movie2.find('p',{'class':'hl-item-sub hl-lc-1'}).em.text:
                    tag = movie2.find('div',{'class':'hl-item-content'})
                    title ,link= tag.a['title'],self.urlBase+tag.a['href']
                    if title not in self.finallst.keys() and fuzz.partial_ratio(self.search,title)>=80:
                        self.finallst[title] = link
                    pass
                else:
                    pass
        else:
            return self.finallst

    def printrst(self) -> str:
        for k,v in sorted(self.finallst.items(),key=lambda x : x[0]):
            print(k+'\t'+v)
    def getrst(self):
        return sorted(self.finallst)
if __name__ == '__main__':
    animeSearch = KuboSearch(input())
    animeSearch.crwalMain()
    animeSearch.printrst()
