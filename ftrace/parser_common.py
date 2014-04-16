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
	time = string.atof(tag[2].split(':')[0])
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
		result.append(prev)
		result.append(next)
		result.append(prev_state)
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
	cpu_trace_task = {}

	def __store_log(self, line):
		cpu = line[0]
		if self.cpu_trace_full.has_key(cpu):
			self.cpu_trace_full[cpu].append(line)
		else:
			self.cpu_trace_full[cpu] = line

	def __parser_task(self, line):
		if line[2] == 'sched_wakeup':
			return
		if line[2] == 'sched_migrate_task':
			return
		if line[2] == 'sched_wakeup_new':
			return
		if line[2] == 'softirq_raise':
			return

		cpu = line[0]
		if self.cpu_trace_task.has_key(cpu):
			self.cpu_trace_task[cpu].append(line)
		else:
			self.cpu_trace_task[cpu] = line

	def parser_ftrace(self, buffer, cmd, time):
		lines = buffer.split('\n')
		for line in lines:
			tag = line.split()
			if len(tag) != 0 and tag[0] != '#':
				result = parser_line(tag)
				if result:
					self.__store_log(result)
					self.__parser_task(result)
		self.cpu = len(self.cpu_trace_full)

