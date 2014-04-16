#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string
import parser_common

def open_file(file):
	f = open(file, 'rb')
	f.seek(0, 2)
	size = f.tell()
	f.seek(0)
	buffer = f.read(size)
	f.close()
	return buffer

argc = len(sys.argv)
if argc < 2 + 1:
	print '     Help:'
	print '     ftrace file cmd [ms]'
	print '     cmd: sum'
else:
	file = sys.argv[1]
	cmd = sys.argv[2]
	time = 0;
	if(argc == 4):
		time = sys.argv[3]
	parser = parser_common.ftrace_parser()
	parser.parser_ftrace(open_file(file), cmd, time)
