
import requests
from bs4 import BeautifulSoup
class AnigamerContent:
    def __init__(self,url:str) -> None:
        self.url = url
        self.finallst = {'簡介':'','STAFF':'','上架日期':'','集數':''} #動畫詳細資訊
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

    def CrawlContent(self):
        r = requests.get(self.url,headers=self.headers)
        soup = BeautifulSoup(r.text,'html.parser')
        content = soup.select('#BH_background > div.container-player')
        base_data = content[0].select('div.anime-title')
        time = base_data[0].select_one('div.anime-option > section.videoname > div.anime_name > div > p')
        num = base_data[0].select(' div.anime-option > section.season > ul > li')
        supervisor = base_data[0].select_one(' div.anime-option > ul > li:nth-child(3)')
        supertitle = supervisor.span.text
        e = len(supertitle)
        try:
            self.finallst['上架日期'] = time.text.split('：')[1]
        except:
            pass
        try:
            self.finallst['集數'] = str(max([int(i.text) for i in num if i.text.isdigit()]))
        except:
            pass
        try:
            self.finallst['STAFF'] = supertitle + ':' + supervisor.text[e:]
        except:
            pass
        desciption = content[0].select('section.data > div.data_intro > p')
        try:
            self.finallst['簡介'] = ' '.join(desciption[0].text.split())
        except:
            pass
        return self.finallst


if __name__ == '__main__':  
    a = AnigamerContent('https://ani.gamer.com.tw/animeVideo.php?sn=10849')
    ans = a.CrawlContent()
    for i,j in ans.items():
        print(i,j)
'''href = anime_item.select_one('a').get('href')
            title = anime_item.select_one('.theme-info-block > p').text
            print(title , href )'''
