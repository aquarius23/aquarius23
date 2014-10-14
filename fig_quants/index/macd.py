#!/usr/bin/python
#!coding=utf-8
import string

#[DIF,DEA,MACD]
class macd():
	def cal_macd(self, list):
		EMA12 = list[0][2]
		EMA26 = EMA12
		DIF = 0
		DEA = 0
		MACD = 0
		ret = []
		for day in list:
			result = []
			end = day[2]
			EMA12 = EMA12*(11.0/13.0) + end*(2.0/13.0)
			EMA26 = EMA26*(25.0/27.0) + end*(2.0/27.0)
			DIF = EMA12 - EMA26
			DEA = DEA*(8.0/10.0) + DIF*(2.0/10.0)
			MACD = 2*(DIF-DEA)
			#result.append(day[0])
			result.append(DIF)
			result.append(DEA)
			result.append(MACD)
			ret.append(result)
		return ret
