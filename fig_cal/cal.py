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

def cal_money_fund_oneday(money, ratio):
	ratio = float(ratio) / 36500
	return money * ratio

def cal_money_fund_day(money, ratio):
	return money + cal_money_fund_oneday(money, ratio)

def cal_money_fund_month(money, ratio):
	for i in range(0, 30):
		money = cal_money_fund_day(money, ratio)
	return money

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
