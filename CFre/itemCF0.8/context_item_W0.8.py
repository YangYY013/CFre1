
# -*- coding=utf-8 -*-
import math
import sys
import pandas
import time
import numpy
from texttable import Texttable
from collections import defaultdict
# from Wtemp import *
from operator import itemgetter

# 读取文件
def readFile(fileData):
    data = []
    rates = []
    f = open(fileData, "r")
    data = f.readlines()
    f.close()
    for line in data:
        dataLine = line.split(",")
        rates.append([int(dataLine[0]),int(dataLine[1]), int(dataLine[2])])
    return rates
# 读取相似度矩阵
def readWcn(fileData):
    data = []
    rates = []
    f = open(fileData, "r")
    data = f.readlines()
    f.close()
    for line in data:
        dataLine = line.strip("\n").lstrip("(").rstrip(")").split(",")
        rates.append([int(dataLine[0]), int(dataLine[1]), float(dataLine[2])])
    return rates

#   输入：数据集合，格式：用户id\t 物品id\t 上下文tag\t
#   输出:上下文信息字典(上下文 - 项目倒排表）： dic[上下文id] = [电影id1，电影id2...]
#                (物品-上下文：dic[物品id]=[上下文id1，上下文id2...]
#                     (user-item： dic[userid]=[itemid1,itemid2...]
#创建上下文字典
def createDictContext(rates):
    context_item_dict = {}
    item_context_dict = {}
    for i in rates:
        if i[2] in context_item_dict:                     #上下文id\t（i[2]）物品id\t(i[1])
            context_item_dict[i[2]].append((i[1]))  #字典里存在上下文，则把扫描到的（物品id）放到当前上下文列表里
        else:
            context_item_dict[i[2]] = [(i[1])]      #字典里不存在上下文，则把扫描到的上下文创建一个列表
    for i in rates:
        if i[1] in item_context_dict:
            item_context_dict[i[1]].append((i[2]))  # item
        else:
            item_context_dict[i[1]] = [i[2]]
    #context_txt = pandas.Series(context_item_dict)
    #context_txt.to_csv('context_item.csv')
    #artistcontext_txt = pandas.Series(item_context_dict)
    #artistcontext_txt.to_csv('item_context.csv')
    return context_item_dict
# 创建item字典
def createDictItem(rates):
    user_item_dict = {}
    for i in rates:
        if i[0] in user_item_dict:              # userid\t（i[0]）物品id\t(i[1])
            user_item_dict[i[0]].append((i[1]))  # 字典里存在user，则把扫描到的（物品id）放到当前user列表里
        else:
            user_item_dict[i[0]] = [(i[1])]  # 字典里不存在user，则把扫描到的item创建一个列表
    #context_txt = pandas.Series(user_item_dict)
    #context_txt.to_csv('user_item.csv')
    return user_item_dict

#计算item-上下文相似度
def contextCF(context_dic,x):
    #f = open("W_c.txt", "w+")
    N = dict()
    C = defaultdict(defaultdict)
    Wc = defaultdict(defaultdict)
    for key in context_dic:
        for i in context_dic[key]:
            if i not in N.keys():  # i[0]表示物品id
                N[i] = 0
            N[i] += 1  # N[i[0]]表示某物品拥有的上下文数
            for j in context_dic[key]:
                if i == j:
                    continue
                if j not in C[i].keys():
                    C[i][j] = 0
                C[i][j] += 1  # C[i[0]][j[0]]表示根据上下文计算的物品两两之间的相似度，eg：物品同时拥有的上下文
                #print(C[i].keys())
                #data = (i, j, C[i][j])
               # print >> f, (data)
        #print(N[i])
    #f.close()
    f2 = open("W_c_c.txt", "w+")
    for i, related_item in C.items():
        for j, cij in related_item.items():
            Wc[i][j] = (cij / math.sqrt(N[i] * N[j]))*x
            data = i,j,Wc[i][j]
            print >>f2,data
    f2.close()
    return Wc
#计算item-用户相似度
def itemCF(item_dic,x):
   # f = open("W_n.txt", "w+")
    N = dict()
    C = defaultdict(defaultdict)
    Wn = defaultdict(defaultdict)
    for key in item_dic:
        for i in item_dic[key]:
            if i not in N.keys():  # i[0]表示物品id
                N[i] = 0
            N[i] += 1  # N[i[0]]表示某物品拥有的上下文数
            #print(i)
            for j in item_dic[key]:
                if i == j:
                    continue
                if j not in C[i].keys():
                    C[i][j] = 0
                C[i][j] += 1  # C[i[0]][j[0]]表示根据上下文计算的物品两两之间的相似度，eg：物品同时拥有的上下文
                #data = (i, j, C[i][j])
                #print >> f, (data)
    #f.close()
    f2 = open("W_n_n.txt", "w+")
    for i, related_item in C.items():
        for j, cij in related_item.items():
            Wn[i][j] = (cij / math.sqrt(N[i] * N[j]))*x
            data = i,j,Wn[i][j]
            print >>f2,data
    f2.close()
    return Wn

#物品-用户Wn，物品-上下文Wc 计算物品相似度矩阵 W=Wn+xWc
def item_context(Wn,Wc):
    W=[]
    f = open("W_0.8.txt","w+")
    for i in Wn:
        for j in Wc:
            if (i[0])==(j[0])and(i[1]==j[1]):
                W = (i[0], j[1], (i[2] + j[2]) * 0.5)
                print >> f, W
    f.close()
    return W

if __name__ == '__main__':
    t1=time.time()
    contextTemp = readFile("D:/PycharmProjects/untitled2/itemCF0.8/Context_9000train.csv")  # 读取用户-物品-上下文
    X=0.2
    Y=1-X
    context_dic = createDictContext(contextTemp)  # 创建上下文字典
    Wc = contextCF(context_dic,X)
    print("创建物品上下文相似矩阵")

    item_dic = createDictItem(contextTemp)  # 创建物品字典
    Wn = itemCF(item_dic,Y)
    print("创建物品用户相似矩阵")

    #计算 W 物品相似度矩阵
    Wn = readWcn("D:/PycharmProjects/untitled2/itemCF0.8/W_n_n.txt")
    Wc = readWcn("D:/PycharmProjects/untitled2/itemCF0.8/W_c_c.txt")
    Wcn = item_context(Wn, Wc)
    t2=time.time()
    print ("W",t2-t1)

