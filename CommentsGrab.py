'''
1.获取每个时间段的微博id
2.获取每个微博热评第一页（热评前10条）
ps。获取当前时间段的微博总数/热评总数
3.写入数据

一个时期一个文件
'''


import os
from datetime import datetime, timedelta

import requests
from lxml import etree
from math import ceil
import re
from time import sleep
from random import randint

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': 'SUB=_2A25NCFRcDeRhGeFP4lMW9yvEyTiIHXVu83wUrDV6PUJbkdANLRemkW1NQOqtdpu0jfDZkN9I84XXWmdE3hF_pZxR; _T_WM=65064296191; MLOGIN=1'
}
requests.packages.urllib3.disable_warnings()
result_headers = [
            '评论者主页',
            '评论内容',
            '评论获赞数',
            '评论发布时间',
        ]
if not os.path.exists('comment2'):
    os.mkdir('comment2')

# global pageNum

def get_one_comment_struct(comment):
        # xpath 中下标从 1 开始
        userURL = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])

        content = comment.xpath(".//span[@class='ctt']/text()")
        # '回复' 或者只 @ 人
        if '回复' in content or len(content) == 0:
            test = comment.xpath(".//span[@class='ctt']")
            content = test[0].xpath('string(.)').strip()

            # 以表情包开头造成的 content == 0,文字没有被子标签包裹
            if len(content) == 0:
                content = comment.xpath('string(.)').strip()
                content = content[content.index(':') + 1:]
        else:
            content = content[0]                                                #内容

        praisedNum = comment.xpath(".//span[@class='cc'][1]/a/text()")[0]
        praisedNum = praisedNum[2:praisedNum.rindex(']')]                       #点赞数

        publish_time = comment.xpath(".//span[@class='ct']/text()")[0]

        publish_time = parse_time(publish_time)                            #发布时间

        return [userURL, content, praisedNum, publish_time]

def parse_time(publish_time):
        publish_time = publish_time.split('来自')[0]
        if '刚刚' in publish_time:
            publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        elif '分钟' in publish_time:
            minute = publish_time[:publish_time.find('分钟')]
            minute = timedelta(minutes=int(minute))
            publish_time = (datetime.now() -
                            minute).strftime('%Y-%m-%d %H:%M')
        elif '今天' in publish_time:
            today = datetime.now().strftime('%Y-%m-%d')
            time = publish_time[3:]
            publish_time = today + ' ' + time
        elif '月' in publish_time:
            year = datetime.now().strftime('%Y')
            month = publish_time[0:2]
            day = publish_time[3:5]
            time = publish_time[7:12]
            publish_time = year + '-' + month + '-' + day + ' ' + time
        else:
            publish_time = publish_time[:16]
        return publish_time

def WeiboCommentScrapy(wid):
        url = 'https://weibo.cn/comment/hot/{}?rl=2'.format(wid)                       #修改为热评页面
        res = requests.get(url,headers=headers)
        # commentNum = re.findall("评论\[.*?\]",res.text)[0]
        # commentNum = int(commentNum[3:len(commentNum)-1])
        # print(commentNum)
        # pageNum = ceil(commentNum/10)
        pageNum = re.findall('跳页.*页',res.text)
        if pageNum==[] :
            return
        pageNum = int(pageNum[0].split('/')[2][:-1])                                #页数
        print(pageNum)
        # for page in min(10,range(pageNum)):
        for page in range(5):
            result = []

            url = 'https://weibo.cn/comment/hot/{}?rl=2&page={}'.format(wid,page+1)
            res = requests.get(url, headers=headers)

            html = etree.HTML(res.text.encode('utf-8'))

            comments = html.xpath("/html/body/div[starts-with(@id,'C')]")

            print('第{}/{}页'.format(page+1,pageNum))

            for i in range(len(comments)):
                result.append(get_one_comment_struct(comments[i]))

            # sleep(randint(10,20))
        return result

            # if page==0:
            #     write(result,isHeader=True,pageNum = pageNum)
            # else:
            #     write(result,isHeader=False)


def write(result,starttime):
    with open('comment2/' + starttime + '.txt', 'a', encoding='utf-8-sig', newline='') as f:
        for i in result_headers:
            f.write(i+' ')
        # string = " 评论共"+ str(pageNum)+"页\n"
        f.write('\n')
        for items in result:
            for item in items:
                f.write(item+' ')
            f.write('\n')
        # f.write(result)
        f.write('\n')
    print('已成功将{}条评论写入{}中'.format(len(result), 'comment2/' + starttime + '.txt'))

def getWeiBoID(startTime,endTime):
    # wid ='JEDspCWbU'
    # WeiboCommentScrapy(wid)
    url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E7%96%AB%E6%83%85&advancedfilter=1&starttime=20191201' \
          '&endtime=20200122&sort=hot&page={}'
    params = {'advancedfilter': '1',
              'keyword': '疫情',
              'nick':'',
              'starttime': startTime,
              'endtime': endTime,
              'sort': 'hot',
              'smblog': '搜索'}

    # pageNum = re.findall('\跳\页.*?\页', res.text)                               #后来页数也找不到了
    # pageNum = int(pageNum[0].split('/')[2][:-1])                                # 页数
    # # itemNum = re.findall('<span class="cmt">共9720268条</span>',res.text)      #条数为什么找不到啊啊啊
    # # itemNum = itemNum[1:-1]
    # print(pageNum)

    weiBoID = []

    for i in range(5):
        res = requests.get(url.format(i+1),headers=headers,params=params,vertify=False)
        data = re.findall('comment\/.*?\?rl\=1\#cmtfrm\" class=\"cc\"\>原文评论', res.text)
        for item in data:
            str = re.findall('\/.*?\?',item)
            weiBoID.append(str[0][1:-1])
        # sleep(randint(10,20))

    return weiBoID


def run(strtimelist,endtimelist):
    for t in range(4):
        dataList = getWeiBoID(startTime=strtimelist[t], endTime=endtimelist[t])
        # 数据处理，写入text，每个时间段一个text
        data = []
        for item in dataList:
            tempdata = WeiboCommentScrapy(item)
            if(tempdata!=None):
                for i in tempdata:
                    for j in i:
                        data.append(j)
                    data.append('\n')
            # sleep(randint(10,20))
        write(data, starttime=strtimelist[t])
        # sleep(5)



if __name__ =="__main__":
    strtimelist = ['20191201','20200123','20200208','20200310']
    endtimelist = ['20190122','20200207','20200309','20200630']
    run(strtimelist,endtimelist)
