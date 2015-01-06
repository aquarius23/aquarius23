#!/usr/bin/python
#!coding=utf-8

class stockflow():
	def cal_flow(self, list):
		list.sort(cmp = lambda x,y: cmp(x[0],y[0]), reverse = True)
		size = len(list)
		sum = 0
		flow = 0
		flow_big = 0
		for i, item in enumerate(list):
			dir = item[1]
			money = item[0]
			sum = sum + money
			if dir == 1:
				flow = flow + money
			elif dir == -1:
				flow = flow - money
			if i == (size / 5): #20%
				flow_big = flow
		return sum, flow, flow_big

