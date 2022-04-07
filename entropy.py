# -*- coding: utf-8 -*-
import jieba
import re
import numpy as np
import os

def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    return chinese

def trans_sentence(text_file):
    file = "".join(open(text_file, 'r', encoding='GB18030').readlines())
    # 先去除广告
    file = file.replace("本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com","")
    replacements = ["\t", "\n", "\u3000", "\u0020", "\u00A0", " "]
    for repalcement in replacements:
        file = file.replace(repalcement, "")
    file = file.replace("，", "。")
    file = file.split("。")
    for i in range(len(file)):
        file[i] = find_chinese(file[i])
    return file

def cha_fre(file,n):
    """
    统计字频
    :param file:给定文章
    :param n: n元
    :return:
    """
    adict = {}
    if n == 1:
        for line in file:
            for i in line:
                if i in adict:adict[i] += 1
                else:adict[i] = 1
    elif n == 2:
        for line in file:
            for i in range(len(line)-1):
                if (line[i]+line[i+1]) in adict:adict[line[i]+line[i+1]] += 1
                else:adict[line[i]+line[i+1]] = 1
    else:
        for line in file:
            for i in range(len(line)-2):
                if (line[i]+line[i+1]+line[i+2]) in adict:adict[line[i]+line[i+1]+line[i+2]] += 1
                else:adict[line[i]+line[i+1]+line[i+2]] = 1
    return adict

def word_fre(file,n):
    """
    统计词频
    :param file:给定文章
    :param n: n元
    :return:
    """
    adict = {}
    if n == 1:
        for line in file:
            words = list(jieba.cut(line))
            for i in range(len(words)):
                if tuple(words[i:i+1]) in adict:adict[tuple(words[i:i+1])] += 1
                else:adict[tuple(words[i:i+1])] = 1
    elif n == 2:
        for line in file:
            words = list(jieba.cut(line))
            for i in range(len(words)-1):
                if tuple(words[i:i+2]) in adict:adict[tuple(words[i:i+2])] += 1
                else:adict[tuple(words[i:i+2])] = 1
    else:
        for line in file:
            words = list(jieba.cut(line))
            for i in range(len(words)-2):
                if tuple(words[i:i+3]) in adict:adict[tuple(words[i:i+3])] += 1
                else:adict[tuple(words[i:i+3])] = 1
    return adict

def cal_cha_entropy(file,n):
    if n == 1:
        frequency = cha_fre(file,1)
        sums = np.sum(list(frequency.values()))
        entropy = -np.sum([i*np.log2(i/sums) for i in  frequency.values()])/sums
    elif n == 2:
        frequency1 = cha_fre(file,1)
        frequency2 = cha_fre(file,2)
        sums = np.sum(list(frequency2.values()))
        entropy = -np.sum([v*np.log2(v/frequency1[k[:n-1]]) for k,v in  frequency2.items()])/sums
    else:
        frequency2 = cha_fre(file,2)
        frequency3 = cha_fre(file,3)
        sums = np.sum(list(frequency3.values()))
        entropy = -np.sum([v*np.log2(v/frequency2[k[:n-1]]) for k,v in  frequency3.items()])/sums
    return entropy

def cal_word_entropy(file,n):
    if n == 1:
        frequency = word_fre(file,1)
        sums = np.sum(list(frequency.values()))
        entropy = -np.sum([i*np.log2(i/sums) for i in  frequency.values()])/sums
    elif n == 2:
        frequency1 = word_fre(file,1)
        frequency2 = word_fre(file,2)
        sums = np.sum(list(frequency2.values()))
        entropy = -np.sum([v*np.log2(v/frequency1[k[:n-1]]) for k,v in  frequency2.items()])/sums
    else:
        frequency2 = word_fre(file,2)
        frequency3 = word_fre(file,3)
        sums = np.sum(list(frequency3.values()))
        entropy = -np.sum([v*np.log2(v/frequency2[k[:n-1]]) for k,v in  frequency3.items()])/sums
    return entropy

# text_file = 'G:\\bad_weather\\entropy\\data\\白马啸西风.txt'
# file = trans_sentence(text_file)
# print(word_fre(file,1))
# print(word_fre(file,2))
# print(word_fre(file,3))

path = 'G:\\bad_weather\\entropy\\new_data\\'
files = os.listdir(path)
for i in files:
    text_file = path + i
    file = trans_sentence(text_file)
    cha1 = cal_cha_entropy(file,1)
    cha2 = cal_cha_entropy(file,2)
    cha3 = cal_cha_entropy(file,3)
    word1 = cal_word_entropy(file,1)
    word2 = cal_word_entropy(file,2)
    word3 = cal_word_entropy(file,3)
    print("{},cha1:{},cha2:{},cha3:{},word1:{},word2:{},word3:{}".format(i,cha1,cha2,cha3,word1,word2,word3))
