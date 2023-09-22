from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import win32gui
import win32con
import os
import shutil
from operate_browser import *
# driver.find_element_by_xpath("//input[@id='kw']")
def upremovetxt(files,type):
    try:
        inputname='./removed/re'+str(type)+'.txt'
        with open(inputname,'a') as f:
            for file in files:
                f.write(file+'\n')
        with open(inputname,'r') as f:
            lines=f.readlines()
            nums=len(lines)
        if nums>1000:
            with open(inputname,'w') as f:
                for line in lines[nums-1000:]:
                    f.write(line)
    except:
        input('meet error in upremovetxt')
def main(driver,num,type,phone,passwd):
    src_path="D:\\Workspace\\openai\\newarticles\\"+str(type)+"\\"
    dst_path="D:\\Workspace\\openai\\newarticles\\"+str(type)+"\\existed\\"
    time.sleep(1)
    url = "http://cuttlefish.baidu.com/shopmis?_wkts_=1671963555694#/taskCenter/majorTask"
    fulllogin(driver,phone,passwd)
    time.sleep(2)
    try:
        if type>=7:
            driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[2]/button[2]").click()
        else:
            driver.find_element(By.XPATH,"//*[@id='app']/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[2]/button[1]").click()
    except:
        pass
    try:
        time.sleep(1)
        tracks=driver.find_elements(By.XPATH,"//div[@class='privilege-item-container' or @class='privilege-item-container action']")
        tracks[type-1].click()
    except:
        input('请手动切换赛道')
    nownum=0
    turn=0
    removedlist=[]
    while 1:        
        turn+=1
        # if turn>=4:
        #     print('out of turn')
        #     break
        print('newturn')
        docx_files=[x for x in os.listdir('./newarticles/'+str(type)) if x.endswith('.docx')]
        preparelist=[]
        uponce=[]
        upmul=[]
        for file in docx_files:
            if len(preparelist)<int(min(20,num-nownum)):
                preparelist.append(file)
                if '.' in file:
                    uponce.append(file)
                else:
                    upmul.append(file)
            else:
                break
            print(file,'added')
        print("prepared")
        if len(upmul)<=1:
            print('文章数不够，开始逐个上传')
            break
        upload(driver,upmul,type)
        print('uploading')
        time.sleep(2)
        page=getpagetype(driver)
        print('in page:',page)
        if page=='repeat':
            repeatlist=repeat(driver)
            print(repeatlist)
            for file in repeatlist:
                file=file[1:-1]
                os.system('del \"'+src_path+file+'.docx\"')
                print(file,'removed')
                removedlist.append(file)
            if getpagetype(driver)=='repeat':
                confirm(driver)
            continue
        if page=='waiting_commit':
            # input('waiting')
            while 1:
                time.sleep(2)
                labels=driver.find_elements(By.XPATH,"//tbody/tr[@class='el-table__row']/td/div[@class='cell']/label/span")
                flag=1
                for label in labels:
                    if label.get_attribute('class')!='el-checkbox__input is-checked':
                        flag=0
                        break
                if flag==1:
                    # input('上传完成')
                    break
                
            sub_list=confirm_submit(driver)
            print('sub_list',sub_list)
            for file in sub_list:
                os.system('del \"'+src_path+file+'.docx\"')
                print(file,'removed')
                removedlist.append(file)
            time.sleep(1)
        if page=="upload_success":
            suc_num=success_num(driver)
            if suc_num==-1:
                input('meet err')
            nownum+=suc_num
            driver.get(url)
            print('上传成功',suc_num,'篇')
            
    upremovetxt(removedlist,type)
    input('fin')
