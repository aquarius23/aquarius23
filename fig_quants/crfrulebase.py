#!/usr/bin/python
#!coding=utf-8

class crfrulebase():
	def set_fix_index(self, fix_index):
		self.fix_index = fix_index

	def build_feature(self, name, list):
		ret = []
		for i,item in enumerate(list):
			feature = name+str(i)+'='+item
			ret.append(feature)
		return ret

	def get_state(self, index, exchange, kline):
		return []

	def feature_macd(self, exchange, index, macd):
		return []

	def feature_kdj(self, exchange, index, kdj):
		return []

	def feature_boll(self, exchange, index, boll):
		return []

	def feature_ma(self, exchange, index, ma):
		return []

	def feature_volume_ma(self, exchange, index, volume_ma):
		return []

	def feature_price_range(self, exchange, index, low, high):
		return []

	def feature_volume_range(self, exchange, index, low, high):
		return []

	def feature_closeprice_range(self, exchange, index, low, high):
		return []

	def feature_kline(self, exchange, index, kline):
		return []

	def feature_exchange(self, index, exchange):
		return []
