#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string

def get_value(tag):
	index = tag.find('=')
	return tag[index+1:]

def get_pid(tag):
	pid = tag.split('-')[1]
	current = tag.split('>')[0][1:]
	return pid

def parser_line(tag):
	cpu = string.atoi(tag[1][3])
	time = string.atof(tag[2].split(':')[0]) * 1000
	result = []
	result.append(cpu)
	result.append(time)
	result.append(tag[3][:-1])

	if tag[3] == 'sched_migrate_task:':
		name = get_value(tag[4])
		pid = get_value(tag[5])
		orig_cpu = get_value(tag[7])
		dest_cpu = get_value(tag[8])
		state = get_value(tag[9])
		result.append(name)
		result.append(pid)
		result.append(orig_cpu)
		result.append(dest_cpu)
		result.append(state)
	elif tag[3] == 'sched_switch:':
		prev = get_value(tag[4])
		next = get_value(tag[9])
		prev_state = get_value(tag[7])
		next_pid = get_value(tag[10])
		prev_pid = get_value(tag[5])
		result.append(prev)
		result.append(prev_pid)
		result.append(prev_state)
		result.append(next)
		result.append(next_pid)
	elif tag[3] == 'irq_handler_exit:':
		irq = get_value(tag[4])
		result.append(irq)
	elif tag[3] == 'irq_handler_entry:':
		irq = get_value(tag[4])
		name = get_value(tag[5])
		result.append(name)
		result.append(irq)
	elif tag[3] == 'softirq_entry:':
		vec = get_value(tag[4])
		name = get_value(tag[5])[:-1]
		result.append(name)
		result.append(vec)
	elif tag[3] == 'softirq_exit:':
		vec = get_value(tag[4])
		name = get_value(tag[5])[:-1]
		result.append(name)
		result.append(vec)
	elif tag[3] == 'sched_wakeup:':
		name = get_value(tag[4])
		pid = get_value(tag[5])
		result.append(name)
		result.append(pid)
		#state = get_value(tag[9])
	elif tag[3] == 'softirq_raise:':
		vec = get_value(tag[4])
		name = get_value(tag[5])[:-1]
		result.append(name)
		result.append(vec)
	elif tag[3] == 'sched_wakeup_new:':
		name = get_value(tag[4])
		pid = get_value(tag[5])
		result.append(name)
		result.append(pid)
		#state = get_value(tag[9]) #always R
	else:
		#print tag
		return []
	return result


class ftrace_parser():
	cpu = 0;
	cpu_trace_full = {}

	def __store_log(self, line):
		cpu_id = line[0]
		if self.cpu_trace_full.has_key(cpu_id) == False:
			self.cpu_trace_full[cpu_id] = []
		self.cpu_trace_full[cpu_id].append(line)

	def get_cpu(self):
		return self.cpu

	def get_result(self):
		return self.cpu_trace_full

	def parser_ftrace(self, buffer):
		lines = buffer.split('\n')
		for line in lines:
			tag = line.split()
			if len(tag) != 0 and tag[0] != '#':
				result = parser_line(tag)
				if result:
					self.__store_log(result)
		self.cpu = len(self.cpu_trace_full)

