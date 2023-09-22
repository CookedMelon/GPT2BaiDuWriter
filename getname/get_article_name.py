import csv
import datetime

# Read the Excel file
def get_name(data,type):
    notuse='\\/:*?"<>|'
    time1=data
    filepath='./getname/table/'+time1+'/'+time1+'_'+str(type)+'.csv'
    # print(filepath)
    columns=[]
    with open(filepath, 'r',encoding='gbk') as f:
        reader = csv.reader(f)
        # Get the second row of the table
        row = next(reader)
        for row in reader:
        # Get the second column of the row
            try:
                column = row[1]
                flag=0
                for i in notuse:
                    if i in column:
                        flag=1
            # print(column)
                if flag==0:
                   columns.append(column)
            except:
                pass
    return columns