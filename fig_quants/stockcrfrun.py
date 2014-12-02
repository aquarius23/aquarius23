#!/usr/bin/python
#!coding=utf-8
import stockrun

class stockcrfrun(stockrun.stockrun):
	chain = 5
	size = 0
	crftag = []
	crffeature = []

	def reset(self):
		self.size = 0
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
		self.size = len(exchange)
		self.feed_stock(exchange)

	def tag_feature(self):
		if self.size >= self.chain:
			for i in range(0, self.size):
				tag, feature = self.get_lable_feature(i)
				tag, feature = self.set_tag_feature(tag, feature)
				if tag != []:
					yield tag, feature
