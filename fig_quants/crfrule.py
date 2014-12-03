#!/usr/bin/python
#!coding=utf-8
import crfrulebase

class crfrule(crfrulebase.crfrulebase):

	def get_state(self, index, exchange, kline):
		next = self.fix_index(1)
		today = kline[index][0]
		if today >= 1:
			today = 1
		elif today <= -1:
			today = -1
		else:
			today = 0

		tomorrow = kline[next][0]
		if tomorrow >= 1:
			tomorrow = 1
		elif tomorrow <= -1:
			tomorrow = -1
		else:
			tomorrow = 0

		return str(tomorrow)

	def feature_kdj(self, exchange, index, kdj):
		adj_1 = self.fix_index(-1)
		ret = []
		j =  kdj[index][2]
		k = kdj[index][0]
		d = kdj[index][1]
		j_1 = kdj[adj_1][2]
		if j < 20:
			ret.append('j=-1')
		elif j >80:
			ret.append('j=1')
		else:
			ret.append('j=0')

		if j > j_1:
			ret.append('j+')
		elif j < j_1:
			ret.append('j-')
		else:
			ret.append('j=')

		if k < d:
			ret.append('k<d')
		elif k > d:
			ret.append('k>d')
		else:
			ret.append('k=d')
		return ret

	def feature_macd(self, exchange, index, macd):
		ret = []
		adj_1 = self.fix_index(-1)
		macd_1 = macd[adj_1][2]
		dif = macd[index][0]
		dea = macd[index][1]
		macd = macd[index][2]
		if macd > 0:
			ret.append('macd=1')
		elif macd < 0:
			ret.append('macd=-1')
		else:
			ret.append('macd=0')

		if dif < dea:
			ret.append('dif<dea')
		elif dif > dea:
			ret.append('dif>dea')
		else:
			ret.append('dif=dea')

		if macd < macd_1:
			ret.append('macd-')
		elif macd > macd_1:
			ret.append('macd+')
		else:
			ret.append('macd=')
		return ret

	def feature_boll(self, exchange, index, boll):
		ret = []
		end = exchange[index][2]
		MB = boll[index][0]
		UP = boll[index][1]
		DN = boll[index][2]
		if MB < end:
			ret.append('MB<end')
		elif MB > end:
			ret.append('MB>end')
		else:
			ret.append('MB=end')

		if UP < end:
			ret.append('UP<end')
		elif UP > end:
			ret.append('UP>end')
		else:
			ret.append('UP=end')

		if DN < end:
			ret.append('DN<end')
		elif DN > end:
			ret.append('DN>end')
		else:
			ret.append('DN=end')
		return ret

