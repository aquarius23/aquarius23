#!/usr/bin/python
#!coding=utf-8
import urllib
import HTMLParser
import re
import time

def get_date():
	return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def get_web_html(url):
	err = 1
	while err:
		try:
			u = urllib.urlopen(url)
			buffer = u.read()
			u.close()
			err = 0
		except:
			err = 1
			time.sleep(2)
	return buffer

def stock_url(index, year, jidu, real_stock):
	if len(index) != 6:
		print 'bad stock code'
		return ''

	url = r'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/' + index
	if real_stock == 1:
		url = url + r'.phtml?'
	else:
		url = url + r'/type/S.phtml?'
		
	url = url + r'year=' + str(year) + r'&jidu=' + str(jidu)
	return url

def detail_url(index, year, month, day):
	if len(index) != 6:
		print 'bad stock code'
		return ''

	url = str(year) + r'-'
	if month < 10:
		url = url + '0'
	url = url + str(month) + r'-'
	if day < 10:
		url = url + '0'
	url = url + str(day) + r'&symbol='
	url = r'http://market.finance.sina.com.cn/downxls.php?date=' + url
	if index[0] == '6':
		url = url + 'sh'
	else:
		url = url + 'sz'
	url = url + index
	return url

class Stocklist(HTMLParser.HTMLParser):
	mkey = {}
	mlist = []

	def reset(self):
		HTMLParser.HTMLParser.reset(self)
		self._level_stack = []
		self.mkey = {}
		self.mlist = []

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for name,value in attrs:
				if name == 'href':
					self._level_stack.append(tag)
	
	def handle_endtag(self, tag):
		if self._level_stack \
		and tag == self._level_stack[-1]:
			self._level_stack.pop()
	
	def handle_data(self, data):
		if self._level_stack:
			pattern = re.compile('\D*[0,3,6]\d{5}\)')
			stock = pattern.match(data)
			if stock: 
				p = re.compile('\d{6}')
				number = p.search(data).group()
				if number:
					#print number
					self.mlist.append(number) 

				name = data.split('(')[0] 
				if name:
					#print name
					self.mkey[number] = name


class Indexlist(HTMLParser.HTMLParser):
	temp = []
	index = []
	count = 0

	def reset(self):
		HTMLParser.HTMLParser.reset(self)
		self._level_stack = []
		self.temp = []
		self.index =[]
		self.count = 0

	def handle_starttag(self, tag, attrs):
		if tag == 'div':
			for name,value in attrs:
				if value == 'center':
					self._level_stack.append(tag)
	
	def handle_endtag(self, tag):
		if self._level_stack \
		and tag == self._level_stack[-1]:
			self._level_stack.pop()
	
	def handle_data(self, data):
		if self._level_stack:
			date_re = re.compile('\d{4}-\d{2}-\d{2}')
			date = date_re.search(data)
			if date:
				self.temp.append(str(date.group()))
				self.count = self.count + 1
			elif data != '' and self.count != 0:
				number_re = re.compile('\d{1}')
				number = number_re.search(data)
				if(number):
					self.temp.append(str(data))
					self.count = self.count + 1

			if self.count == 7:
				self.count = 0
				self.index.append(self.temp)
				self.temp = []

class stock_parser():
	last_time = ''
	stock_kv = {}
	stock_list = []

	def __parser_stock_list(self):
		list = Stocklist()
		stocklist_html = get_web_html('http://quote.eastmoney.com/stocklist.html')
		stocklist_html = stocklist_html.decode('GBK')
		list.feed(stocklist_html)
		self.stock_kv = list.mkey
		self.stock_list = list.mlist

	def get_stock_list(self):
		if get_date() != self.last_time:
			self.last_time = get_date()
			self.__parser_stock_list()
		return self.stock_list

	def get_stock_kv(self):
		if get_date() != self.last_time:
			self.last_time = get_date()
			self.__parser_stock_list()
		return self.stock_kv

	def get_index_list(self, index, year, jidu, real_stock):
		index_html = stock_url(index, year, jidu, real_stock)
		index_html = get_web_html(index_html)
		index_html = index_html.decode('GBK')
		index = Indexlist()
		index.feed(index_html)
		#print index.index
		return index.index

	def get_detailed_exchange(self, index, year, month, day):
		exchanges = []
		exchange_html = detail_url(index, year, month, day)
		exchange_html = get_web_html(exchange_html)
		exchange_html = exchange_html.decode('GBK')
		if len(exchange_html) < 200:
			return []
		lines = exchange_html.split('\n')
		first = 1
		for line in lines:
			if first == 1:
				first = 0
			else:
				result = []
				item = line.split('\t')
				if len(item) == 6:
					result.append(item[0])
					result.append(item[1])
					result.append(item[3])
					if item[5] == u'买盘':
						result.append('1')
					elif item[5] == u'卖盘':
						result.append('-1')
					else:
						result.append('0')
					exchanges.append(result)
		return exchanges

