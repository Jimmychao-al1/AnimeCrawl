import requests
from bs4 import BeautifulSoup
import json
class LineContent:
    def __init__(self,url : str) -> None:
        self.url = url
        self.finallst = {'簡介':'','STAFF':'','上架日期':'','集數':''}
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }
        pass
    def CrawlContent(self):
        r = requests.get(self.url,headers=self.headers)
        print(r)
        soup = BeautifulSoup(r.text,'html.parser')
        data = soup.select('script')
        s = len('window.__INITIAL_STATE__ = ')
        x_dict = json.loads(data[0].text[s:])
        info = x_dict['entities']['dramaInfo']
        y = list(info['byId'].values())[0]
        try:
            self.finallst['STAFF'] = y['actors'][0]['name']
        except:
            pass
        try:
            self.finallst['上架日期'] = y['year']
        except:
            pass
        try:
            self.finallst['簡介'] = y['introduction']
        except:
            pass
        try:
            self.finallst['集數'] = y['current_eps']
        except:
            pass
        #print(self.finallst)
        return self.finallst


if __name__ == '__main__':
    a = LineContent('https://www.linetv.tw/drama/10844/eps/1?drama_id=10844&source=SEARCH_RESULT_PAGE')
    print(a.CrawlContent())
    
    pass

