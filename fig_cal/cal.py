#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string

def cal_ratio(count, ratio):
	ratio = 1.0 + float(ratio)
	return pow(ratio, count)

def cal_month_money(money, month, ratio):
	ratio = float(ratio) / 1200
	factor = cal_ratio(month, ratio)
	month_money = (money * ratio * factor) / (factor - 1)
	return month_money

def cal_money_fund_ratio(ratio, day):
	return cal_ratio(day, float(ratio) / 36500)

def cal_money_fund_month(money, ratio):
	return money * cal_money_fund_ratio(ratio, 30)

def cal_pinan_money(money, month, ratio, fund_ratio):
	receive = cal_month_money(money, month, ratio)
	total = receive
	for i in range(1, month):
		fund = cal_money_fund_month(total, fund_ratio)
		total = fund + receive
	return total

def cal_pinan_ratio(money, month, ratio, fund_ratio):
	money = cal_pinan_money(money, month, ratio, fund_ratio) - money
	return (money * 12) / (month * 100)

ratio = cal_pinan_ratio(10000, 36, 8.61, 5)
print ratio
