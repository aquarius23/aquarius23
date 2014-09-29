#!/usr/bin/python
#!coding=utf-8
import sys
import string

class kdj():

	def find_low_high(self, list):
		low = sys.float_info.max;
		high = 0.0;
		for day in list:
			if day[3] < low:
				low = day[3]
			if day[4] > high:
				high = day[4]
		return low, high

	def cal_kdj(self, list):
		K = 50
		D = 50
		J = 50
		J2 = 50
		nine = []
		for day in list:
			if len(nine) < 9:
				nine.append(day)
			else:
				nine.remove(nine[0])
				nine.append(day)
				low, high = self.find_low_high(nine)
				end = day[2]
				RSV = (end-low)/(high-low)*100.0
				K = K*(2.0/3.0) + RSV*(1.0/3.0)
				D = D*(2.0/3.0) + K*(1.0/3.0)
				J = 3*K - 2*D
				J2 = 3*D - 2*K
			print K
			print D
			print J
			print J2
			print '----------'
