#!/usr/bin/python
#!coding=utf-8
import sqlite3

class stockdb():
	def open(self, path):
		self.db = sqlite3.connect(path)

	def close(self):
		self.db.close()

	def validate(self, table):
		cur = self.db.cursor()
		sql = 'create table if not exists ' + table + \
				'(date char(10),\
				start varchar(7),\
				end varchar(7),\
				high varchar(7),\
				low varchar(7),\
				hand varchar(13),\
				money varchar(15))'
		cur.execute(sql)
		self.db.commit()
		cur.close()

	def insert(self, table, date, start, end, high, low, hand, money):
		self.validate(table)
		cur = self.db.cursor()
		last_date = self.get_newest_date(table)
		if last_date == 'None' or cmp(date, last_date) > 0:
			sql = 'insert into ' + table + \
				' values("' + date + '","' + start + '","' + end + '","' + \
				high + '","' + low + '","' + hand + '","' + money + '")' 
			cur.execute(sql)
		else:
			print 'Already insert ' + table + ': ' + date
		
		self.db.commit()
		cur.close()

	def get_all_list(self, table, desc):
		self.validate(table)
		cur = self.db.cursor()
		sql = 'select * from ' + table + ' order by date'
		if desc == 1:
			sql += ' desc'
		cur.execute(sql)
		all = cur.fetchall()
		cur.close()
		return all

	def get_all_list_from_date(self, table, date, desc):
		self.validate(table)
		cur = self.db.cursor()
		sql = 'select * from ' + table + ' where date>="' + date + '"' + ' order by date'
		if desc == 1:
			sql += ' desc'	
		cur.execute(sql)
		all = cur.fetchall()
		cur.close()
		return all


	def get_date_list(self, table, desc):
		self.validate(table)
		cur = self.db.cursor()
		sql = 'select date from ' + table + ' order by date'
		if desc == 1:
			sql += ' desc'
		cur.execute(sql)
		all = cur.fetchall()
		cur.close()
		list = []
		for value in all:
			list.append(str(value[0]))
		return list
	
	def get_date_list_from_date(self, table, date, desc):
		self.validate(table)
		cur = self.db.cursor()
		sql = 'select date from ' + table + ' where date>="' + date + '"' + ' order by date'
		if desc == 1:
			sql += ' desc'
		cur.execute(sql)
		all = cur.fetchall()
		cur.close()
		list = []
		for value in all:
			list.append(str(value[0]))
		return list

	def get_newest_date(self, table):
		self.validate(table)
		cur = self.db.cursor()
		sql = 'select max(date) from ' + table
		cur.execute(sql)
		all = cur.fetchmany(1)
		cur.close()
		date = all[0][0]
		return str(date)

