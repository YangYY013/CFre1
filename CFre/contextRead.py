
# -*- coding=utf-8 -*-
import math
import sys
import pandas
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
    context_txt = pandas.Series(context_item_dict)
    context_txt.to_csv('context_item.csv')
    artistcontext_txt = pandas.Series(item_context_dict)
    artistcontext_txt.to_csv('item_context.csv')
    return context_item_dict
# 创建item字典
def createDictItem(rates):
    user_item_dict = {}
    for i in rates:
        if i[0] in user_item_dict:              # userid\t（i[0]）物品id\t(i[1])
            user_item_dict[i[0]].append((i[1]))  # 字典里存在user，则把扫描到的（物品id）放到当前user列表里
        else:
            user_item_dict[i[0]] = [(i[1])]  # 字典里不存在user，则把扫描到的item创建一个列表

    context_txt = pandas.Series(user_item_dict)
    context_txt.to_csv('user_item.csv')

    return user_item_dict
#创建矩阵字典
# id1 id2 相似度
def CreatWcn_dict(rates):
    Wcn_dict = {}
    for i in rates:
        if i[0] in Wcn_dict:  # userid\t（i[0]）物品id\t(i[1])
            Wcn_dict[i[0]].append((i[1],i[2]))  # 字典里存在id，则把扫描到的id-相似度放到当前id的value里
        else:
            Wcn_dict[i[0]] = [(i[1],i[2])]  # 字典里不存在id1，则把扫描到的ID-相似度创建一个key：value
    return Wcn_dict

#计算物品-上下文相似度
def contextCF(context_dic,x):
    f = open("W_c.txt", "w+")
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
                data = (i, j, C[i][j])
                print >> f, (data)
        #print(N[i])
    f.close()
    f2 = open("W_c_c.txt", "w+")
    for i, related_item in C.items():
        for j, cij in related_item.items():
            Wc[i][j] = (cij / math.sqrt(N[i] * N[j]))*x
            data = i,j,Wc[i][j]
            print >>f2,data
    f2.close()
    return Wc
#计算物品-用户相似度
def itemCF(item_dic,x):
    f = open("W_n.txt", "w+")
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
                data = (i, j, C[i][j])
                print >> f, (data)
    f.close()
    f2 = open("W_n_n.txt", "w+")
    for i, related_item in C.items():
        for j, cij in related_item.items():
            Wn[i][j] = (cij / math.sqrt(N[i] * N[j]))*(1-x)
            data = i,j,Wn[i][j]
            print >>f2,data
    f2.close()
    return Wn

#物品-用户Wn，物品-上下文Wc 计算物品相似度矩阵 W=Wn+xWc
def item_context(Wn,Wc):
    W=[]
    f = open("W.txt","w+")
    for i in Wn:
        for j in Wc:
            if (i[0])==(j[0])and(i[1]==j[1]):
                W = (i[0], j[1], (i[2] + j[2]) * 0.5)
                print >> f, W
    f.close()
    return W

# 获取上下文列表
def getContextList(item):
    items = {}
    f = open(item, "r")
    context_content = f.readlines()
    f.close()
    for context in  context_content:
        contextLine = context.split("\t")
        items[int(contextLine[0])] = contextLine[1:]
    #context_txt = pandas.Series(items)
    #context_txt.to_csv('context_txt.csv')
    return items

# 结合用户喜好对物品排序
#获取用户——物品
def readUser_item(fileData):
    data = []
    rates = []
    f = open(fileData, "r")
    data = f.readlines()
    f.close()
    for line in data:
        dataLine = line.split(",")
        rates.append([int(dataLine[0]),int(dataLine[1]), int(dataLine[2])])
    return rates

# 这里产生了用户——项目 训练集的 的用户字典和项目字典
def createUser_Dict(rates):
    user_dict = {}
    for i in rates:
        if i[0] in user_dict:  # 用户id\t（i[0]）物品id\t(i[1]) 用户评分(i[2])
            user_dict[i[0]].append((i[1], i[2]))  # 字典里存在用户，则把扫描到的（物品id，权重）放到当前用户的value里
        else:
            user_dict[i[0]] = [(i[1], i[2])]  # 字典里不存在用户，则把扫描到的用户创建一个key:value
                #字典里不存在用户，则把扫描到的用户创建一个列表
    return user_dict

def recommondation(user_id,user_dict,W,K):
    rank = defaultdict(int)
    l = list()
    for i, score in user_dict[user_id]:  # i为特定用户的电影id，score为其相应评分
        for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:K]:  # sorted()的返回值为list,list的元素为元组
            if j in user_dict[user_id]:
                continue
            rank[j] += score * wj  # 先找出用户产生过行为的物品，对每一部电影id，假设其中一部电影id1,找出与该电影最相似的K部电影，计算出在id1下用户对每部电影的兴趣度，接着迭代整个用户评论过的电影集合，求加权和，再排序，可推荐出前n部电影，我这里取10部。
    l = sorted(rank.items(), key=itemgetter(1), reverse=True)[0:10]
    return l


if __name__ == '__main__':
    contextTemp = readFile("D:/PycharmProjects/untitled2/Context_train.csv")  # 读取用户-物品-上下文

    context_dic = createDictContext(contextTemp)  # 创建上下文字典
    Wc = contextCF(context_dic,0.5)
    print("创建物品上下文相似矩阵")

    item_dic = createDictItem(contextTemp)  # 创建物品字典
    Wn = itemCF(item_dic,0.5)
    print("创建物品用户相似矩阵")

    #计算 W 物品相似度矩阵
    Wn = readWcn("D:/PycharmProjects/untitled2/W_n_n.txt")
    Wc = readWcn("D:/PycharmProjects/untitled2/W_c_c.txt")
    Wcn = item_context(Wn, Wc)
    print ("W生成")

    #可以不用每次都跑 W.txt了，直接从这里跑
    #进行推荐
    # 这里是物品相似度矩阵这里是元组格式，需要转换成字典格式
    # 创建矩阵字典
    #W_dict = readWcn("W.txt")
    #W=CreatWcn_dict(W_dict)
    #print("W-dict生成")
    ###  这里的 W里的物品id和user里的物品id 部分重合，需要做==判断
    ###  这里的 user 的资料需要分开做 训练资料 和 测试资料
    #用户——物品的字典
   # user_id=96
    #user_dict=createUser_Dict(readUser_item("D:/PycharmProjects/untitled2/user_artists_train.csv"))
    #idtemp = recommondation(user_id, user_dict,W,30)  #这里的80 是对item相似度求前80
    #print (idtemp)
