from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from operate_browser import *

# driver.find_element_by_xpath("//input[@id='kw']")
def main(driver,num,beginpage,type,phone,passwd):
    notin='\\/<>:\"|?*×\'·《》~…-'
    noin2=['简介', '课本', '答案', '通知书', '读本', '试卷','教材','电子版','PPT','ppt','成绩','市','日语','调研卷','手抄报','pdf','PDF']
    time.sleep(1)
    fulllogin(driver,phone,passwd)
    titles=[]
    try:
        if type>=7:
            driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[2]/button[2]").click()
        else:
            driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[2]/button[1]").click()
    except:
        pass
    time.sleep(1)
    try:
        driver.find_elements(By.XPATH,"//div[@class='privilege-item-container' or @class='privilege-item-container action']")[type-1].click()
    except:
        input('未找到该类型，请手动登录')
    time.sleep(2)
    for i in range(beginpage):
        driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div[2]/div[4]/div/button[@class='btn-next']").click()
        time.sleep(0.5)
    try:
        lines=[]
        with open('./removed/re'+str(type)+'.txt','r') as f:
            lines=f.readlines()
    except:
        pass    
    while 1:
        try:
            tasks=driver.find_elements(By.XPATH,"//div[@class='doc-wrapper']/div[@class='content']/div[@class='doc-row']")
            for task in tasks:
                newtitle=task.find_elements(By.XPATH,"div[@class='row-content']/div/span")[1].get_attribute('title')
                print('检查：',newtitle)
                flag=0
                for c in notin:
                    if c in newtitle:
                        flag=1
                        break
                # print('flag:',flag)
                for c in noin2:
                    if c in newtitle:
                        flag=1
                        break
                for line in lines:
                    if newtitle==line.strip():
                        flag=1
                jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')  # \uAC00-\uD7A3为匹配韩文的，其余为日文
                if jap.search(newtitle):
                    flag=1
                # print('flag:',flag,"len:",len(newtitle))
                if flag==0 and len(newtitle.spilt('.')[0])>=5:
                    print('添加：',newtitle)
                    titles.append(newtitle)
            if len(titles)>num:
                break
            else:
                try:
                    next=driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div[2]/div[4]/div/button[@class='btn-next']")
                    print(next.get_attribute('disabled'))
                    if next.get_attribute('disabled')=='true':
                        break
                    else:
                        next.click()
                        time.sleep(1)
                except:
                    pass
        except:
            pass
    print('获取到的标题数：',len(titles))
    return titles
