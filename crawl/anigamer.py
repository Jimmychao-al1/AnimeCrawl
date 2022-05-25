
import requests
from bs4 import BeautifulSoup

class AnigamerSearch:
    def __init__(self,search:str) -> None:
        self.search = search
        self.finallst = {}
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
}
        self.urlBae = 'https://ani.gamer.com.tw/'
        self.mydata = {
            'kw' : f'{search}'
        }

    def AnigamerCrawl(self):
        url = self.GetPostResult()
        r = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(r.text,'html.parser')
        theme_list = soup.select_one('.animate-theme-list:not(.animate-wish)')
        anime_lst = theme_list.select('.theme-list-block > .theme-list-main') 
        for anime_item in anime_lst:
            href = self.urlBae+anime_item["href"]
            title = anime_item.select_one('.theme-info-block > p').text
            if title not in self.finallst.keys():
                self.finallst[title] = href
        return dict(sorted(self.finallst.items()))

    def GetPostResult(self):
        r = requests.post('https://ani.gamer.com.tw/search.php',data=self.mydata,headers = self.headers,allow_redirects=False)
        return self.urlBae+str(r.headers.get('Location'))

if __name__ == '__main__':
    a = AnigamerSearch(input())
    ans = a.AnigamerCrawl()
    for i,j in ans.items():
        print(i,j)
'''href = anime_item.select_one('a').get('href')
            title = anime_item.select_one('.theme-info-block > p').text
            print(title , href )'''