#!/usr/bin/python
#!coding=utf-8
import sys
import string

class ma():

	def __cal_ma(self, list):
		count = 0
		MA = 0.0
		for value in list:
			MA = MA + value
			count = count + 1
		MA = MA/count
		return MA

	def cal_ma(self, list):
		three = []
		five = []
		ten = []
		twenty = []
		thirty = []
		ret = []
		for day in list:
			result = []
			end = day[2]

			if len(three) < 3:
				three.append(end)
			else:
				three.remove(three[0])
				three.append(end)

			if len(five) < 5:
				five.append(end)
			else:
				five.remove(five[0])
				five.append(end)

			if len(ten) < 10:
				ten.append(end)
			else:
				ten.remove(ten[0])
				ten.append(end)

			if len(twenty) < 20:
				twenty.append(end)
			else:
				twenty.remove(twenty[0])
				twenty.append(end)

			if len(thirty) < 30:
				thirty.append(end)
			else:
				thirty.remove(thirty[0])
				thirty.append(end)

			result.append(end)
			result.append(self.__cal_ma(three))
			result.append(self.__cal_ma(five))
			result.append(self.__cal_ma(ten))
			result.append(self.__cal_ma(twenty))
			result.append(self.__cal_ma(thirty))
			ret.append(result)
		return ret
