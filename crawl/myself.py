import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
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
        pass
    
    def crawlMyself(self):
        self.getRedirectUrl()
        r2 = requests.get(self.redirect,headers=self.headers)
        soup = BeautifulSoup(r2.text,'html.parser')
        findpage =  soup.find_all("div",{'class':'pg'})
        #getmaxpage
        try:
            self.maxpage = max([int(x.span.text.strip().split()[1]) for x in [x for x in findpage if x.span]])
        except:
            pass    
        #crawhomepage
        test = soup.find_all('li',{'class':'pbw'})
        for i in test:
            tag = i.a.text
            if (tag not in self.finallst.keys()) and (fuzz.partial_ratio(self.search,tag)>=80):
                    self.finallst[i.a.text]=self.urlBase+i.a['href']
        #crawallsubpage
        if self.maxpage > 1 :
            self.crawlSubpage()
        return dict(sorted(self.finallst.items()))

    def getRedirectUrl(self):
        r = requests.post(self.urlSearch,data=self.my_data,allow_redirects=False)
        self.redirect = self.urlBase + str(r.headers.get('location'))
        pass

    def crawlSubpage(self):
        kindex = self.redirect.index('k')
        self.redirect = self.redirect[:kindex]+'page='
        for pagenum in range(2,self.maxpage+1):
            self.redirect+=str(pagenum)
            r = requests.get(self.redirect,headers=self.headers)
            soup = BeautifulSoup(r.text,'html.parser')
            test = soup.find_all('li',{'class':'pbw'})
            for i in test:
                tag_ = i.a.text
                if tag_ not in self.finallst.keys() and fuzz.partial_ratio(self.search,tag_)>=80: 
                    self.finallst[i.a.text]=self.urlBase+i.a['href']
        pass
    def printrst(self) -> str:
        for k,v in sorted(self.finallst.items(),key=lambda x : x[0]):
            print(k+'\t'+v)

if __name__ == '__main__':
    MyselfAnime = MyselfSearch(input())
    MyselfAnime.crawlMyself()
    MyselfAnime.printrst()
