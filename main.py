from  getname.get_article_name import get_name
from get1 import gettxt
import datetime
import time
import pytz as pytz
apikey='' # your apikey
tz= pytz.timezone('Asia/Shanghai')
data=datetime.datetime.fromtimestamp(int(time.time()), tz).strftime('%Y-%m-%d')
print(data)
type=1
columns=get_name(data,type)
print(columns)
for i in range(0,len(columns)):
    time=0
    print('第'+str(i)+"篇",columns[i])
    try:
        gettxt(apikey,columns[i],type)
    except Exception as e:
        time+=1
        print('error',time,e)
        if time==2:
            break
print('done')