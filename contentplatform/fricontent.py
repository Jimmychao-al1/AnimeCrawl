import requests
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
class FridayContent:
    def __init__(self, url : str):
        self.url = url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }
        self.finallst = {'簡介':'','STAFF':'','上架日期':'','集數':''}
        
        
    def CrawlContent(self):
        r = requests.get(self.url,headers=self.headers)
        soup = BeautifulSoup(r.text,'html.parser')                  
        data = soup.select('body > header > div.header-content > div.header-text > div')
        x = data[0].select(' div.director-actors.table-display > div')
        supervisor = []
        for i in x :
            title = i.select_one('div > p').text
            name = i.select_one('div:nth-child(2) > p > a > em').text
            supervisor.append(title+name)
        num = data[0].select('h6:nth-child(4)')
        time = data[0].select('h6:nth-child(5)')
        des = data[0].select('div.header-text > div > p')
        try:
            self.finallst['STAFF'] = ','.join(supervisor)
        except:
            pass
        try:
            self.finallst['上架日期'] = time[0].text.split('|')[0].strip()
        except:
            pass
        try:
            self.finallst['集數'] = num[0].text[1:-1]
        except:
            pass
        try:
            self.finallst['簡介'] = des[0].text
        except:
            pass
        #print(self.finallst)
        return self.finallst

if __name__ == '__main__':
    FridayAnime = FridayContent('https://video.friday.tw/movie/detail/22313')
    a = FridayAnime.CrawlContent()
    for i,j in sorted(a.items(),key=lambda x :x[0]):
        print(i,j)



