#!/usr/bin/python
#!coding=utf-8
import string

#[end-y_end, end-start, high-low, $2/$3, end_level, 缺口, 包线]
class kline():
	def cal_kline(self, list):
		y_e = list[0][2]
		y_l = list[0][3]
		y_h = list[0][4]
		ret = []
		for day in list:
			result = []
			low = day[3]
			high = day[4]
			start = day[1]
			end = day[2]
			range_ratio = (high - low) / y_e
			day_ratio = (end - y_e) / y_e
			k_ratio = (end - start) / y_e
			result.append(day_ratio*100)
			result.append(k_ratio*100)
			result.append(range_ratio*100)
			if range_ratio == 0:
				result.append(1.0)
				result.append(1.0)
			else:
				result.append(abs(k_ratio)/range_ratio)
				result.append((end-low)/(high-low))

			if low > y_h:
				result.append(1)
			elif high < y_l:
				result.append(-1)
			else:
				result.append(0)

			if k_ratio > 0:
				if start < y_l and end > y_h:
					result.append(1)
				else:
					result.append(0)
			elif k_ratio < 0:
				if start > y_h and end < y_l:
					result.append(-1)
				else:
					result.append(0)
			else:
				result.append(0)

			ret.append(result)
			y_e = end
			y_l = low
			y_h = high
		return ret
