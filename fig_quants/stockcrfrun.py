#!/usr/bin/python
#!coding=utf-8
import stockrun

class stockcrfrun(stockrun.stockrun):
	chain = 5
	crftag = []
	crffeature = []

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
