
import time
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class kktvSearch:
    
    def __init__(self, search:str,driver):
        self.search = search
        self.search_url = f"https://www.kktv.me/search/{self.search}"
        self.location_lst = []
        self.finallst = {}
        self.driver = driver

    def crawlkktv(self):
        self.driver.get(self.search_url)
        time.sleep(0.5)
        all_name = self.driver.find_elements_by_class_name('desc-title')
        time.sleep(0.5)

        for i in range(len(all_name)):
            if fuzz.partial_ratio(self.search.lower(), all_name[i].text.lower()) >= 70:
                self.location_lst.append(i)

        
        all_a = self.driver.find_elements_by_class_name('cover-view__img')
        time.sleep(0.5)

        for i in self.location_lst:
            self.finallst[all_name[i].text]=all_a[i].get_attribute('href')

        #self.driver.close()
        return dict(sorted(self.finallst.items()))

if __name__ == '__main__':
    option = Options()
    option.add_argument('--headless')
    driver = webdriver.Chrome('D:\crawler_final\webcrawl\chromedriver.exe',options=option)    
    kktvAnime = kktvSearch(input(),driver)
    x = kktvAnime.crawlkktv()
    print(x)

