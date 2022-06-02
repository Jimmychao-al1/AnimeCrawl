import requests
from bs4 import BeautifulSoup

class MyselfContent:
    def __init__(self,url:str) -> None:
        self.url = url
        self.finallst = {'簡介':'','STAFF':'','上架日期':'','集數':''}
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }
        pass
    
    def CrawlContent(self):
        s = len(' 全 ')
        e = len(' 話')
        r = requests.get(self.url,headers=self.headers)
        soup = BeautifulSoup(r.text,'html.parser')
        content = soup.select('#ct > div:nth-child(3) > div.info_box.fl > div > div.info_info')
        data = content[0].select('ul > li') #上架日期
        self.finallst['上架日期'] = data[1].text.split(':')[1].strip()
        x =data[2].text.split(':')[1]
        if x.strip() != '未知':
            self.finallst['集數'] = x[s:-e]
        else:
            self.finallst['集數'] = '未知'
        self.finallst['STFF'] = data[3].text
        self.finallst['簡介'] = content[0].select('#info_introduction > p')[0].text
        #print(self.finallst)
        return self.finallst
        

    def printrst(self) -> str:
        for k,v in sorted(self.finallst.items(),key=lambda x : x[0]):
            print(k+'\t'+v)

if __name__ == '__main__':
    MyselfAnime = MyselfContent('https://myself-bbs.com/thread-48426-1-1.html')
    MyselfAnime.CrawlContent()
