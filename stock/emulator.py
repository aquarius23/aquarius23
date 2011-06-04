#!/usr/bin/python
#!coding=utf/-8

import string
import time
import interface

def parser_rules(str):
	rules = []
	str = str.split(';')
	for s in str:
		rule_and = []
		str_and = s.split('&')
		for a in str_and:
			rule_or = []
			str_or = a.split('|')
			for o in str_or:
				rule_or.append(o)
			rule_and.append(rule_or)
		rules.append(rule_and)
	return rules

def last_month(day):
	day = day.split('-')
	year = string.atoi(day[0])
	month = string.atoi(day[1])
	day = string.atoi(day[2])
	if month > 1:
		month -= 1
	else:
		month = 12
		year -= 1
	return '%4d-%02d-%02d' %(year, month, day)

class exchange_emu():
	stock_db = interface.stock_al()
	def set_parameter(self, money, tax, hand, start_day, end_day):
		self.money = float(money)
		self.tax = float(tax)
		self.hand = float(hand)
		self.start_day = start_day
		self.end_day = end_day
		self.stock_pool = []
		self.stock_index = []
		self.rules = []

	def add_rules(self, buy, sell):
		rule = []
		rule.append(parser_rules(buy))
		rule.append(parser_rules(sell))
		self.rules.append(rule)
	
	def add_stock(self, index):
		if index == 'all':
			self.stock_index = self.stock_db.get_stock_list()
		else:
			self.stock_index.append(index)

	def __get_token_list(self, rule):
		token = []
		i = 0
		n = len(rule)
		parentheses = 0
		while(i < n):
			c = rule[i]
			if c == ' ':
				pass
			elif c == '(':
				parentheses = i + 1
			elif c == ')':
				number = string.atoi(rule[parentheses:i])
				token.append(number)
				parentheses = 0
			elif parentheses == 0:
				token.append(c)
			i += 1
		return token

	def __find_max_min(self, start, end, ismax, char):
		if start < 0:
			start = 0
		pos = 0
		ret = 0
		if char == 'S':
			pos = 1
		elif char == 'E':
			pos = 2
		elif char == 'H':
			pos = 3
		elif char == 'L':
			pos = 4
		elif char == 'N':
			pos = 5
		for i in range(start, end):
			value = string.atof(self.list[i][pos])
			if ismax == 1:
				if value > ret:
					ret = value
			else:
				if ret == 0:
					ret = value
				elif value < ret:
					ret = value
		return ret

	def __safe_minus(self, op1, op2):
		ret = op1 - op2
		if ret < 0:
			ret = 0
		return ret

	def __calculate_token(self, token, index):
		op = []
		n = len(token)
		i = 0
		while(i < n):
			c = token[i]
			if c == '[':
				i += 1
				sub = []
				rstack = 1
				while(rstack > 0):
					if token[i] == ']':
						rstack -= 1
						if rstack > 0:
							sub.append(token[i])
					else:
						if token[i] == '[':
							rstack += 1
						sub.append(token[i])
					i += 1
				i -= 1
				c = self.__calculate_token(sub, index)
			elif c == 'V':
				i += 1
				days = token[i]
				i += 1
				sub = []
				if token[i] == '[':
					i += 1
					rstack = 1
					while(rstack > 0):
						if token[i] == ']':
							rstack -= 1
							if rstack > 0:
								sub.append(token[i])
						else:
							if token[i] == '[':
								rstack += 1
							sub.append(token[i])
						i += 1
					i -= 1
				else:
					sub.append(token[i])
					sub.append(0)
				sum = 0
				count = 0
				start = self.__safe_minus(index, abs(days))
				for day in range(start, index):
					sum += self.__calculate_token(sub, day)
					count += 1
				if count == 0: # new stock
					c = self.__calculate_token(sub, index)
				else:
					c = sum / count # Some date/stock has no exchange
			elif c == 'S':
				i += 1
				index = self.__safe_minus(index, abs(token[i]))
				c = string.atof(self.list[index][1])
			elif c == 'E':
				i += 1
				index = self.__safe_minus(index, abs(token[i]))
				c = string.atof(self.list[index][2])
			elif c == 'H':
				i += 1
				index = self.__safe_minus(index, abs(token[i]))
				c = string.atof(self.list[index][3])
			elif c == 'L':
				i += 1
				index = self.__safe_minus(index, abs(token[i]))
				c = string.atof(self.list[index][4])
			elif c == 'N':
				i += 1
				index = self.__safe_minus(index, abs(token[i]))
				c = string.atoi(self.list[index][5])
			elif c == 'X':
				i += 1
				index = self.__safe_minus(index, abs(token[i]))
				c = string.atoi(self.list[index][6]) / string.atoi(self.list[index][5])
				c = float(c) / 100
			elif c == 'M':
				i += 1
				c = token[i]
				i += 1
				start = self.__safe_minus(index, abs(token[i]))
				c = self.__find_max_min(start, index, 1, c)
			elif c == 'W':
				i += 1
				c = token[i]
				i += 1
				start = self.__safe_minus(index, abs(token[i]))
				c = self.__find_max_min(start, index, 0, c)

			if len(op) == 0:
				op.append(c)
			elif len(op) == 2:
				op2 = op.pop()
				op1 = op.pop()
				if op2 == '+':
					c = op1 + c
				elif op2 == '-':
					c = op1 - c
				elif op2 == '*':
					c = op1 * c
				elif op2 == '/':
					c = op1 / c
				elif op2 == '%':
					c = op1*c/100
				op.append(c)
			elif c == '+':
				op.append(c)
			elif c == '-':
				op.append(c)
			elif c == '*':
				op.append(c)
			elif c == '/':
				op.append(c)
			elif c == '%':
				op.append(c)
			i += 1

		c = op.pop()
		return c

	def __compile_rule(self, rule, cost):
		ins = []
		rule = rule.split(':')
		if len(rule) >= 3:
			for item in rule:
				if len(ins) == 1: #0< 1<= 2= 3>= 4>
					if item[0] == '=':
						op = 2
					elif item[0] == '<':
						if len(item) > 1 and item[1] == '=':
							op = 1
						else:
							op = 0
					else:
						if len(item) > 1 and item[1] == '=':
							op = 3
						else:
							op = 4
					ins.append(op)
				else:
					token = self.__get_token_list(item)
					ins.append(self.__calculate_token(token, self.iterate))
		elif len(rule) == 1:
			rule = rule[0]
			token = self.__get_token_list(rule)
			ins.append(token[0])
			percent = float(abs(token[1]))
			if token[0] == '^':
				price = cost*(100 + percent)/100
			elif token[0] == '!':
				price = cost*(100 - percent)/100
			ins.append(price)
		return ins

	def __compare_rule(self, rule):
		opx = len(rule)
		ret = 0
		ret2 = 0
		if opx > 3:
			ret =  rule.pop()
		op1 = rule[0]
		op2 = rule[1]
		op3 = rule[2]
		if op2 == 0:
			ret2 = op1 < op3
		elif op2 == 1:
			ret2 = op1 <= op3
		elif op2 == 2:
			ret2 = op1 == op3
		elif op2 == 3:
			ret2 = op1 >= op3
		elif op2 == 4:
			ret2 = op1 > op3
		
		if ret2 == True:
			return ret
		else:
			return -1

	def __exec_buy_rule_and(self, rule):
		for or_rule in rule:
			op = self.__compile_rule(or_rule, 0)
			price = self.__compare_rule(op)
			if price >= 0:
				return price
		return -1

	def __exec_buy_rule(self, rule):
		price = float(0)
		for and_rule in rule:
			ret = self.__exec_buy_rule_and(and_rule)
			if ret < 0:
				return -1
			elif ret > 0:
				price = ret
		return price
	
	def __stock_pool_money(self, date):
		total = 0
		for stock in self.stock_pool:
			exchange = self.stock_db.get_all_list_from_date(date, stock[2], 1)
			if exchange:
				endprice = string.atof(exchange[0][2])
				total += stock[1] * endprice * 100
			else:
				total += stock[1] * stock[0] * 100
		return total

	def __print_exchange(self, date, index, isbuy, price, result):
		poolprice = self.money + self.__stock_pool_money(date)
		print '%s     %s    buy: %d     price:%f    exchange:%f/%f  remain:%f   total:%f' %(date, index, isbuy, price, price*self.hand*100, result, self.money, poolprice)

	def __real_buy(self, index, price, date, sell_rule):
		pool = []
		pool.append(price)
		pool.append(self.hand)
		pool.append(index)
		pool.append(sell_rule)
		self.stock_pool.append(pool)
		self.money -= price * self.hand * 100
		self.__print_exchange(date, index, 1, price, 0)

	def __exec_buy(self, date, index, rule):
		self.iterate =  self.date_list.index(date)
		buy_list = map(self.__exec_buy_rule, rule[0])
		for buy in buy_list:
			if buy > 0 and buy * self.hand * 100 <= self.money:
				self.__real_buy(index, buy, date, rule[1])
	
	def __exec_sell_rule_and(self, rule, stock):
		start_day = last_month(last_month(self.date))
		self.date_list = self.stock_db.get_date_list_from_date(start_day, stock[2], 1)
		if self.date not in self.date_list:
			return -1
		self.list = self.stock_db.get_all_list_from_date(start_day, stock[2], 1)
		self.iterate = self.date_list.index(self.date)
		for or_rule in rule:
			op = self.__compile_rule(or_rule, stock[0])
			if op[0] == '^':
				hprice = string.atof(self.list[self.iterate][3])
				if hprice >= op[1]:
					return op[1]
			elif op[0] == '!':
				lprice = string.atof(self.list[self.iterate][4])
				if lprice <= op[1]:
					return op[1]
			else:
				price = self.__compare_rule(op)
				if price >= 0:
					return price
		return -1

	def __exec_sell_rule(self):
		sell_pool = []
		for stock in self.stock_pool:
			price = -1
			for rule in stock[3]:
				for and_rule in rule:
					ret = self.__exec_sell_rule_and(and_rule, stock)
					if ret < 0:
						price = ret
						break
					elif ret > 0:
						price = ret
				if price > 0:
					temp = []
					temp.append(stock)
					temp.append(price)
					sell_pool.append(temp)
					break
		
		for stock in sell_pool:
			self.stock_pool.remove(stock[0])
		return sell_pool
	
	def __real_sell(self, cost, price, hand, date, index):
		money = price * self.hand * 100
		money = money * (1000 - self.tax) / 1000
		result = money - cost * self.hand * 100
		self.money += money
		self.__print_exchange(date, index, 0, price, result)

	def __exec_sell(self, date):
		sell_list = self.__exec_sell_rule()
		for sell in sell_list:
			price = sell[1]
			hand = sell[0][1]
			cost = sell[0][0]
			index =  sell[0][2]
			self.__real_sell(cost, price, hand, date, index)

	def __real_range(self, date):
		if self.start_day <= date and date <= self.end_day:
			return 1
		else:
			return 0

	def __execute(self, date):
		self.date = date
		self.__exec_sell(date)
		for index in self.stock_index:
			start_day = last_month(self.start_day)
			start_day = last_month(start_day)
			self.date_list = self.stock_db.get_date_list_from_date(start_day, index, 1)
			if date in self.date_list:
				self.list = self.stock_db.get_all_list_from_date(start_day, index, 1)
				for rule in self.rules:
					self.__exec_buy(date, index, rule)

	def execute(self):
		date_list = self.stock_db.get_date_list_from_date(self.start_day, '000001', 0)
		map(self.__execute, filter(self.__real_range, date_list))

xx = exchange_emu()
xx.set_parameter('100000', '3', '1', '2011-04-26', '2011-06-10')
xx.add_stock('600015')
xx.add_stock('all')
xx.add_rules('V(20)N%(65):>:N(-1)&ME(20)%(75):>:E(-1)&L(-2):>:E(-1)&E(-1):<:L(0):E(0)', '^(15);^(2)&[H(0)-L(0)]%(50):>:[H(-1)-L(-1)]&[H(0)-L(0)]%(5):>:[H(0)-E(0)]:E(0)')
xx.execute()
