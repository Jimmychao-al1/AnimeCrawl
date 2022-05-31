import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import time
import concurrent.futures

class MyselfSearch:
    def __init__(self,search:str) -> None:
        self.search = search
        self.finallst = {}
        self.maxpage = 0
        self.urlBase = 'https://myself-bbs.com/'
        self.urlSearch ='https://myself-bbs.com/search.php?mod=forum'
        self.redirect = ''
        self.headers = {
            'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        self.my_data = {
            'formhash':'e5ea8494',
            'srchtxt':f'{search}',
            'searchsubmit' : 'yes'
        }
        self.time = 0
        pass
    
    def crawlMyself(self):
        self.getRedirectUrl()
        r2 = requests.get(self.redirect,headers=self.headers)
        soup = BeautifulSoup(r2.text,'html.parser')
        findpage =  soup.select("div > div.pgs.cl.mbm > div")
        #getmaxpage
        try:
            self.maxpage = max([int(x.span.text.strip().split()[1]) for x in [x for x in findpage if x.span]])
        except:
            pass    
        #crawhomepage
        test = soup.find_all('li',{'class':'pbw'})
        for i in test:
            tag:str = i.a.text
            tag = tag[:tag.index('【')]
            if (tag not in self.finallst.keys()):
                    self.finallst[tag]=self.urlBase+i.a['href']
        #crawallsubpage -> multithreading speedup
        if self.maxpage > 1 :
            
            kindex = self.redirect.index('k')
            urls = [f"{self.redirect[:kindex]}page={page}" for page in range(1, self.maxpage+1)]

            start_time = time.time()

            #同時建立及啟用10個執行緒
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxpage) as executor:
                executor.map(self.crawlSubpage,urls)
            end_time = time.time()

            self.time = end_time-start_time

        return dict(sorted(self.finallst.items()))

    def crawlSubpage(self,urls):
        r = requests.get(urls,headers=self.headers)
        soup = BeautifulSoup(r.text,'html.parser')
        test = soup.find_all('li',{'class':'pbw'})
        for i in test:
            tag:str = i.a.text
            tag = tag[:tag.index('【')]
            if (tag not in self.finallst.keys()):
                    self.finallst[tag]=self.urlBase+i.a['href']
        pass

    def getRedirectUrl(self):
        r = requests.post(self.urlSearch,data=self.my_data,allow_redirects=False)
        self.redirect = self.urlBase + str(r.headers.get('location'))
        pass


    def printrst(self) -> str:
        for k,v in sorted(self.finallst.items(),key=lambda x : x[0]):
            print(k+'\t'+v)

if __name__ == '__main__':
    MyselfAnime = MyselfSearch(input())
    MyselfAnime.crawlMyself()
    MyselfAnime.printrst()
    print(MyselfAnime.time)
