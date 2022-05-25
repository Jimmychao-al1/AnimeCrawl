from .kubo import KuboSearch 
from .kktv import kktvSearch 
from .myself import MyselfSearch 
from .friday import FridaySearch
from .linetv import LineSearch
from .grimy import GrimySearch
from .anigamer import AnigamerSearch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def AnimeCraw(search :str):
    option = Options()
    option.add_argument('--headless')
    kubo_ = KuboSearch(search).crwalMain()
    myself_ = MyselfSearch(search).crawlMyself()
    friday_ =FridaySearch(search).Fridaycrawl()
    anigamer_ = AnigamerSearch(search).AnigamerCrawl()
    driver = webdriver.Chrome('D:\crawler_final\crawl\chromedriver.exe',options=option)
    kktv_ = kktvSearch(search,driver).crawlkktv()
    driver = webdriver.Chrome('D:\crawler_final\crawl\chromedriver.exe',options=option)
    linetv_ = LineSearch(search,driver).LineCraw()
    driver = webdriver.Chrome('D:\crawler_final\crawl\chromedriver.exe',options=option)
    grimy_ = GrimySearch(search,driver).GrimyCrawl()
    return kubo_ , myself_ ,friday_,anigamer_,kktv_ , linetv_,grimy_