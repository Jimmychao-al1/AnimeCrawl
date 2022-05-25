##gimy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fuzzywuzzy import fuzz
class GrimySearch:
    def __init__(self,search:str,driver) -> None:
        self.search = search
        self.driver = driver
        self.finallst = {}
    def GrimyCrawl(self):
        self.driver.get(f"https://gimy.app/search/-------------.html?wd={self.search}")
        all_name = self.driver.find_elements(By.TAG_NAME,"a")
        for name in all_name:
            title = name.text
            if self.search in title and fuzz.partial_ratio(self.search,title)>=80:
                href = name.get_attribute("href")
                if title not in self.finallst.keys():
                    self.finallst[title] = href
        self.driver.close()
        return dict(sorted(self.finallst.items()))

if __name__ == '__main__':
    option = Options()
    option.add_argument('--headless')
    driver = webdriver.Chrome('D:\crawler_final\crawl\chromedriver.exe',options=option)
    a = GrimySearch(input(),driver)
    a.GrimyCrawl()
    pass