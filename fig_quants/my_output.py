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

if len(sys.argv) == 3:
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	file1 = read_file(file1)
	list1 = get_result(file1)
	for x in list1:
		print x
