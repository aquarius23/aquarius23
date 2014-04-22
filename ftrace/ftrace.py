#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string
import parser_common
import parser_task

def open_file(file):
	f = open(file, 'rb')
	f.seek(0, 2)
	size = f.tell()
	f.seek(0)
	buffer = f.read(size)
	f.close()
	return buffer

def help():
	print '     Help:'
	print '     ftrace file cmdline [ms]'
	print '     cmdline:'
	print '            sum name=id'
	print '            top [num]'
	print '            block num'

def get_task(ms):
	parser = parser_common.ftrace_parser()
	parser.parser_ftrace(open_file(file))
	result = parser.get_result()

	task = parser_task.ftrace_task()
	if ms > 0:
		task.select_time_slice(ms)
	task.parser_task(result)
	return task

argc = len(sys.argv) - 1
if argc < 2:
	help()
else:
	file = sys.argv[1]
	cmd = sys.argv[2]

	time = []
	result = []
	if cmd == 'sum':
		if argc < 3:
			help()
		else:
			name = sys.argv[3].split('=')
			id = name[1]
			name = name[0]
			ms = 0
			if argc == 4:
				ms = string.atoi(sys.argv[4])
			task = get_task(ms)
			result = []
			if name == 'task':
				time, result = task.task_percent(id)
			elif name == 'irq':
				time, result = task.irq_percent(id)
			elif name == 'softirq':
				time, result = task.softirq_percent(id)

			count = 0
			for slice in time:
				print slice
				item = result[count]
				print item
				count = count + 1
	elif cmd == 'top':
		ms = 0
		num = 0
		if argc >= 3:
			num = string.atoi(sys.argv[3])
			if argc >= 4:
				ms = string.atoi(sys.argv[4])
		task = get_task(ms)
		time, result = task.top(num)
		count = 0
		for slice in time:
			print slice
			for item in result[count]:
				print item
			count = count + 1
			print '--------------------------'
	elif cmd == 'block':
		if argc < 3:
			help()
		else:
			task = get_task(0)
			num = string.atoi(sys.argv[3])
			result = task.find_kernel_block(num)
			for cpu in result:
				print '-------------------------------------'
				for item in cpu:
					print item
