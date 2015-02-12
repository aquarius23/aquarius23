#!/usr/bin/python
#!coding=utf-8
import sys
import string

def read_file(file):
	value = ''
	f = open(file, 'rb')
	if f:
		f.seek(0, 2)
		size = f.tell()
		f.seek(0)
		value = f.read(size)
	return value

def get_result(buffer):
	ret = []
	lines = buffer.split('\n')
	for line in lines:
		if len(line) > 0 and line[0] == '[':
			line = line.replace('\'', '')
			line = line.replace('(', '')
			line = line.replace(')', '')
			line = line.replace(' ', '')
			line = line[1:-1].split(',')
			result = []
			for i, item in enumerate(line):
				if i != 0:
					item = string.atof(item)
				result.append(item)
			ret.append(result)
	return ret

def filter_list(list, threshold):
	ret = []
	for item in list:
		p = item[-1]
		if p > threshold:
			ret.append(item)
	return ret

def find_item(list, name):
	for item in list:
		if item[0] == name:
			return item
	return []

def cal_result(result, filter, list, index):
	for item in filter:
		name = item[0]
		exist = find_item(result, name)
		if exist == []:
			new = []
			new.append(name)
			print 'new item:' + name
			another = find_item(list, name)
			if index == 0:
				new.append(item)
				new.append(another)
			else:
				new.append(another)
				new.append(item)
			result.append(new)

def final_result(list1, list2):
	result = []
	filter1 = filter_list(list1, 0.7)
	filter2 = filter_list(list2, 0.7)
	cal_result(result, filter1, list2, 0)
	print '------------------------'
	cal_result(result, filter2, list1, 1)
	return result

if len(sys.argv) == 3:
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	file1 = read_file(file1)
	list1 = get_result(file1)
	file2 = read_file(file2)
	list2 = get_result(file2)
	output = final_result(list1, list2)
	for x in output:
		print '-----'
		for y in x:
			print y
