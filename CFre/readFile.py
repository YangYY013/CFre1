# -*- coding=utf-8 -*-
import sys
defaultencoding = 'utf-8'

import math
import sys
from texttable import Texttable
from collections import defaultdict
# from Wtemp import *
from operator import itemgetter


arr = [1,2,3,4,5,6,7,8,9]
matrix_a = np.array(arr)
print(matrix_a)


def createDict(rates):
    # type: (object) -> object
    user_dict = {}
    movie_dict = {}
    for i in rates:
        if i[0] in user_dict:
            user_dict[i[0]].append((i[1], i[2]))
        else:
            user_dict[i[0]] = [(i[1], i[2])]
        if i[1] in movie_dict:
            movie_dict[i[1]].append(i[0])
        else:
            movie_dict[i[1]] = [i[0]]
    return user_dict, movie_dict

def itemCF(user_dict):
    N = dict()
    C = defaultdict(defaultdict)
    W = defaultdict(defaultdict)
    for key in user_dict:
        for i in user_dict[key]:
            if i[0] not in N.keys():
                N[i[0]] = 0
            N[i[0]] += 1
            for j in user_dict[key]:
                if i == j:
                    continue
                if j not in C[i[0]].keys():
                    C[i[0]][j[0]] = 0
                C[i[0]][j[0]] += 1
    for i, related_item in C.items():
        for j, cij in related_item.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W

def main():
    data = []
    rates = []
    f1 = open("D:/PycharmProjects/reMov/user_artists.data", "r",)
    f = open("D:/PycharmProjects/reMov/artists.item", "r",)
    items = {}
    movie_content = f.readlines()
    for movie in movie_content:
        movieLine = movie.split("\t")
        items[int(movieLine[0])] = movieLine[1:]
    f.close()
    print(movieLine)
    user_dict, movie_dict = createDict(f1)

    N = dict()
    C = defaultdict(defaultdict)
    W = defaultdict(defaultdict)
    for key in user_dict:
        for i in user_dict[key]:
            if i[0] not in N.keys():  # i[0]表示movie_id
                N[i[0]] = 0
            N[i[0]] += 1  # N[i[0]]表示评论过某电影的用户数
            for j in user_dict[key]:
                if i == j:
                    continue
                if j not in C[i[0]].keys():
                    C[i[0]][j[0]] = 0
                C[i[0]][j[0]] += 1  # C[i[0]][j[0]]表示电影两两之间的相似度，eg：同时评论过电影1和电影2的用户数
    for i, related_item in C.items():
        for j, cij in related_item.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    print (W)
main()

