import getnames
import get1
import upload as myup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from operate_browser import *
import pyttsx3
import sys
from selenium.webdriver.remote.remote_connection import LOGGER

# 此处填上自己的apikey
api_key_list=['sk-.....','','']
# 管理多个账号，此处填写百度文库账号
account=[
    {'phone':'','passwd':'','brotype':1},
    {'phone':'','passwd':'','brotype':2},
    {'phone':'','passwd':'','brotype':3},
]
# 这下面两个也要填，作为默认账号
phone=''
passwd=''
# 加启动配置
chrome_options = webdriver.ChromeOptions()
# 打开chrome浏览器
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
#chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])#实现了规避监测
chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])#上面两个可以同时设置
# chrome_options.add_argument('--headless') # 无头模式
# chrome_options.add_argument('--disable-gpu')  # 上面代码就是为了将Chrome不弹出界面
chrome_options.add_argument('--start-maximized')#最大化
# chrome_options.add_argument('--incognito')#无痕隐身模式
# chrome_options.add_argument("disable-cache")#禁用缓存
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('log-level=3')#INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0

edge_options = webdriver.EdgeOptions()
edge_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])#上面两个可以同时设置
edge_options.add_argument('--start-maximized')#最大化
edge_options.add_argument('disable-infobars')
edge_options.add_argument('log-level=3')#INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0

fire_option=webdriver.FirefoxOptions()
fire_option.add_argument('--start-maximized')#最大化
fire_option.add_argument('disable-infobars')
# fire_option.add_argument('log-level=3')#INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 

args = sys.argv
accountnum=0
apinum=0
api_key=api_key_list[apinum]
# 第一个参数是脚本本身的文件名，所以获取第二个参数
if len(args) > 1:
    arg1 = args[1]
    print('选择的账号是：', arg1)
    accountnum=int(arg1)-1
if len(args) > 2:
    apinum=int(args[2])-1
    print('选择的apikey是：', args[2])
    api_key=api_key_list[apinum]
def upaccount(index):
    global phone,passwd,brotype
    phone=account[index]['phone']
    passwd=account[index]['passwd']
    brotype=account[index]['brotype']
    print('当前账号是：',phone)

def getdriver(type):
    if type==1:
        return webdriver.Chrome(chrome_options=chrome_options)
    elif type==2:
        return webdriver.Firefox(options=fire_option)
    else :
        return webdriver.Edge(edge_options=edge_options)
type=1

titles=[]
titlenum=0

brotype=1

upaccount(accountnum)
# driver = webdriver.Chrome()
driver = getdriver(brotype)
driver.maximize_window()
def menu():
    print('0.获取已有标题\n1.获取标题\n2.获取文章\n3.格式转换\n4.上传文章\n5.登录\n6.更改赛道，当前赛道'+str(type)+'\n7.新开浏览器\n8.清除文章\n9.更改api_key,当前key:'+str(apinum+1)+'\n10.更改账号，当前账号：'+phone+'\n11.退出')
while 1:
    menu()
    choice=input('请输入你的选择：')
    if choice=='0':
        f=open('./titles.txt','r')
        titles=f.read().split('\n\n')
        type=int(titles[0])
        titles=titles[1:-1]
        titlenum=len(titles)
        print(titles)
    if choice=='1':
        titles=[]
        inputstr=input('请输入爬取数量：').split(' ')
        beginpage=1
        titlenum=int(inputstr[0])
        if(len(inputstr)==2):
            beginpage=int(inputstr[1])
        titles.extend(getnames.main(driver,titlenum,beginpage,type,phone,passwd))
        string=str(type)+'\n\n'
        print(titles)
        for title in titles:
            string+=title+'\n\n'
        f=open('./titles.txt','w')
        f.write(string)
        f.close()
    if choice=='2':
        for index in range(min(len(titles),titlenum)):
            print('正在获取第'+str(index+1)+'篇文章：'+titles[index])
            get1.gettxt(titles[index],type,api_key)
        engine = pyttsx3.init()  # 创建engine并初始化
        engine.say("文章生成完毕")
        engine.runAndWait()  # 等待语音播报完毕
    if choice=='3':
        src_path='D:\\Workspace\\openai\\newarticles\\'+str(type)
        filelist=os.listdir('D:\\Workspace\\openai\\newarticles\\'+str(type))
        for file in filelist:
            if file.endswith('.txt'):
                try:
                    filename=file[:-4]
                    os.system('pandoc -o \"'+src_path+'\\'+filename+'.docx\" \"'+src_path+'\\'+file+'\"')
                    os.system('del \"'+src_path+'\\'+file+'\"')
                except:
                    pass
        # os.system('newpan.sh '+str(type))
        pass
    if choice=='4':
        num=int(input('请输入上传数量：'))
        myup.main(driver,num,type,phone,passwd)
    if choice=='5':
        fulllogin(driver,phone,passwd)
        time.sleep(2)
        tracks=driver.find_elements(By.XPATH,"//div[@class='privilege-item-container' or @class='privilege-item-container action']")
        print('赛道总数',len(tracks))
        print(type,tracks[type-1])
        tracks[type-1].click()
    if choice=='6':
        type=int(input('请输入赛道：'))
    if choice=='7':
        try:
            driver.quit()
        except:    
            pass
        try:
            driver = getdriver(brotype)
            driver.maximize_window()   
        except:
            pass
    if choice=='8':
        src_path='D:\\Workspace\\openai\\newarticles\\'+str(type)
        filelist=os.listdir('D:\\Workspace\\openai\\newarticles\\'+str(type))
        try:
            for file in filelist:
                if file.endswith('.docx'):
                    filename=file.split('.')[0]
                    os.system('del \"'+src_path+'\\'+filename+'.docx\"')
            print('清除完毕')
        except Exception as e:
            print('清除失败',e)
    if choice=='9':
        apinum=int(input('请输入api_key序号：'))-1
        api_key=api_key_list[apinum]
    if choice=='10':
        accountnum=int(input('请输入账号序号：'))-1
        upaccount(accountnum)
    if choice=='23':
        src_path='D:\\Workspace\\openai\\newarticles\\'+str(type)
        filelist=os.listdir('D:\\Workspace\\openai\\newarticles\\'+str(type))
        for index in range(len(titles)):
            title=titles[index]
            print('正在获取第'+str(index+1)+'篇文章：'+title)
            get1.gettxt(title,type)
            os.system('pandoc -o \"'+src_path+'\\'+title+'.docx\" \"'+src_path+'\\'+title+'.txt\"')
            os.system('del \"'+src_path+'\\'+title+'.txt\"')
        engine = pyttsx3.init()  # 创建engine并初始化
        engine.say("文章生成并转换完毕")
        engine.runAndWait()  # 等待语音播报完毕