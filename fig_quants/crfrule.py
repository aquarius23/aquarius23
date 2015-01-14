#!/usr/bin/python
#!coding=utf-8
import crfrulebase
import stockconfig

class crfrule(crfrulebase.crfrulebase):
	crf_day = -stockconfig.FIG_CRF_DAY
	def __get_state(self, index, exchange, kline):
		today = kline[index][0]
		if today >= 1:
			if today >= 3:
				if today >= 5:
					today = 5
				else:
					today = 3
			else:
				today = 1
		elif today <= -1:
			if today <= -3:
				if today <= -5:
					today = -5
				else:
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
		ret = []
		kd_trend = []
		kdj_sort = []
		j_trend = []
		for i in range(self.crf_day,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			k = kdj[adj][0]
			d = kdj[adj][1]
			kd_trend.append(self.compare(k, d))
			j_trend.append(self.compare(kdj[adj][2], kdj[adj_1][2]))
			kdj_sort.append(kdj[adj][2])
		ret.append(self.build_sort_feature('kdj_s', kdj_sort))
		ret.extend(self.build_feature('kd_t', kd_trend))
		ret.extend(self.build_feature('j_t', j_trend))
		return ret

	def feature_macd(self, exchange, index, macd):
		ret = []
		macd1_sort = []
		macd2_sort = []
		macd3_sort = []
		macd1_trend = []
		macd12_trend = []
		for i in range(self.crf_day,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			y = macd[adj_1][2]
			t = macd[adj][2]
			macd1_trend.append(self.compare(t, y))
			dif = macd[adj][0]
			dea = macd[adj][1]
			macd12_trend.append(self.compare(dif, dea))
			macd1_sort.append(macd[adj][0])
			macd2_sort.append(macd[adj][1])
			macd3_sort.append(macd[adj][2])
		ret.append(self.build_sort_feature('macd1_s', macd1_sort))
		ret.append(self.build_sort_feature('macd2_s', macd2_sort))
		ret.append(self.build_sort_feature('macd3_s', macd3_sort))
		ret.extend(self.build_feature('macd1_t', macd1_trend))
		ret.extend(self.build_feature('macd12_t', macd12_trend))
		return ret

	def feature_boll(self, exchange, index, boll):
		ret = []
		boll_s_trend = []
		boll_e_trend = []
		boll_l_trend = []
		boll_h_trend = []
		for i in range(self.crf_day,1):
			adj = self.fix_index(i)
			mb = boll[adj][0]
			up = boll[adj][1]
			dn = boll[adj][2]
			start = exchange[adj][1]
			end = exchange[adj][2]
			low = exchange[adj][3]
			high = exchange[adj][4]
			boll_s_trend.append(self.cal_position(start, mb, up, dn))
			boll_e_trend.append(self.cal_position(end, mb, up, dn))
			boll_l_trend.append(self.cal_position(low, mb, up, dn))
			boll_h_trend.append(self.cal_position(high, mb, up, dn))
		ret.extend(self.build_feature('boll_s', boll_s_trend))
		ret.extend(self.build_feature('boll_e', boll_e_trend))
		ret.extend(self.build_feature('boll_l', boll_l_trend))
		ret.extend(self.build_feature('boll_h', boll_h_trend))
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
		ma10_sort = []
		ma5s_trend = []
		ma5e_trend = []
		ma5l_trend = []
		ma5h_trend = []
		ma10s_trend = []
		ma10e_trend = []
		ma10l_trend = []
		ma10h_trend = []
		for i in range(self.crf_day,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			y = ma[adj_1][0]
			t = ma[adj][0]
			t5 = ma[adj][2]
			t10 = ma[adj][3]
			start = exchange[adj][1]
			end = exchange[adj][2]
			low = exchange[adj][3]
			high = exchange[adj][4]
			ma1_sort.append(ma[adj][0])
			ma3_sort.append(ma[adj][1])
			ma5_sort.append(ma[adj][2])
			ma10_sort.append(ma[adj][3])
			ma5s_trend.append(self.compare(start, t5))
			ma5e_trend.append(self.compare(end, t5))
			ma5l_trend.append(self.compare(low, t5))
			ma5h_trend.append(self.compare(high, t5))
			ma10s_trend.append(self.compare(start, t10))
			ma10e_trend.append(self.compare(end, t10))
			ma10l_trend.append(self.compare(low, t10))
			ma10h_trend.append(self.compare(high, t10))
		ret.append(self.build_sort_feature('ma1_s', ma1_sort))
		ret.append(self.build_sort_feature('ma3_s', ma3_sort))
		ret.append(self.build_sort_feature('ma5_s', ma5_sort))
		ret.append(self.build_sort_feature('ma10_s', ma10_sort))
		ret.extend(self.build_feature('ma5s_t', ma5s_trend))
		ret.extend(self.build_feature('ma5e_t', ma5e_trend))
		ret.extend(self.build_feature('ma5l_t', ma5l_trend))
		ret.extend(self.build_feature('ma5h_t', ma5h_trend))
		ret.extend(self.build_feature('ma10s_t', ma10s_trend))
		ret.extend(self.build_feature('ma10e_t', ma10e_trend))
		ret.extend(self.build_feature('ma10l_t', ma10l_trend))
		ret.extend(self.build_feature('ma10h_t', ma10h_trend))

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

		ma1_sort = []
		ma3_sort = []
		ma5_sort = []
		ma10_sort = []
		for i in range(self.crf_day,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			ma1_sort.append(volume_ma[adj][0])
			ma3_sort.append(volume_ma[adj][1])
			ma5_sort.append(volume_ma[adj][2])
			ma10_sort.append(volume_ma[adj][3])
		ret.append(self.build_sort_feature('vma1_s', ma1_sort))
		ret.append(self.build_sort_feature('vma3_s', ma3_sort))
		ret.append(self.build_sort_feature('vma5_s', ma5_sort))
		ret.append(self.build_sort_feature('vma10_s', ma10_sort))

		vbx = []
		for i in range(self.crf_day,1):
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
		for i in range(self.crf_day,1):
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
		for i in range(self.crf_day,1):
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
		kl0=[]
		kl1=[]
		kl2=[]
		kl4=[]
		kl5=[]
		kl6=[]
		for i in range(self.crf_day,1):
			adj = self.fix_index(i)
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
		ret.extend(self.build_feature('kl0-', kl0))
		ret.extend(self.build_feature('kl1-', kl1))
		ret.extend(self.build_feature('kl2-', kl2))
		ret.extend(self.build_feature('kl4-', kl4))
		ret.extend(self.build_feature('kl5-', kl5))
		ret.extend(self.build_feature('kl6-', kl6))
		return ret

	def feature_exchange(self, index, exchange):
		return []

	def feature_flow(self, exchange, index, flow):
		ret = []
		diff = []
		trend = []
		trend_big = []
		dir = []
		dir_big = []
		for i in range(self.crf_day,1):
			adj = self.fix_index(i)
			adj_1 = self.fix_index(i-1)
			trend.append(self.compare(flow[adj][2], flow[adj_1][2]))
			trend_big.append(self.compare(flow[adj][3], flow[adj_1][3]))
			diff.append(self.compare(flow[adj][2], flow[adj][3]))
			dir.append(self.compare(flow[adj][2], 0))
			dir_big.append(self.compare(flow[adj][3],0))
		ret.extend(self.build_feature('fl_tr', trend))
		ret.extend(self.build_feature('fl_trb', trend_big))
		ret.extend(self.build_feature('fl_dif', diff))
		ret.extend(self.build_feature('fl_dir', dir))
		ret.extend(self.build_feature('fl_dirb', dir_big))
		return ret
