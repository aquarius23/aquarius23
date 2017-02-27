#!/usr/bin/python
#!coding=utf-8
import os
import zlib

def __validate_path(path, db):
	pathlist = path.split('/')
	file = db
	for i in pathlist:
		file = file + '/' + i
		if os.path.exists(file) == False:
			try:
				os.mkdir(file)
			except:
				if os.path.exists(file):
					print file + 'already exist'

def write_file(path, file, buf, db):
	__validate_path(path, db)
	file = db + '/' + path + '/' + file
	value = zlib.compress(buf)
	f = open(file, 'wb')
	f.write(value)
	f.flush()
	f.close()

def is_file_exist(path, file, db):
	file = db + '/' + path + '/' + file
	return os.path.exists(file)

def read_file(path, file, db):
	buf = ''
	if is_file_exist(path, file, db) == False:
		return ''
	file = db + '/' + path + '/' + file
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

