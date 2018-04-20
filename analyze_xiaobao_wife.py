#coding:utf-8
"""
=======================================
        Character relationships
=======================================

---------------------------------------
This is a programm for analyze the txt.
you will get who is Xiaobao's true love
---------------------------------------
"""

import sys, os
import jieba
import numpy as np
import networkx as nx
from pandas import DataFrame
from collections import defaultdict
import matplotlib.pyplot as plt


__time__ = "2018-4-15"
__author__ = "Wei"
__email__ = "hanwei@shanghaitech.edu.cn"

#input a file, cut file to paragraphs and you will get a list#
def read_txt(obj):
	op_txt = open(obj, "r", encoding="utf-8")
	txt = op_txt.read()
	txt_list = txt.split("\n\n")
	while "" in txt_list:
		txt_list.remove("")
	op_txt.close()
	return txt_list

#get a DataFrame, every column is a list; and every element is 0(not exist) or 1(exit)
def count_words(txt_list, actor, roles):
	count = 0
	start = defaultdict(int)
	res = {name:[] for name in actor}
	for paragraph in txt_list:
		count += 1
		words = list(jieba.cut(paragraph))
		for i in range(len(roles)):
			role = roles[i].split('/')
			flag = 'no'
			while role:
				if role[0] in words:
					flag = 'yes'; break
				del role[0]
			if flag == 'yes':
				res[actor[i]].append(1)
			else:
				res[actor[i]].append(0)
			if sum(res[actor[i]])==1:
				start[actor[i]] = count
	return res, start

#analyze the DataFrame format	
def analyze(result, start, leng):
	df = DataFrame(np.zeros(64).reshape(8, 8), columns=actor, index=actor)
	for key1, value1 in result.items():
		for key2, value2 in result.items():
			count = sum(map(lambda x, y:x+y==2, value1, value2))
			exist = leng - max((start[key1], start[key2]))
			count = count/exist
			df.loc[key1][key2] = count
	df = round(100*df/max(df.max()), 3)
	return df	

#Dtaw a network
def Draw_fig(df):
	graph_list = []
	for i in range(len(df)):
		x = df.columns[i]
		for j in range(i, len(df)):
			y = df.columns[j]
			z = df.iloc[i][j]
			graph_list.append((x, y, z))
	G.add_weighted_edges_from(graph_list)
	pos = nx.spring_layout(G)
	labels = dict(zip(df.index, df.index))
	nx.draw_networkx_edges(G, pos,
			edgelist=None,
			width=1.5,
			edge_color='k',
			style='solid',
			alpha=1.0,
			edge_cmap=None,
			edge_vmin=None,
			edge_vmax=None,
			ax=None,
			arrows=True,
			lable=None)
	nx.draw_networkx_nodes(G, pos,
			nodelist=list(df.index).remove('Xiaobao'),
			node_size=300,
			node_color='b',
			node_shape='o',
			alpha=1.0,
			cmap=None,
			vmin=None,
			vmax=None,
			ax=None,
			linewidths=None,
			label=None)
	nx.draw_networkx_nodes(G, pos,
			nodelist=['Xiaobao'],
			node_size=300,
			node_color='r')
	nx.draw_networkx_labels(G, pos, labels)
	plt.savefig("p.png")


if __name__ == "__main__":
	actor = ('Xiaobao', 'Zengrou', 'Ake', 'Suquan', 'Jianning',\
			'Shuanger', 'Junzhu', 'Fangyi')
#	actor = (u'小宝', u'曾柔', u'阿珂', u'苏荃', u'建宁', u'双儿', u'郡主', u'方怡')
	roles = (u'韦小宝/小宝/桂贝勒', u'曾柔/曾姑娘', u'阿珂/伍子珂',\
			 u'苏荃/洪夫人', u'建宁公主/建宁/爱新觉罗·宁香', \
			 u'双儿/赵双儿', u'沐剑屏/郡主', u'方怡/方姑娘/方姑娘道')
	G = nx.Graph()
	arg = sys.argv[1]
	txt_list = read_txt(arg)
	leng = len(txt_list)
	result, start = count_words(txt_list, actor, roles)
	df_res = analyze(result, start, leng)
	print(df_res)
#	G = nx.from_pandas_adjacency(df_res)
	Draw_fig(df_res)
	df_res.to_csv('out_data_aver2.csv', header=True)

