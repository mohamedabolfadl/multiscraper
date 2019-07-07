
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 22:26:29 2016

@author: Moh2
"""
#import numpy as np
#import matplotlib.pyplot as plt
from PIL import ImageGrab
from time import sleep
from time import gmtime, strftime
import numpy as np
import matplotlib.pyplot as plt
import csv
import telepot
import time
from selenium import webdriver
from bs4 import BeautifulSoup


TimeDifference = 6


telegram_token = '720588462:AAGAv3RGD5qdTDGiyBO9MGRTDeUgp6jWkR4'
telegram_id = 680621666

# Font 9 laptop
#wid = 34
#hei = 13
#spac_h= 18
#spac_w= 123
#xo   = 640
#yo   = 102
#sx0=593
#sy0=77
#sx1=1211
#sy1=243



# Font 11 monitor
wid = 42
hei = 14
spac_h= 21
spac_w= 150
xo   = 787
yo   = 190
sx0=740
sy0=163
sx1=1480
sy1=355

JPY =  [255, 255, 0]
AUD = [186, 85, 211]
CAD = [0, 255, 0]
NZD = [255, 140, 0]
CHF = [0, 255, 255]
USD = [105, 105, 105]
EUR = [30, 144, 255]
GBP = [220, 20, 60]
currencies =['USD', 'EUR', 'JPY', 'GBP', 'CAD', 'AUD', 'CHF', 'NZD']
matrix = [[0 for x in range(5)] for y in range(8)] 
def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def stra(s):
    try:
        str(s)
        return str(s)
    except ValueError:
        return ''
        
def assignS(s,ind,c):
    sl = list(s)
    sl[ind]=c
    return "".join(sl)

def insertS(s,ind,c):
    sl = list(s)
    fp = sl[:ind-1]
    sp = sl[ind-1:]
    re = []
    re.append(fp)
    re.append(c)
    re.append(sp)
    out = [item for sublist in re for item in sublist]
    return "".join(out)
        
def normalizeTm(s):
    st = stra(s)
    if st[len(st)-1]=='m':
        ind = st.find(':')
        dig = st[ind-2:ind]
        dig.replace(' ','')
        addTim = 0
        if st[len(st)-2]=='p':
            addTim = 12
        eut = int(dig)+TimeDifference+addTim
        chang = False
        if eut==24 and st[len(st)-2]=='p':
            
            st = assignS(st,len(st)-2,'a')
            chang = True
            
        else:
            if eut==12 and st[len(st)-2]=='a':
               st = assignS(st,len(st)-2,'p')


        if eut>12 and eut<25:
            eut = eut-12
            if not chang:            
              st = assignS(st,len(st)-2,'p')
        note = ''
        if eut>24:
            eut = eut -24
            note = '(next day)'
            st = assignS(st,len(st)-2,'a')
        euts = stra(eut)
        stl = list(st)
        stl[ind-2] = ' '
        stl[ind-1] = euts[0]
        if len(euts)>1:
            stl[ind-2] = euts[0]
            stl[ind-1] = euts[1]
        st="".join(stl)
        if int(dig)<10 and int(euts)>9:
             st=insertS(st,len(st)-6,' ')
        st=st+note
        return st
    else:
            return ''
            
def getCurrs(currs):
      cus=[]
      if 'u' in currs:
            cus.append('USD')
      if 'e' in currs:
            cus.append('EUR')
      if 'j' in currs:
            cus.append('JPY')
      if 'a' in currs:
            cus.append('AUD')
      if 'c' in currs:
            cus.append('CAD')
      if 'n' in currs:
            cus.append('NZD')
      if 'h' in currs:
            cus.append('CHF')
      if 'g' in currs:
            cus.append('GBP')
    
      return cus

def handle(msg):
    command = msg['text']
    cmds = command.split()
    #print cmds
    if len(cmds)==1 :
        if command == '/plot':
            sendPlots(["USD","EUR","JPY","GBP","CAD","AUD","CHF","NZD"],5,-1)
        if command == '/shot':
            sendStrengths()
    else:
        if len(cmds)==2 and cmds[0]=='/plot':
            sendPlots(getCurrs(cmds[1]),5,-1)
        else:
            if len(cmds)==3 and cmds[0]=='/plot':
                sendPlots(getCurrs(cmds[1]),int(cmds[2]),-1)
            else:
                if len(cmds)==4 and cmds[0]=='/plot':
                  sendPlots(getCurrs(cmds[1]),int(cmds[2]),int(cmds[3]))  

    if len(cmds)==2 and cmds[0]=='/news':
        curr_vec = getCurrs(cmds[1])
        sendNews(curr_vec[0])


def sendNews(t):
    
    link = "https://www.forexfactory.com/calendar.php"
    driver = webdriver.PhantomJS(executable_path='C:/Users/Mohamed Ibrahim/Box Sync/bot/selenium/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.set_window_size(50, 50)
    driver.get(link)
    s=BeautifulSoup(driver.page_source)
    driver.quit()
    
    # Load file
    #html_data = open("calff.html",'r').read()
    #s = BeautifulSoup( html_data)
    
    

    targ = t
    elements = s.findAll("tr",class_="calendar_row")
    mat = []
    currDt=[]
    #crrTm=[]
    for element in elements:
       
        # Currency
        curr = element.find("td", class_="calendar__cell calendar__currency currency")
        # Importance    
        imp = element.find("span", title=True, class_=True)
        # Title of the news    
        tit = element.find("span",  class_="calendar__event-title")
        # Actual
        act = element.find("td", class_="actual")
        # Better worse
        bw = act.findNext("span",class_=True)
        # Forecast
        forc = element.find("td", class_="forecast")
        # Previous    
        prev = element.find("td", class_="previous")
        # Time and date
        tm = element.findNext("td",class_="time")
        dt = element.findPrevious("td",class_="date")
        
        if dt:
         if len(dt.get_text())>3:
            currDt = dt.get_text()
            
         if len(tm.get_text())>3:
            currTm = tm.get_text()   
        if curr.get_text()==targ:
            mat.append( (stra(currDt)+" "+currTm,bw['class'][0],tit.get_text(),imp['class'][0],act.get_text(),forc.get_text(),prev.get_text() ) )
    
    inf=mat
    plt.figure()
    ax = plt.subplot(111)
    width = 0.5
    i=0
    pls = 0
    fv = []
    av = []
    pv = []
    relf = []
    relp = []
    cnt = []
    xlb = []
    Nstr=18
    cbetter = (0.01,0.95,0.01)
    cworse = (0.95,0.01,0.01)
    csame = (0.25,0.25,0.25)
    cunfound = (0.01,0.01,0.95)
    colors=[]
    while i<len(inf):
        
        c = inf[i]
        f = stra(c[5]).replace("%","").replace(" ","").replace("K","").replace("B","").replace("M","")
        p = stra(c[6]).replace("%","").replace(" ","").replace("K","").replace("B","").replace("M","")
        a = stra(c[4]).replace("%","").replace(" ","").replace("K","").replace("B","").replace("M","")
    
        
        if IsInt(stra(f).replace(".","")) and IsInt(stra(p).replace(".","")) and IsInt(stra(a).replace(".","")):
            fd = float(f)
            pd = float(p)
            ad = float(a)
            fv.append(fd)  
            av.append(pd)  
            pv.append(ad)  
            forecast_change = 0
            if fd != 0:
                forecast_change = 100.0*(ad-fd)/abs(fd)
            previous_change = 0
            if pd != 0:
             previous_change = 100.0*(ad-pd)/abs(pd)
            relf.append(forecast_change)
            relp.append(previous_change)
            
            cnt.append(pls)
            
            lb = stra(c[2])
            
            tm=stra(c[0])
            tm = normalizeTm(tm)
            lb=lb[:Nstr]+'\n'+tm[3:]
            
            xlb.append(lb)
            
            col = cunfound
            cond = stra(c[1])
            if cond[0]=='b':
                col = cbetter
            if cond[0]=='w':
                col = cworse
            if cond[0]=='s':
                col = csame
            if cond[0]=='b' and   forecast_change<0:
                forecast_change=-1*forecast_change
            if cond[0]=='w' and   forecast_change>0:
                forecast_change=-1*forecast_change   
                
            impcol = 'y'
            imp = stra(c[3])
            if imp[0]=='h':
                impcol='r'
            if imp[0]=='l':
                impcol='g'
            if imp[0]=='m':
                impcol='b'
            colors.append(impcol)
            
            plt.bar(pls, forecast_change ,width,  edgecolor =col,alpha=0.8,fill=False,linewidth=1, align='center')
            plt.bar(pls, previous_change, width, edgecolor =cunfound,alpha=0.3,fill=False,linewidth=1, align='center')
            ax.text(pls-0.25, 100+(pls%2)*50, stra(c[4])+'\n'+stra(c[5])+'\n'+stra(c[6]), fontsize=10,color=tuple([0.5*x for x in col]))
            pls = pls+1
            
        else:
    
            if  IsInt(stra(p).replace(".","")) and IsInt(stra(a).replace(".","")) :
                pd = float(p)
                ad = float(a)
                av.append(pd)  
                pv.append(ad)  
                previous_change = 0
                if pd != 0:            
                    previous_change = 100.0*(ad-pd)/abs(pd)
    
                relf.append(0)
                relp.append(previous_change)
                    
                cnt.append(pls)
    
                lb = stra(c[2])
                tm=stra(c[0])
                tm = normalizeTm(tm)
                lb=lb[:Nstr]+'\n'+tm[3:]
                xlb.append(lb)
                
                col = (0.9,0,0.9)
                cond = stra(c[1])
                if cond[0]=='b':
                    col = cbetter
                if cond[0]=='w':
                    col = cworse
                if cond[0]=='s':
                    col = csame
                
                if cond[0]=='b' and   previous_change<0:
                    previous_change=-1*previous_change
        
                if cond[0]=='w' and   previous_change>0:
                    previous_change=-1*previous_change            
                
                impcol = 'y'
        
                imp = stra(c[3])
                if imp[0]=='h':
                    impcol='r'
                if imp[0]=='l':
                    impcol='g'
                if imp[0]=='m':
                    impcol='b'
                    
                colors.append(impcol)
                
                plt.bar(pls, 0 ,width,  edgecolor =col,alpha=0.8,fill=False,linewidth=0, align='center')
                plt.bar(pls, previous_change, width, edgecolor =col,alpha=0.8,fill=False,linewidth=1, align='center')
                ax.text(pls-0.125, 100+(pls%2)*50, stra(c[4])+'\n'+stra(c[6]), fontsize=10,color=tuple([0.5*x for x in col]))
                pls = pls+1            
                
            else:
                
             if  stra(c[3])=='high':
                
                plt.bar(pls, forecast_change ,width,  edgecolor =col,alpha=0.8,fill=False,linewidth=0, align='center')
                lb = stra(c[2])
                tm=stra(c[0])
                tm = normalizeTm(tm)
                lb=lb[:Nstr]+'\n'+tm[3:]
                xlb.append(lb)
                colors.append('r')
                cnt.append(pls)
                pls = pls+1    
                
        i=i+1
       
    
    plt.ylim([-200,200])
    plt.xlim([-0.5,max(cnt)+1])
    plt.xticks(cnt, xlb, rotation='vertical', fontsize = 5)
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.15)
    
    for xtick, color in zip(ax.get_xticklabels(), colors):
        xtick.set_color(color)
    
    plt.grid()
    plt.title(targ)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
        
    plt.show()
    
    plt.savefig(targ+'_news.png')
    f = open(targ+'_news.png', 'rb')
    bot.sendPhoto(telegram_id,f)
    f.close()
    plt.close()    




def sendPlots(currencies,tfs,wind):
    
    #path = "C:/Users/Moh2/Desktop/scraping/strengths/27 Feb 17/"
    path = ""
    date=time.strftime("%d")
    #date=27
    
    plt.figure()
    ip=1
    while(ip<tfs+1):
        #plt.figure()
        plt.subplot(tfs,1,ip)  
        ic=1
        for curr in currencies:
            f= open(path+curr+'.csv', 'rb') 
            spamreader = csv.reader(f, delimiter=';', quotechar='|')
            tf = [] 
            dt=[]
            for row in spamreader:
                 tmp = row[0]
                 if((int(tmp[8:10])-int(date))==0):
                     tm = int(tmp[tmp.find(':')-2:tmp.find(':')])+float(tmp[tmp.find(':')+1:tmp.find(':')+5])/60.0
                     dt.append(tm)            
                     tf.append(row[ip])
            #print str(len(tf))
            if(ic<8):
                plt.plot(dt,tf,hold=True)
            else:
                plt.plot(dt,tf,color=(0.5,0.5,0.5))  
            ic = ic+1

    
        
        if(ip==tfs):    
            plt.legend(currencies)
    
        ip=ip+1
        plt.grid()         
    
    if wind>0:
        plt.xlim(dt[len(dt)-1]-wind,dt[len(dt)-1])
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.show()
    
    plt.savefig(str(date)+'_streng.png')
    f = open(str(date)+'_streng.png', 'rb')
    bot.sendPhoto(telegram_id,f)
    f.close()
    plt.close()

        
def sendStrengths():
    img=ImageGrab.grab()
    img.save("strength.png","PNG")
    f = open("strength.png", 'rb')
    bot.sendPhoto(telegram_id,f)
    f.close()
def get_main_color(img):
    colors = img.getcolors(256) #put a higher value if there are many colors in your image
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present
    except TypeError:
        raise Exception("Too many colors in the image")


def detectCurr(r):
    # USD EUR JPY GBP CAD AUD CHF NZD
    dist = [abs(r[0]-USD[0])+abs(r[1]-USD[1])+abs(r[2]-USD[2]),abs(r[0]-EUR[0])+abs(r[1]-EUR[1])+abs(r[2]-EUR[2]),abs(r[0]-JPY[0])+abs(r[1]-JPY[1])+abs(r[2]-JPY[2]),abs(r[0]-GBP[0])+abs(r[1]-GBP[1])+abs(r[2]-GBP[2]),abs(r[0]-CAD[0])+abs(r[1]-CAD[1])+abs(r[2]-CAD[2]),abs(r[0]-AUD[0])+abs(r[1]-AUD[1])+abs(r[2]-AUD[2]),abs(r[0]-CHF[0])+abs(r[1]-CHF[1])+abs(r[2]-CHF[2]),abs(r[0]-NZD[0])+abs(r[1]-NZD[1])+abs(r[2]-NZD[2]),]
    return dist.index(min(dist))
    
bot = telepot.Bot(telegram_token)
bot.message_loop(handle)


while 1:   


    sleep(3)


    
