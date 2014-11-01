#!/usr/bin/python
#!coding=utf-8
import score

class stockscore():
	day1 = score.score()
	day3 = score.score()
	day5 = score.score()
	day10 = score.score()
	day20 = score.score()
	day30 = score.score()

	def reset(self):
		self.day1.reset()
		self.day3.reset()
		self.day5.reset()
		self.day10.reset()
		self.day20.reset()
		self.day30.reset()

	def __fix_index(self, current, size, increase):
		ret = current + increase
		if ret > (size - 1):
			ret = size - 1
		return ret

	def normalize(self, list):
		sum = 0
		ret = []
		for item in list:
			sum = sum + item
		for item in list:
			nor = (float(item)/float(sum))*100.0
			ret.append(nor)
		return ret

	def update(self, current, index, low, middle, high):
		size = len(middle)
		index1 = self.__fix_index(index, size, 1)
		self.day1.update(current, low[index1], middle[index1], high[index1])
		index3 = self.__fix_index(index, size, 3)
		self.day3.update(current, low[index3], middle[index3], high[index3])
		index5 = self.__fix_index(index, size, 5)
		self.day5.update(current, low[index5], middle[index5], high[index5])
		index10 = self.__fix_index(index, size, 10)
		self.day10.update(current, low[index10], middle[index10], high[index10])
		index20 = self.__fix_index(index, size, 20)
		self.day20.update(current, low[index20], middle[index20], high[index20])
		index30 = self.__fix_index(index, size, 30)
		self.day30.update(current, low[index30], middle[index30], high[index30])

	def get_level(self):
		return self.day1.get_level()
