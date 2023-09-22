from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import win32gui
import win32con
import os
import shutil
def getpagetype(driver):
    try:
        yan=driver.find_element(By.XPATH,"//div[@class='mod-vcodes']/div/p[text()='安全验证']")
        if yan:
            driver.find_element(By.XPATH,"//div[@class='vcode-close']").click()
            time.sleep(2.34)
            driver.find_element(By.XPATH,"//div/form/p/input[@value='登录']").click()
            return 'yanzheng'
    except:
        pass
    try:
        driver.find_element(By.XPATH,"//div/div/p[@class='pass-form-logo']")
        return 'login'
    except:
        pass
    try:
        driver.find_element(By.XPATH,"//main/div/div/div/div/div[@class='title']")
        return 'I_know'
    except:
        pass
    try:
        if 'none'in driver.find_element(By.XPATH,"//main/div/div/div[@class='el-dialog__wrapper']/div/div/div[text()='温馨提示']").find_element(By.XPATH,"../../..").get_attribute("style"):
            return 'task'
    except:
        pass
    try:
        if 'none' not in driver.find_element(By.XPATH,"//main/div/div/div[@class='el-dialog__wrapper']/div/div/div[text()='温馨提示']").find_element(By.XPATH,"../../..").get_attribute("style"):
            return 'repeat'
    except:
        pass
    try:
        if driver.find_element(By.XPATH,"//body/div/div[@class='upload-success-list-wrap']/div[@class='upload-dialog-wrap']"):
            return 'upload_success'
    except:
        pass
    # try:
    #     if driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div/div[3]/div[2]/button/span"):
    #         return 'upload'
    # except:
    #     pass     
    try:
        if driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div/div[3]/div[2]/button/span[text()='确认提交']"):
            return 'waiting_commit'
    except:
        pass
    return "none"

def login(driver,phone,passwd):
    try:
        driver.find_element(By.XPATH,"//div/div/p[@title='用户名登录']").click()
        driver.find_element(By.XPATH,"//div/form/p/input[@name='userName']").send_keys(phone)
        driver.find_element(By.XPATH,"//div/form/p/input[@name='password']").send_keys(passwd)
        driver.find_element(By.XPATH,"//div/form/p/input[@value='登录']").click()
    except:
        pass
    
def success_num(driver):
    try:
        num=int(driver.find_element(By.XPATH,"/html/body/div/div/div/div[2]/div[1]/div/span").text.split('（')[1].split('篇')[0])
        return num
    except:
        return -1
def I_know(driver):
    try:
        but=driver.find_element(By.XPATH,"//main/div/div/div/div/span/button/span[text()='我知道啦']")
        but.click()
    except:
        pass
    try:
        driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[3]/div/div/div[1]/button").click()
    except:
        pass

def confirm_submit(driver):
    try:
        cells=driver.find_elements(By.XPATH,"//div[@class='cell']/div/div/div/div/input")
        artlist=[cell.get_attribute('value') for cell in cells]
        driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div/div[3]/div[2]/button/span").click()
        print('confirm_submit',artlist)
        return artlist
    except:
        pass
def repeat(driver):
    try:
        ps=driver.find_elements(By.XPATH,"//main/div/div/div/div/div[@class='el-dialog__body']/p")
        repeatname=[x.text for x in ps]
        return repeatname
    except:
        print('get repeat wrong')
        return []

def confirm(dirver):
    try:
        dirver.find_elements(By.XPATH,"//main/div/div/div/div/div[@class='el-dialog__footer']/span/button[@class='el-button el-button--primary']/span[text()='确认']")[1].click()
    except:
        pass
def upload(driver,articles,type):
    try:
        # print(articles)
        driver.find_element(By.XPATH,"//div/div[@type='primary'and text()='批量上传\n                        ']").click()
        time.sleep(0.1)
        dialog = win32gui.FindWindow('#32770', None)
        time.sleep(0.1)
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        time.sleep(0.1)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        time.sleep(0.1)
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)
        time.sleep(0.1)
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)
    # 跟上面示例的代码是一样的，只是这里传入的参数不同，如果愿意可以写一个上传函数把上传功能封装起来
        time.sleep(0.1)
        src_path="d:\\Workspace\\openai\\newarticles\\"+str(type)+"\\"
        string=''
        for article in articles:
            string+='\"'+src_path+article+'\"'+' '
        print(string)
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, 0, string)
    
    # win32gui.SendMessage(Edit, win32con.WM_SETTEXT, 0, '"d:\\Workspace\\openai\\snewarticles\\1\\test1.txt" "d:\\Workspace\\openai\\snewarticles\\1\\test2.txt" ')
    
        time.sleep(2)
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
        print('上传完成')
    except:
        pass

def geterrs(driver):
    try:
        err_arts=[]
        cells=driver.find_elements(By.XPATH,"//tbody/tr[@class='el-table__row']/td[2]/div[@class='cell']")
        for cell in cells:
            if cell.find_element(By.XPATH,"div/div/div/div[@class='error-tip']"):
                err_arts.append(cell.find_element(By.XPATH,"div/div/div/div/input").get_attribute('value'))
        return err_arts
    except Exception as e:
        print('get err wrong',e)
def fulllogin(driver,phone,passwd):
    url = "http://cuttlefish.baidu.com/shopmis?_wkts_=1671963555694#/taskCenter/majorTask"
    driver.get(url)
    while 1:
        page=getpagetype(driver)
        print('in page:'+page)
        if page=='login':
            login(driver,phone,passwd)
            time.sleep(4)
        if page=='I_know':
            I_know(driver)
        if page=='task':
            time.sleep(4)
            if getpagetype(driver)=='task':
                print('in page task confirmed ')
                break
        time.sleep(1)
