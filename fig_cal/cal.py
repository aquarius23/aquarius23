#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string

def cal_ratio(count, ratio):
	sum = 1
	ratio = 1.0 + float(ratio)
	for i in range(0, count):
		sum = sum * ratio
	return sum

def cal_month_money(money, month, ratio):
	ratio = float(ratio) / 1200
	factor = cal_ratio(month, ratio)
	month_money = (money * ratio * factor) / (factor - 1)
	return month_money

money = cal_month_money(500000, 12*30, 6.55)
print money
