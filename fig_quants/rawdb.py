#!/usr/bin/python
#!coding=utf-8
import os
import zlib
import stockconfig

def __validate_path(path):
	pathlist = path.split('/')
	file = stockconfig.FIG_DB_PATH
	for i in pathlist:
		file = file + '/' + i
		if os.path.exists(file) == False:
			try:
				os.mkdir(file)
			except:
				if os.path.exists(file):
					print file + 'already exist'

def write_file(path, file, buf):
	__validate_path(path)
	file = stockconfig.FIG_DB_PATH + '/' + path + '/' + file
	value = zlib.compress(buf)
	f = open(file, 'wb')
	f.write(value)
	f.flush()
	f.close()

def is_file_exist(path, file):
	file = stockconfig.FIG_DB_PATH + '/' + path + '/' + file
	return os.path.exists(file)

def read_file(path, file):
	buf = ''
	if is_file_exist(path, file) == False:
		return ''
	file = stockconfig.FIG_DB_PATH + '/' + path + '/' + file
	f = open(file, 'rb')
	if f:
		f.seek(0, 2)
		size = f.tell()
		f.seek(0)
		value = f.read(size)
		try:
			buf = zlib.decompress(value)
		except Exception as err:
			print err
		f.close()
	return buf

