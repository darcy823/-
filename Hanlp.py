#-*- coding : utf-8-*-
from pyhanlp import *
import zipfile
import os
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH
IClassifier = JClass('com.hankcs.hanlp.classification.classifiers.IClassifier')
NaiveBayesClassifier = JClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')
TermFrequency = JClass('com.hankcs.hanlp.corpus.occurrence.TermFrequency')
TermFrequencyCounter = JClass('com.hankcs.hanlp.mining.word.TermFrequencyCounter')
TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")

data=[]
temp=''

DATA_FILES_PATH = "D:/MyProjects/数据科学大作业"

def test_data_path():
    data_path = os.path.join(HANLP_DATA_PATH, DATA_FILES_PATH)
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    return data_path

def ensure_data(data_name, data_url):
    root_path = test_data_path()
    dest_path = os.path.join(root_path, data_name)
    if os.path.exists(dest_path):
        return dest_path
    if data_url.endswith('.zip'):
        dest_path += '.zip'
    download(data_url, dest_path)
    if data_url.endswith('.zip'):
        with zipfile.ZipFile(dest_path, "r") as archive:
            archive.extractall(root_path)
        remove_file(dest_path)
        dest_path = dest_path[:-len('.zip')]
    return dest_path

def predict(classifier, text):
    print("%s 情感极性是 %s" % (text, classifier.classify(text)))


if __name__ == '__main__':
    ChnSentiCorp_path = ensure_data('ChnSentiCorp情感分析酒店评论', "http://file.hankcs.com/corpus/ChnSentiCorp.zip")
    classifier = NaiveBayesClassifier()
    classifier.train(ChnSentiCorp_path)
    counter = TermFrequencyCounter()
    for line in open("test.txt","r",encoding = 'utf-8'):
        if line != '\n':
            temp=temp+line
        else:
            data.append(temp)
            temp=''
    data.append(temp)
    str=''.join(data)
    length = len(data)
    for i in range(0,length):
        content=''.join(data[i])
        counter.add(content)
        print(counter.top(5))
        print(TermFrequencyCounter.getKeywordList(content,5))
        print(HanLP.extractKeyword(content, 5))
        predict(classifier, content)




