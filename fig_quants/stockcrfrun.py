#!/usr/bin/python
#!coding=utf-8
import stockrun
import crfrule

class stockcrfrun(stockrun.stockrun):
	chain = 5
	size = 0
	crftag = []
	crffeature = []
	crfrule = crfrule.crfrule()

	def reset(self):
		self.crftag = []
		self.crffeature = []

	def set_chain_size(self, size):
		self.chain = size

	def set_tag_feature(self, tag, feature):
		self.crftag.append(tag[:])
		self.crffeature.append(feature[:])
		if len(self.crftag) > self.chain:
			self.crftag.remove(self.crftag[0])
			self.crffeature.remove(self.crffeature[0])
		if len(self.crftag) == self.chain:
			return self.crftag, self.crffeature
		else:
			return [],[]

	def feed(self, exchange):
		self.reset()
		self.crfrule.set_fix_index(self.fix_index)
		self.size = len(exchange)
		self.feed_stock(exchange)

	def last_tag_feature(self):
		if self.size < self.chain:
			return [],[]
		self.reset()
		for i in range(self.size-self.chain, self.size):
			tag, feature = self.get_lable_feature(i)
			tag, feature = self.set_tag_feature(tag, feature)
			if tag != []:
				return tag, feature

	def tag_feature_by_index(self, index):
		if self.size < self.chain:
			return [],[]
		tag, feature = self.get_lable_feature(index)
		tag, feature = self.set_tag_feature(tag, feature)
		return tag, feature

	def tag_feature(self):
		if self.size >= self.chain:
			for i in range(0, self.size):
				tag, feature = self.get_lable_feature(i)
				tag, feature = self.set_tag_feature(tag, feature)
				if tag != []:
					yield tag, feature

	def get_state(self, index, exchange, kline):
		return self.crfrule.get_state(index, exchange, kline)

	def feature_macd(self, exchange, index, macd):
		return self.crfrule.feature_macd(exchange, index, macd)

	def feature_kdj(self, exchange, index, kdj):
		return self.crfrule.feature_kdj(exchange, index, kdj)

	def feature_boll(self, exchange, index, boll):
		return self.crfrule.feature_boll(exchange, index, boll)

	def feature_ma(self, exchange, index, ma):
		return self.crfrule.feature_ma(exchange, index, ma)

	def feature_volume_ma(self, exchange, index, volume_ma):
		return self.crfrule.feature_volume_ma(exchange, index, volume_ma)

	def feature_price_range(self, exchange, index, low, high):
		return self.crfrule.feature_price_range(exchange, index, low, high)

	def feature_volume_range(self, exchange, index, low, high):
		return self.crfrule.feature_volume_range(exchange, index, low, high)

	def feature_closeprice_range(self, exchange, index, low, high):
		return self.crfrule.feature_closeprice_range(exchange, index, low, high)

	def feature_kline(self, exchange, index, kline):
		return self.crfrule.feature_kline(exchange, index, kline)

	def feature_exchange(self, index, exchange):
		return self.crfrule.feature_exchange(index, exchange)

	def feature_flow(self, exchange, index, flow):
		return self.crfrule.feature_flow(exchange, index, flow)

