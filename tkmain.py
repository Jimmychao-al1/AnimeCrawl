# -*- coding: utf-8 -*-
from  tkinter import* 
import webbrowser
from webcrawl.crawling import Crawl
import tkinter.font as tkFont
from ctypes import windll

#建立主視窗
win = Tk()
windll.shcore.SetProcessDpiAwareness(2)# 2 -> 清晰 但是螢幕小 , 3->模糊 螢幕大
win.title("動畫資訊")
win.geometry("650x900+400+0") #大小:寬x高/視窗出現座標
win.resizable(0,0) #不可縮放
bgimg = PhotoImage(file = "D:\\crawler_final\\background.png") #背景
canvas1 = Canvas(win, width = 200,height = 200)  
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( -50, -100, image = bgimg, anchor = "nw")
win.attributes("-topmost",True) #置頂

#title
canvas1.create_text( 325,75, text = "動 畫 搜 尋\n",font = tkFont.Font(family='Constantia',size=25,weight='bold'))
#input box
canvas1.create_text( 100,100, text = "我想看...",font = tkFont.Font(family='Constantia',size=18,weight='bold'))
en = Entry(bd = 5, font = "Constantia 18") #輸入
canvas1.create_window( 325, 100, window = en, width = 300)
holder_list = []
tag = False
#search
def search():
    #刪除先前結果未處理
    inp = en.get()
    global c
    c = Crawl(inp)
    option = c.Outputchoose()
    #傳出inp(str) 傳入option(list)
    message = canvas1.create_text( 325,150, text = "是哪一個勒?",font = tkFont.Font(family='Constantia',size=18,weight='bold'))
    #option = ['刀劍神域 Alicization', '刀劍神域 Alicization War of Underworld', '刀劍神域 Alicization War of Underworld -THE LAST SEASON-', '刀劍神域 Alternative GGO', '刀劍神域 Extra Edition', '刀劍神域 Progressive', '刀劍神域 Sword Art Online', '刀劍神域 Sword Art Online 第二季', '刀劍神域 劇場版 序列爭戰', '刀劍神域 愛麗絲篇', '刀劍神域 特別篇 Extra Edition', '刀劍神域外傳 Gun Gale Online', '刀劍神域外傳GGO', '刀劍神域第1季', '刀劍神域：序列之爭']
    #select
    def select():
        selection = var.get()
        #傳出所選選項-> selection
        for i in holder_list:
            i.destroy()
        canvas1.delete(message)
        canvas1.create_text( 325,150, text = selection, font = tkFont.Font(family='Constantia',size=22,weight='bold'))   
        outp(c,selection)
    #顯示選項
    n = 150
    var = StringVar()
    #var.set(option)
    #b1 = Button(win, text='selection', width=15, height=2, command=select, font = "Constantia 15",bg='papayawhip')
    #canvas1.create_window(325, n, window = b1)
    #b1.pack()
    #lb = Listbox(win, listvariable=var)
    #canvas1.create_window(325, n+40, window = lb)
    #lb.pack()
    for i in option:
        bu = Radiobutton(win, text = i, variable = var, value = i, command = select)
        n += 40
        canvas1.create_window(325, n, window = bu)
        holder_list.append(bu)


def callback(url):
    webbrowser.open_new(url)

def outp(c:Crawl,actualsearch:str):
    #傳入out1(str)"預告片連結"、out2(dic){簡介:text,staff:text,上架日期:text,集數:text}、out3(dic){播放平台:連結,...}
    #out1 = "https://www.youtube.com/watch?v=F6q1p-qXtpo"
    out2 = c.CrawlContent(actualsearch)
    out3 = c.result_dict #播放連結及平台
    
    #out1
    #canvas1.create_text( 325,185,text = "___預告片連結___",font = "Consolas 15")
    #pv_linkbtn = Button(text = out1, font = "Consolas 10", command = lambda: pv_linkbtn.config(callback(out1)))
    #canvas1.create_window( 325, 220, win = pv_linkbtn)
    #out2
    #簡介
    intro = [] #簡介換行
    word = 0
    count = 0
    for i in out2["簡介"]:
        intro.append(i)
        word += 1
        if word == 40:
            if count == 7:
                intro.append("...")
                break
            intro.append("\n")
            word = 0
            count += 1
    canvas1.create_text( 325,200,text = "_____簡介_____",font = tkFont.Font(family='Constantia',size=15,weight='bold'))
    canvas1.create_text( 325,290,text = "".join(intro), font = "Consolas 12")
    #staff
    canvas1.create_text( 325,375,text = "_____STAFF_____",font = tkFont.Font(family='Constantia',size=15,weight='bold'))
    n = 420
    word = 0
    for i in out2["STAFF"].split(","):
        if word == 0:
            canvas1.create_text( 150,n,text = i,font = tkFont.Font(family='Candara',size=14,weight='bold'))
            word += 1
        elif word == 1:
            canvas1.create_text( 350,n,text = i,font = tkFont.Font(family='Candara',size=14,weight='bold'))
            word += 1
        elif word == 2:
            canvas1.create_text( 550,n,text = i,font = tkFont.Font(family='Candara',size=14,weight='bold'))
            word = 0
            n += 30
    n += 30
    #上架日期
    canvas1.create_text( 200,n+10,text = "_____上架日期_____",font = tkFont.Font(family='Constantia',size=15,weight='bold'))
    canvas1.create_text( 200,n+30,text = out2["上架日期"],font = tkFont.Font(family='Candara',size=13,weight='bold'))

    #集數
    canvas1.create_text( 480,n+10,text = "_____集數_____",font = tkFont.Font(family='Constantia',size=15,weight='bold'))
    canvas1.create_text( 480,n+30,text = out2["集數"],font = tkFont.Font(family='Candara',size=15,weight='bold'))
    n += 70
    
    #out3
    canvas1.create_text( 325,n,text = "_____播放平台_____",font = tkFont.Font(family='Constantia',size=15,weight='bold'))
    word = 0
    n += 50
    for k,v in out3.items():
        if word == 0: 
            linkbtn = Button(text = k, font = "Consolas 15", command =  lambda v = v :linkbtn.config(callback(v)),bg='papayawhip')
            canvas1.create_window( 200, n, win = linkbtn)
            word = 1
        else:
            linkbtn = Button(text = k, font = "Consolas 15", command = lambda v = v:linkbtn.config(callback(v)),bg='papayawhip')
            canvas1.create_window( 480, n, win = linkbtn)
            word = 0
            n += 50    

#search_button
btnimg = PhotoImage(file = "D:\\crawler_final\\btn.png") #but底圖
btn = Button(text = "搜尋!", font = "Consolas 18", image = btnimg)
btn.config(command = search)
showbtn = canvas1.create_window( 560, 100, window = btn)


win.mainloop() #常駐主視窗
