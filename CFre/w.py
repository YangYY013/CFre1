
# -*- coding=utf-8 -*-
import math
import sys
import pandas
import numpy
from texttable import Texttable
from collections import defaultdict
# from Wtemp import *
from operator import itemgetter

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


def item_context(Wn,Wc):
    W=[]
    f = open("W.txt","w+")
    for i in Wn:
        for j in Wc:
            if (i[0])==(j[0])and(i[1]==j[1]):
                W=(i[0],j[1],(i[2]+j[2])*0.5)
                print >> f, W
    f.close()
    return W


if __name__ == '__main__':
    #读取两个相似度矩阵
    Wn=readWcn("D:/PycharmProjects/untitled2/W_n_n.txt")
    Wc=readWcn("D:/PycharmProjects/untitled2/W_c_c.txt")
    W = item_context(Wn, Wc)
    print ("W生成")

