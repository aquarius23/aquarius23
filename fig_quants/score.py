#!/usr/bin/python
#!coding=utf-8

class score():
	level = [-30.0, -20.0, -10.0, -5.0, -3.0, -1.0, 1, 3, 5, 10, 20, 30]
	low = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	middle = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def reset(self):
		self.low = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.middle = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def cal_level(self, ratio):
		pos = 0;
		for l in self.level:
			if ratio <= l:
				break
			pos = pos + 1
		return pos

	def update(self, current, low, middle, high):
		low = (low - current) / current
		middle = (middle - current) / current
		high = (high - current) / current
		low_pos = self.cal_level(low*100)
		middle_pos = self.cal_level(middle*100)
		high_pos = self.cal_level(high*100)
		self.low[low_pos] = self.low[low_pos] + 1
		self.middle[middle_pos] = self.middle[middle_pos] + 1
		self.high[high_pos] = self.high[high_pos] + 1

	def get_level(self):
		return self.level

	def get_low(self):
		return self.low

	def get_high(self):
		return self.high

	def get_middle(self):
		return self.middle

