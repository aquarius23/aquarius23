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

def cal_fix_month_invest(money, month, ratio):
	sum = money
	for i in range(1, month):
		sum = money + cal_money_fund_month(sum, ratio)
	return sum

def diff_cmp(total_money, reserve_money, bank_ratio, invest_ratio, year):
	bank_orig_month = cal_month_money(total_money, year * 12, bank_ratio)
	bank_before_month = cal_month_money(total_money - reserve_money, year * 12, bank_ratio)
	bank_orig = bank_orig_month * year * 12
	bank_before = bank_before_month * year * 12
	invest_orig = reserve_money * cal_ratio(year, float(invest_ratio) / 100)
	invest_before = cal_fix_month_invest(bank_orig_month - bank_before_month, year * 12, invest_ratio)
	return (invest_orig - bank_orig) - (invest_before - bank_before - reserve_money)
diff = diff_cmp(500000, 200000, 6.55,  8.61, 30)
print diff
