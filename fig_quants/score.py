#!/usr/bin/python
#!coding=utf-8
import stockmanager

class score():
	level = [-30.0, -20.0, -10.0, -5.0, -3.0, -1.0, 1, 3, 5, 10, 20, 30]
	low = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	middle = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def reset(self):
		self.low = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.middle = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def cal_level(self, ratio):
		pos = 0;
		for l in self.level:
			if ratio <= l:
				break
			pos = pos + 1
		return pos

	def update(self, current, end):
		cal_level(current)

	def get_level(self):
		return self.level

	def get_low(self):
		return self.low

	def get_high(self):
		return self.high

	def get_middle(self):
		return self.middle

