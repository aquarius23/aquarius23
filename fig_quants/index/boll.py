#!/usr/bin/python
#!coding=utf-8
import sys
import string

#[MB,UP,DN]
class boll():

	def cal_ma_md(self, list):
		count = 0
		MA = 0.0
		MD = 0.0
		for value in list:
			MA = MA + value
			count = count + 1
		MA = MA/count
		for value in list:
			MD = MD + (value - MA)**2
		MD = (MD/count)**0.5
		return MA,MD

	def cal_boll(self, list):
		twenty = []
		ret = []
		for day in list:
			result = []
			end = day[2]
			if len(twenty) < 20:
				twenty.append(end)
			else:
				twenty.remove(twenty[0])
				twenty.append(end)
			MB,MD = self.cal_ma_md(twenty)
			UP = MB + 2*MD
			DN = MB - 2*MD
			result.append(MB)
			result.append(UP)
			result.append(DN)
			ret.append(result)
		return ret
