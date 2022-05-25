from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class LineSearch:
    def __init__(self,search:str,driver) -> None:
        self.search = search
        self.driver = driver
        self.finallst = {}
        pass
    def LineCraw(self):
        url = f"https://www.linetv.tw/search?action_value={self.search}&q={self.search}&source=SEARCH_BAR"
        self.driver.get(url)
        time.sleep(1)
        all_name = self.driver.find_elements(By.TAG_NAME,"a")
        for name in all_name:
            title = name.text
            if self.search in title:
                href = name.get_attribute("href")
                if href not in self.finallst.values():
                    self.finallst[title.split('\n')[-1]] = href
        #print(self.finallst)
        self.driver.close()
        return dict(sorted(self.finallst.items()))


if __name__ == '__main__':
    option = Options()
    option.add_argument('--headless')
    driver = webdriver.Chrome('D:\crawler_final\crawl\chromedriver.exe',options=option)
    a = LineSearch(input(),driver)
    print(a.LineCraw())
    
    pass

