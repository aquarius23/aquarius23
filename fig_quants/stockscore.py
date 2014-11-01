#!/usr/bin/python
#!coding=utf-8
import score

class stockscore():
	days = [1,3,5,10,20,30]
	days_score = []
	for day in days:
		day_score = score.score()
		days_score.append(day_score)

	def reset(self):
		for score in self.days_score:
			score.reset()

	def __fix_index(self, current, size, increase):
		ret = current + increase
		if ret > (size - 1):
			ret = size - 1
		return ret

	def __normalize(self, list):
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
		index_day = 0
		for day in self.days:
			real_index = self.__fix_index(index, size, day)
			self.days_score[index_day].update(current, low[real_index], middle[real_index], high[real_index])
			index_day = index_day + 1

	def get_level(self):
		return self.days_score[0].get_level()

	def __common_get(self, name):
		ret = []
		for score in self.days_score:
			if name == 'low':
				ret.append(self.__normalize(score.get_low()))
			elif name == 'middle':
				ret.append(self.__normalize(score.get_middle()))
			elif name == 'high':
				ret.append(self.__normalize(score.get_high()))
		return ret
