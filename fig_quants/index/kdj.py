#!/usr/bin/python
#!coding=utf-8
import sys
import string

#[K,D,J,J2]
class kdj():

	def find_low_high(self, list):
		low = sys.float_info.max;
		high = 0.0;
		for day in list:
			if day[0] < low:
				low = day[0]
			if day[1] > high:
				high = day[1]
		return low, high

	def cal_kdj(self, list):
		K = 50
		D = 50
		J = 50
		J2 = 50
		nine = []
		ret = []
		for day in list:
			result = []
			if len(nine) < 9:
				nine.append(day[3:5])
			else:
				nine.remove(nine[0])
				nine.append(day[3:5])
				low, high = self.find_low_high(nine)
				end = day[2]
				RSV = (end-low)/(high-low)*100.0
				K = K*(2.0/3.0) + RSV*(1.0/3.0)
				D = D*(2.0/3.0) + K*(1.0/3.0)
				J = 3*K - 2*D
				J2 = 3*D - 2*K
			result.append(K)
			result.append(D)
			result.append(J)
			result.append(J2)
			ret.append(result)
		return ret
