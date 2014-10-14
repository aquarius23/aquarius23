#!/usr/bin/python
#!coding=utf-8
import sys
import string

#[low,high][1,3,5,10,20,30]
class price_range():

	def find_low_high(self, list):
		low = sys.float_info.max;
		high = 0.0;
		for day in list:
			if day[0] < low:
				low = day[0]
			if day[1] > high:
				high = day[1]
		return low, high

	def cal_range(self, list):
		three = []
		five = []
		ten = []
		twenty = []
		thirty = []
		ret_l = []
		ret_h = []
		for day in list:
			result_l = []
			result_h = []
			end = day[3:5]

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

			low = end[0]
			high = end[1]
			result_l.append(low)
			result_h.append(high)

			low,high = self.find_low_high(three)
			result_l.append(low)
			result_h.append(high)

			low,high = self.find_low_high(five)
			result_l.append(low)
			result_h.append(high)

			low,high = self.find_low_high(ten)
			result_l.append(low)
			result_h.append(high)

			low,high = self.find_low_high(twenty)
			result_l.append(low)
			result_h.append(high)

			low,high = self.find_low_high(thirty)
			result_l.append(low)
			result_h.append(high)

			ret_l.append(result_l)
			ret_h.append(result_h)
		return ret_l, ret_h
