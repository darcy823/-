import requests
from bs4 import BeautifulSoup

n=0#计总数
for year in range(2019,2021):
    for month in range(1,13):
        day=29
        if year==2019 and month!=12:
            continue
        if year==2020 and month>6:
            break
        if year==2020 and month<=6:
            if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
                day=31
            if month==4 or month==6 or month==9 or month==11:
                day=30
            if month==2:
                day=29      #只考虑2020年
        for i in range(1,day+1):
            tempDay=str(i)
            tempMonth=str(month)
            tempYear=str(year)
            if i<10:
                tempDay=str(0)+tempDay
            if month<10:
                tempMonth=str(0)+tempMonth
            url='http://news.sina.com.cn/head/news'+tempYear+tempMonth+tempDay+'am.shtml'


            html = requests.get(url)
            soup=BeautifulSoup(html.content,"html.parser")


            data=soup.find_all('h1')
            for k in range(len(data)):
                try:
                    if data[k].a.string.find('疫情')!=-1 or data[k].a.string.find('新冠')!=-1 or data[k].a.string.find('确诊')!=-1 or data[k].a.string.find('隔离')!=-1 or data[k].a.string.find('武汉')!=-1:
                        n=n+1
                        with open(r'E:\Desktop\spider\urls.txt','a') as ff:
                            ff.write(data[k].a['href']+'\n')
                        print(data[k].a['href'])
                except :
                    continue
            data = soup.find_all('li')
            for k in range(len(data)):
                try:
                    if data[k].a.string.find('疫') != -1 or data[k].a.string.find('新冠') != -1 or data[k].a.string.find(
                            '确诊') != -1 or data[k].a.string.find('隔离') != -1 or data[k].a.string.find('武汉') != -1:
                        n = n + 1
                        # with open(r'E:\Desktop\spider\urls.txt', 'a') as ff:
                        #     ff.write(data[k].a['href'] + '\n')
                        print(data[k].a['href'])
                except:
                    continue

print(n)

