# -*- coding: utf-8 -*-

import jieba
import math

data=[]
temp=''

s = open("stopwords.txt", encoding='utf-8', errors="ignore")  # 拉取停词表
chinese_stop = {}
for word in s:
    word = word.strip()
    chinese_stop[word] = 1
s.close()



for line in open("test.txt", "r", encoding='utf-8'):
    if line != '\n':
        temp = temp + line
    else:
        data.append(temp)
        temp = ''
data.append(temp)
str = ''.join(data)
length = len(data)
for i in range(0, length):
    counts = {}  # 通过键值对的形式存储词语及其出现的次数
    tfs = {}  # 通过键值对的形式存储词语及其TF值
    lines = {}  # 通过键值对的形式存储词语及其出现的行数
    idfs = {}  # 通过键值对的形式存储词语及其IDF值
    tf_idfs = {}  # 通过键值对的形式存储词语及其TF-IDF值
    content = ''.join(data[i])
    words = jieba.lcut_for_search(content)
    wordcounts = 0
    for word in words:
        if word not in chinese_stop.keys():  # 不考虑停词表中的词
            counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加1
            wordcounts += 1  # 总词数也加1
    print(wordcounts)
    items = list(counts.items())
    for i in range(len(counts)):  # 计算每个词语的TF值
        word, count = items[i]
        tfs[word] = count / wordcounts
    lineCount = 0  # 总行数
    for line in content:
        lineCount += 1  # 总行数加1
        for i in range(len(counts)):
            word, count = items[i]
            if word in line:
                lines[word] = lines.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的行数加1
    print(lineCount)
    for i in range(len(counts)):
        word3, line = items[i]
        idfs[word3] = math.log10(lineCount / line)  # 计算每个词语的IDF值
    items2 = list(tfs.items())
    items3 = list(idfs.items())
    for i in range(len(counts)):
        word2, tf = items2[i]
        word3, idf = items3[i]
        tf_idfs[word2] = tf * idf  # 计算每个词语的TF-IDF值
    items4 = list(tf_idfs.items())
    items4.sort(key=lambda x: x[1], reverse=True)  # 根据词语的TF-IDF值进行从大到小排序
    for i in range(0,20):
        word4, tf_idf = items4[i]
        print("{0:^5} {1:^5}".format(word4, tf_idf))