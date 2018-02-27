# -*- coding=utf-8 -*-
import math
import sys
import pandas
import numpy
from texttable import Texttable
from collections import defaultdict
# from Wtemp import *
from operator import itemgetter

# 读取W相似度矩阵
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
#创建矩阵字典
# id1 id2 相似度
def CreatWcn_dict(rates):
    Wcn_dict = {}
    Wcn=defaultdict(defaultdict)
    for i in rates:
        if i[0] in Wcn_dict:  # userid\t（i[0]）物品id\t(i[1])
            Wcn_dict[i[0]].append((i[1],i[2]))  # 字典里存在id，则把扫描到的id-相似度放到当前id的value里
        else:
            Wcn_dict[i[0]] = [(i[1],i[2])]  # 字典里不存在id1，则把扫描到的ID-相似度创建一个key：value
    for key in Wcn_dict:
        for i in Wcn_dict[key]:
            Wcn[key][i[0]] =i[1]  #id1 id2 similar
    return Wcn
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
    f = open("res.txt", "w")
    rank = defaultdict(int)
    l = list()
    for i, score in user_dict[user_id]:          #  遍历用户字典的value  i为特定用户的itemid，score为其相应评分
        for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:K]:  # sorted()的返回值为list,list的元素为元组
            if j in user_dict[user_id]:
                continue
            rank[j] += score * wj  # 先找出用户产生过行为的物品，对每一部电影id，假设其中一部电影id1,找出与该电影最相似的K部电影，计算出在id1下用户对每部电影的兴趣度，接着迭代整个用户评论过的电影集合，求加权和，再排序，可推荐出前n部电影，我这里取10部。
    l = sorted(rank.items(), key=itemgetter(1), reverse=True)
    l2 = list(set(l))     #去除重复的项目
    for i in l2:
        data= i[0]
        print >> f, data
    f.close()
    return l2


if __name__ == '__main__':

    # 可以不用每次都跑 W.txt了，直接从这里跑
    # 进行推荐
    # 这里是物品相似度矩阵这里是元组格式，需要转换成字典格式
    # 创建矩阵字典

    W_dict = readWcn("D:/PycharmProjects/untitled2/itemCFH/W_0.5.txt")
    W = CreatWcn_dict(W_dict)
    print("W-dict生成")

    ###  这里的 W里的物品id和user里的物品id 部分重合，需要做==判断
    ###  这里的 user 的资料需要分开做 训练资料 和 测试资料
    # 用户——物品的字典

    user_id = 442
    user_dict = createUser_Dict(readUser_item("D:/PycharmProjects/untitled2/itemCFH/user_artists1.csv"))
    data = recommondation(user_id, user_dict, W, 70)  # 这里的80 是对item相似度求前80
    print data
