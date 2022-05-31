#Class Hamivideo 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fuzzywuzzy import fuzz

class HamivideoSearch:
    def __init__(self, search:str,driver):
        self.search = search
        self.url_search = f"https://hamivideo.hinet.net/search.do?keyword={self.search}"
        self.driver = driver
        
    def Hamivideocrawl(self):
        self.driver.get(self.url_search)
        all_button = self.driver.find_elements(By.XPATH,
            "/html/body/div[@class='wrapper']/div[@class='title-wrapper memberType']/div[@class='tabArea sty_member']/ul/li")
        link_lst = []
        name_lst = []
        hamivideo_dict = {}
        for button in all_button:
            if button.text == "影劇":
                button.click() 
                time.sleep(0.5)
                #拿link
                links = self.driver.find_elements(By.CLASS_NAME,"alink")
                for link in links:
                    link_lst.append(link.get_attribute('href'))
                #拿名字
                names = self.driver.find_elements(By.CLASS_NAME,"title")
                for name in names:
                    name_lst.append(name.text)
                #整合在一起
                
                for a,b in zip(name_lst,link_lst):
                    if fuzz.partial_ratio(self.search.lower(),a.lower())>=70:
                        hamivideo_dict[a] = b
        #最後輸出   
    #    if hamivideo_lst == []:
    #        print("無")
    #    else:
    #        for i in hamivideo_lst:
    #            print(i)
        self.driver.close()
        return dict(sorted(hamivideo_dict.items()))
                
if __name__ == '__main__':
    my_options = Options()
    my_options.add_argument("--headless")#不開啓實體瀏覽器
    driver = webdriver.Chrome(options = my_options)
    a = time.time()
    Hamivideo = HamivideoSearch(input(),driver)
    ans = Hamivideo.Hamivideocrawl()
    b = time.time()
    print(b-a)
    print(ans)
    
