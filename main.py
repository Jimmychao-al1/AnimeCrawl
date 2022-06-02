from webcrawl.crawling import Crawl


if __name__ == '__main__':
    #target = input()
    c = Crawl('刀劍神域')
    choose_lst = c.Outputchoose()
    actualchoose = '刀劍神域 Sword Art Online'
    information = c.platform(actualchoose)
    platform_ = c.result_dict
    print(choose_lst)
    print(information)
    print(platform_)
    pass
