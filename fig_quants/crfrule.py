#!/usr/bin/python
#!coding=utf-8
import crfrulebase

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
			sort.append(item)
		ret.append(self.build_sort_feature('j_sort=', sort))

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
			sort.append(item)
		ret.append(self.build_sort_feature('macd_sort=', sort))
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
		adj_1 = self.fix_index(-1)
		adj_2 = self.fix_index(-2)

		sort = []
		for item in boll[index]:
			sort.append(item)
		sort.append(exchange[index][2])
		ret.append(self.build_sort_feature('boll', sort))

		sort = []
		for item in boll[adj_1]:
			sort.append(item)
		sort.append(exchange[adj_1][2])
		ret.append(self.build_sort_feature('boll_1', sort))

		sort = []
		for item in boll[adj_2]:
			sort.append(item)
		sort.append(exchange[adj_2][2])
		ret.append(self.build_sort_feature('boll_2', sort))

		return ret

	def feature_ma(self, exchange, index, ma):
		ret = []
		adj_1 = self.fix_index(-1)
		adj_2 = self.fix_index(-2)

		sort = []
		for item in ma[index]:
			sort.append(item)
		ret.append(self.build_sort_feature('ma', sort))

		sort = []
		for item in ma[adj_1]:
			sort.append(item)
		ret.append(self.build_sort_feature('ma_1', sort))

		sort = []
		for item in ma[adj_2]:
			sort.append(item)
		ret.append(self.build_sort_feature('ma_2', sort))

		ma1_sort = []
		ma3_sort = []
		ma5_sort = []
		ma1_trend = []
		for i in range(-5,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			y = ma[adj_1][0]
			t = ma[adj][0]
			if t > y:
				ma1_trend.append('+')
			elif t < y:
				ma1_trend.append('-')
			else:
				ma1_trend.append('=')
			ma1_sort.append(ma[adj][0])
			ma3_sort.append(ma[adj][1])
			ma5_sort.append(ma[adj][2])
		ret.append(self.build_sort_feature('ma1_s', ma1_sort))
		ret.append(self.build_sort_feature('ma3_s', ma3_sort))
		ret.append(self.build_sort_feature('ma5_s', ma5_sort))
		ret.extend(self.build_feature('ma1_t', ma1_trend))
		return ret

	def feature_volume_ma(self, exchange, index, volume_ma):
		ret = []
		sort = []
		for item in volume_ma[index]:
			sort.append(item)
		ret.append(self.build_sort_feature('v_ma', sort))

		adj_1 = self.fix_index(-1)
		sort = []
		for item in volume_ma[adj_1]:
			sort.append(item)
		ret.append(self.build_sort_feature('v_ma_1', sort))

		adj_2 = self.fix_index(-2)
		sort = []
		for item in volume_ma[adj_2]:
			sort.append(item)
		ret.append(self.build_sort_feature('v_ma_2', sort))

		vbx = []
		for i in range(-5,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			v_1=volume_ma[adj_1][0]
			v=volume_ma[adj][0]
			vb=(int)((v/v_1)*10)
			if vb > 30:
				vb = (vb/10)*10
			vbx.append(':'+str(vb))
		ret.extend(self.build_feature('vb-', vbx))

		vbx = []
		for i in range(-5,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			v_1=volume_ma[adj_1][1]
			v=volume_ma[adj][0]
			vb=(int)((v/v_1)*10)
			if vb > 30:
				vb = (vb/10)*10
			vbx.append(':'+str(vb))
		ret.extend(self.build_feature('vb3-', vbx))

		vbx = []
		for i in range(-5,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			v_1=volume_ma[adj_1][2]
			v=volume_ma[adj][0]
			vb=(int)((v/v_1)*10)
			if vb > 30:
				vb = (vb/10)*10
			vbx.append(':'+str(vb))
		ret.extend(self.build_feature('vb5-', vbx))

		return ret

	def feature_kline(self, exchange, index, kline):
		ret = []
		state=[]
		kl0=[]
		kl1=[]
		kl2=[]
		kl4=[]
		kl5=[]
		kl6=[]
		for i in range(-5,1):
			adj = self.fix_index(i)
			state.append(':'+self.__get_state(adj, exchange, kline))
			x = (int)(kline[adj][0])
			if x > 10:
				x = 10
			elif x < -10:
				x = -10
			kl0.append(':'+str((int)(x)))
			x = (int)(kline[adj][1])
			if x > 20:
				x = 20
			elif x < -20:
				x = -20
			kl1.append(':'+str((int)(x)))
			x = (int)(kline[adj][2])
			if x > 20:
				x = 20
			kl2.append(':'+str((int)(x)))
			kl4.append(':'+str((int)(kline[index][4]*10)))
			kl5.append(':'+str(kline[index][5]))
			kl6.append(':'+str(kline[index][6]))
		ret.extend(self.build_feature('state-', state))
		ret.extend(self.build_feature('kl0-', kl0))
		ret.extend(self.build_feature('kl1-', kl1))
		ret.extend(self.build_feature('kl2-', kl2))
		ret.extend(self.build_feature('kl4-', kl4))
		ret.extend(self.build_feature('kl5-', kl5))
		ret.extend(self.build_feature('kl6-', kl6))
		return ret

	def feature_exchange(self, index, exchange):
		return []
