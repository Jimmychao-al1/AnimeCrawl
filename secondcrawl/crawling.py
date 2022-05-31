from webcrawl.kubo import KuboSearch
from webcrawl.myself import MyselfSearch
from webcrawl.friday import FridaySearch
from webcrawl.anigamer import AnigamerSearch
from webcrawl.kktv import kktvSearch
from webcrawl.grimy import GrimySearch
from webcrawl.linetv import LineSearch
from webcrawl.hami import HamivideoSearch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fuzzywuzzy import fuzz

def AnimeCraw(search :str):
    option = Options()
    option.add_argument('--headless')
    start_ = time.time()
    kubo_ = KuboSearch(search).crwalMain()
    
    myself_ = MyselfSearch(search).crawlMyself()
    
    friday_ =FridaySearch(search).Fridaycrawl()
    
    anigamer_ = AnigamerSearch(search).AnigamerCrawl()
    
    grimy_ = GrimySearch(search).GrimyCrawl()
    
    driver = webdriver.Chrome('D:\crawler_final\crawl\chromedriver.exe',options=option)
    kktv_ = kktvSearch(search,driver).crawlkktv()
    
    linetv_ = LineSearch(search,driver).LineCraw()
    
    hami_ = HamivideoSearch(search,driver).Hamivideocrawl()
    
    end_ = time.time()
    print('total=',end_-start_)
    return kubo_ , myself_ ,friday_,anigamer_,kktv_ , linetv_,grimy_,hami_

def Outputchoose(search:str):
    kubo , myself ,friday,anigamer,kktv , linetv,grimy,hami = AnimeCraw(search)
    #anigamer
    choose_lst = list(anigamer.keys())
    #myself
    for i in myself:
        if i not in choose_lst or (not fuzz.partial_ratio(i,search)>=70):
            choose_lst.append(i)
            pass
    #friday
    for i in friday:
        if i not in choose_lst or (not fuzz.partial_ratio(i,search)>=70):
            choose_lst.append(i)
            pass
    for i in kubo:
        if i not in choose_lst or (not fuzz.partial_ratio(i,search)>=70):
            choose_lst.append(i)
            pass
    for i in kktv:
        if i not in choose_lst or (not fuzz.partial_ratio(i,search)>=70):
            choose_lst.append(i)
            pass
    for i in linetv:
        if i not in choose_lst or (not fuzz.partial_ratio(i,search)>=70):
            choose_lst.append(i)
            pass
    return choose_lst

def CrawlAnimeContent(target:str):
    #crawl pv
    pv  =[]
    #crawl content: cv , story
    content = []
    return pv,content
