#!/usr/bin/python
#!coding=utf-8
import crfrulebase
ma_feature_size = 6
class crfrule(crfrulebase.crfrulebase):
	def __get_state(self, index, exchange, kline):
		today = kline[index][0]
		if today >= 1:
			if today >= 3:
				today = 3
			else:
				today = 1
		elif today <= -1:
			if today <= -3:
				today = -3
			else:
				today = -1
		else:
			today = 0

		return str(today)

	def get_state(self, index, exchange, kline):
		next = self.fix_index(1)
		tomorrow = self.__get_state(next, exchange, kline)
		return str(tomorrow)

	def feature_kdj(self, exchange, index, kdj):
		adj_1 = self.fix_index(-1)
		ret = []
		sort = []
		for i in range(-5,1):
			adj = self.fix_index(i)
			item = kdj[adj][2]
			x = []
			x.append(str(abs(i)))
			x.append(item)
			sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='j_sort='
		for i in sort:
			x = x+i[0]
		ret.append(x)

		j =  kdj[index][2]
		k = kdj[index][0]
		d = kdj[index][1]
		j_1 = kdj[adj_1][2]
		j_1_level = (int)(j_1/10)
		j_level = (int)(j/10)
		ret.append('j_1='+str(j_1_level))
		ret.append('j1='+str(j_level))

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
		sort = []
		for i in range(-5,1):
			adj = self.fix_index(i)
			item = macd[adj][2]
			x = []
			x.append(str(abs(i)))
			x.append(item)
			sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='macd_sort='
		for i in sort:
			x = x+i[0]
		ret.append(x)

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
			if i >= ma_feature_size:
				break
			x = []
			x.append(str(i))
			x.append(item)
			sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='ma'
		for i in sort:
			x = x+i[0]
		ret.append(x)

		sort = []
		for i, item in enumerate(ma[adj_1]):
			if i >= ma_feature_size:
				break
			x = []
			x.append(str(i))
			x.append(item)
			sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='ma_1'
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
		sort = []
		for i, item in enumerate(volume_ma[index]):
			if i > ma_feature_size:
				break;
			x = []
			x.append(str(i))
			x.append(item)
			sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='v_ma'
		for i in sort:
			x = x+i[0]
		ret.append(x)

		adj_1 = self.fix_index(-1)
		sort = []
		for i, item in enumerate(volume_ma[adj_1]):
			if i > ma_feature_size:
				break;
			x = []
			x.append(str(i))
			x.append(item)
			sort.append(x)
		sort.sort(cmp = lambda x,y: cmp(x[1],y[1]))
		x='v_ma'
		for i in sort:
			x = x+i[0]
		ret.append(x)

		v_1=volume_ma[adj_1][0]
		v=volume_ma[index][0]
		vb=(int)((v/v_1)*10)
		if vb > 30:
			vb = (vb/10)*10
		ret.append('vb='+str(vb))
		return ret

	def feature_kline(self, exchange, index, kline):
		ret = []
		k_el = (int)(kline[index][4]*10)
		ret.append('k_el'+str(k_el))
		ret.append('quekou=' + str(kline[index][5]))
		ret.append('baoxian=' + str(kline[index][6]))
		state='state='
		for i in range(-4,1):
			adj = self.fix_index(i)
			state = state + self.__get_state(adj, exchange, kline)
		ret.append(state)
		return ret

	def feature_exchange(self, index, exchange):
		return []
