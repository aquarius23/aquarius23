#!/usr/bin/python
#!coding=utf-8
import pywt

class stockwt():
	def __filter(self, list):
		sum = 0
		for item in list:
			sum = sum + abs(item)
		average = sum / len(list)
		for i, item in enumerate(list):
			if abs(item) < average:
				list[i] = 0

	def walelet_db(self, list):
		cA1,cD3,cD2,cD1 = pywt.wavedec(list, 'db5', level=3)
		self.__filter(cD3)
		new = pywt.waverec([cA1,cD3,cD2,cD1], 'db5')
		#print 'stockwt-----------------'
		#for i, item in enumerate(list):
			#print str(list[i]) + '--' + str(new[i])
		ret = []
		last = new[0]
		for item in new:
			day_ratio = (item - last) / last
			ret.append(day_ratio*100)
			last = item
		return ret
