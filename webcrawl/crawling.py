from webplatform import anigamer,kktv,kubo,friday,grimy,linetv,hami,myself

import contentplatform.anicontent as anc
import contentplatform.fricontent as fric
#import contentplatform.kktvcontent as kktvc
import contentplatform.linetvcontent as linec
import contentplatform.myselfcontent as myc

from typing import Dict, List
class Crawl:
    def __init__(self,search:str) -> None:
        
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        option = Options()
        option.add_argument('--headless')
        self.driver = webdriver.Chrome('D:\crawler_final\webplatform\chromedriver.exe',options=option)
        self.kubo = self.myself = self.friday \
            = self.kktv = self.linetv = self.grimy = self.anigamer ={}
        self.hami = {}
        self.platformlst = ['kubo','myself','friday','anigamer','grimy']
        self.search = search
        self.result_dict = {}

    
    def AnimePlatform(self,platform:str):
        if platform == 'kubo':
            self.kubo = kubo.KuboSearch(self.search).crwalMain()
        elif platform == 'myself':
            self.myself = myself.MyselfSearch(self.search).crawlMyself()
        elif platform == 'friday':
            self.friday =friday.FridaySearch(self.search).Fridaycrawl()
        elif platform == 'anigamer':
            self.anigamer = anigamer.AnigamerSearch(self.search).AnigamerCrawl()
        elif platform == 'grimy':
            self.grimy = grimy.GrimySearch(self.search).GrimyCrawl()

    def CrawlAll(self):
        from concurrent import futures
        import time
        with futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.AnimePlatform,self.platformlst)
        self.kktv = kktv.kktvSearch(self.search,self.driver).crawlkktv()
        time.sleep(0.5)
        self.linetv = linetv.LineSearch(self.search,self.driver).LineCraw()
        time.sleep(0.5)
        self.hami = hami.HamivideoSearch(self.search,self.driver).Hamivideocrawl()

    def Outputchoose(self):
        self.CrawlAll()
        #anigamer
        choose_lst = list(self.anigamer.keys())
        #myself
        from fuzzywuzzy import fuzz
        for i in self.myself.keys():
            if i not in choose_lst:
                for j in choose_lst:
                    if fuzz.partial_ratio(i,j)>=80:
                        break
                else:
                    choose_lst.append(i)
        #friday
        for i in self.friday.keys():
            if i not in choose_lst:
                for j in choose_lst:
                    if fuzz.partial_ratio(i,j)>=80:
                        break
                else:
                    choose_lst.append(i)

        for i in self.kubo.keys():
            if i not in choose_lst:
                for j in choose_lst:
                    if fuzz.partial_ratio(i,j)>=80:
                        break
                else:
                    choose_lst.append(i)

        for i in self.kktv.keys():
            if i not in choose_lst:
                for j in choose_lst:
                    if fuzz.partial_ratio(i,j)>=80:
                        break
                else:
                    choose_lst.append(i)

        for i in self.linetv.keys():
            if i not in choose_lst:
                for j in choose_lst:
                    if fuzz.partial_ratio(i,j)>=80:
                        break
                else:
                    choose_lst.append(i)
                pass
        
        for i in self.hami.keys():
            if i not in choose_lst:
                for j in choose_lst:
                    if fuzz.partial_ratio(i,j)>=80:
                        break
                else:
                    choose_lst.append(i)
                pass

        for i in self.grimy.keys():
            if i not in choose_lst:
                for j in choose_lst:
                    if fuzz.partial_ratio(i,j)>=80:
                        break
                else:
                    choose_lst.append(i)
                pass
        #print(sorted(choose_lst))
        return choose_lst 
    
    def platform(self,actualsearch:str)->Dict:
        for i in self.anigamer.keys():
            if i == actualsearch:
                self.result_dict['巴哈姆特動畫瘋'] = self.anigamer[i]
                break
        for i in self.myself.keys():
            if i == actualsearch:
                self.result_dict['myself'] = self.myself[i]
                break
        #friday
        for i in self.friday.keys():
            if i == actualsearch:
                self.result_dict['friday'] = self.friday[i]
                break

        for i in self.kubo.keys():
            if i == actualsearch:
                self.result_dict['kubo'] = self.kubo[i]
                break

        for i in self.kktv.keys():
            if i == actualsearch:
                self.result_dict['kktv'] = self.kktv[i]
                break

        for i in self.linetv.keys():
            if i == actualsearch:
                self.result_dict['linetv'] = self.linetv[i]
                break

        for i in self.grimy.keys():
            if i == actualsearch:
                self.result_dict['grimy'] = self.grimy[i]
                break

        for i in self.hami.keys():
            if i == actualsearch:
                self.result_dict['hami'] = self.hami[i]
                break
        return self.CrawInform()
        #回傳結果 -> self.Information & self.CrawInform
    
    def CrawInform(self):
        if self.result_dict:
            for i,j in self.result_dict.items():
                if i == '巴哈姆特動畫瘋' : return anc.AnigamerContent(j).CrawlContent() #anigamer
                elif i == 'myself' :  return myc.MyselfContent(j).CrawlContent()  #myself
                elif i == 'friday' : return fric.FridayContent(j).CrawlContent() #friday
                elif i == 'linetv' : return linec.LineContent(j).CrawlContent() #linetv
                elif i == 'kktv' : pass #kktv
                elif i == 'kubo' : pass #kubo 內容亂七八糟 也無法爬
                elif i == 'grimy' : pass #grimy 內容亂
                elif i == 'hami' : pass #hami 
        pass




if __name__ == '__main__':
    import sys
    print(sys.path)
    c = Crawl(input())
    c.Outputchoose()
    y = c.platform('刀劍神域 Sword Art Online')
    print(c.myself)
    print(y)
    url = ''
    pass