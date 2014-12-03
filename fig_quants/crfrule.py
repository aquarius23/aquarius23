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

	def feature_ma(self, exchange, index, ma):
		ret = []
		adj_1 = self.fix_index(-1)
		ma1_1 = ma[adj_1][0]
		ma3_1 = ma[adj_1][1]
		ma5_1 = ma[adj_1][2]
		ma1 = ma[index][0]
		ma3 = ma[index][1]
		ma5 = ma[index][2]
		end = exchange[index][2]
		sort = []
		for i, item in enumerate(ma[index]):
			x = []
			x.append(str(i))
			x.append(item)
			sort.append(x)
		x=[]
		x.append('e')
		x.append(end)
		sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='ma'
		for i in sort:
			x = x+i[0]
		ret.append(x)
		if ma1_1 < ma1:
			ret.append('ma1+')
		elif ma1_1 > ma1:
			ret.append('ma1-')
		else:
			ret.append('ma1=')

		if ma3_1 < ma3:
			ret.append('ma3+')
		elif ma3_1 > ma3:
			ret.append('ma3-')
		else:
			ret.append('ma3=')

		if ma5_1 < ma5:
			ret.append('ma5+')
		elif ma5_1 > ma5:
			ret.append('ma5-')
		else:
			ret.append('ma5=')
		return ret

	def feature_volume_ma(self, exchange, index, volume_ma):
		ret = []
		end = volume_ma[index][5]
		sort = []
		for i, item in enumerate(volume_ma[index]):
			x = []
			x.append(str(i))
			x.append(item)
			sort.append(x)
		x=[]
		x.append('e')
		x.append(end)
		sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='v_ma'
		for i in sort:
			x = x+i[0]
		ret.append(x)
		return ret

	def feature_kline(self, exchange, index, kline):
		ret = []
		k_r = (int)(kline[index][3]*10)
		k_el = (int)(kline[index][4]*10)
		ret.append('k_r='+str(k_r))
		ret.append('k_el'+str(k_el))
		ret.append('quekou=' + str(kline[index][5]))
		ret.append('baoxian=' + str(kline[index][6]))
		return ret

	def feature_exchange(self, index, exchange):
		return []
