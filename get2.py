title='./初中七年级上册政治教案3篇.txt'
try:
    file= open(title, 'r',encoding='UTF-8')      # 打开文件
    data = file.read()                   # 读取文件内容
finally:
    if file:
        file.close()                     # 确保文件被关闭
with open(title,'w',encoding='utf-8') as write_file:
    write_file.write(data.replace('\n','\n\n'))