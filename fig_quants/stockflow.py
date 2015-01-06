#!/usr/bin/python
#!coding=utf-8
import string
import stockdb
import stockparser
import stockmanager

class stockflow():
	def cal_flow(self, list):
		list.sort(cmp = lambda x,y: cmp(x[0],y[0]), reverse = True)
		size = len(list)
		sum = 0
		flow = 0
		flow_big = 0
		for i, item in enumerate(list):
			dir = item[1]
			money = item[0]
			sum = sum + money
			if dir == 1:
				flow = flow + money
			elif dir == -1:
				flow = flow - money
			if i == (size / 5): #20%
				flow_big = flow
		return sum, flow, flow_big

	def read_flow(self, index):
		db = stockdb.stockdb()
		data = db.read_data_flow(index)
		if data == '':
			return []
		list = data.split('\n')
		ret = []
		for line in list:
			day_flow = line.split(',')
			ret.append(day_flow)
		ret.sort(cmp = lambda x,y: cmp(x[0],y[0]))
		return ret

	def update_flow(self, index):
		db = stockdb.stockdb()
		flow = self.read_flow(index)
		size = len(flow)
		manager = stockmanager.stockmanager()
		days = manager.get_stock_index(index)
		for i, item in enumerate(days):
			if i < size:
				continue
			day = item[0].split('-')
			year = string.atoi(day[0])
			month = string.atoi(day[1])
			day = string.atoi(day[2])
			new = manager.get_stock_detailed(index, year, month, day)
			if new == []:
				print 'BUG(miss data): ' + str(year) + str(month) + str(day)
				parser = stockparser.stock_parser()
				detail = parser.get_detailed_exchange(index, year, month, day)
				if len(detail) > 0:
					db.write_data_day(index, detail, year, month, day)
					new = manager.get_stock_detailed(index, year, month, day)
					print 'Fixed OK!'
			record = []
			record.append(item[0])
			if new != []:
				sum, all, big = self.cal_flow(new)
				record.append(str(sum))
				record.append(str(all))
				record.append(str(big))
			flow.append(record)
		db.write_data_flow(index, flow)
