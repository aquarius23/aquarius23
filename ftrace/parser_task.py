#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string

class ftrace_task():
	cpu_trace_task = {}
	def __stack_push(self, stack, item):
		stack.append(item)

	def __stack_pop(self, stack):
		return stack.pop()

	def __calculate_pop(self, stack, line):
		item = self.__stack_pop(stack)
		sum = 0
		while item != '-':
			sum = sum + item
			item = self.__stack_pop(stack)
		start = self.__stack_pop(stack)
		return line[1] - start[1] - sum

	def __parser_time(self, cpu_id, line, result, stack):
		if cpu_id >= 0:
			type = line[2]
			if type == 'sched_switch':
				if len(stack) > 0:
					time = self.__calculate_pop(stack, line)
					#print 'sched time: ' + str(time)
					self.__store_time(time, result, line)
				self.__stack_push(stack, line)
				self.__stack_push(stack, '-')
			elif type == 'irq_handler_entry':
				self.__stack_push(stack, line)
				self.__stack_push(stack, '-')
			elif type == 'irq_handler_exit':
				time = self.__calculate_pop(stack, line)
				self.__stack_push(stack, time)
				#print 'irq time ' + str(time)
				self.__store_time(time, result, line)
			elif type == 'softirq_entry':
				self.__stack_push(stack, line)
				self.__stack_push(stack, '-')
			elif type == 'softirq_exit':
				time = self.__calculate_pop(stack, line)
				self.__stack_push(stack, time)
				#print 'softirq time ' + str(time)
				self.__store_time(time, result, line)

	def __store_kv(self, kv, list, cpu_id):
		if kv.has_key(cpu_id) == False:
			kv[cpu_id] = []
		kv[cpu_id].append(list)

	def __store_time(self, time, kv, line):
		cpu = line[0]
		type = line[2]
		list = []
		list.append(time)#cost time
		list.append(line[1])#current time
		if type == 'sched_switch':
			list.append('task')
			list.append(line[3])#name
			list.append(line[4])#pid
		elif type == 'irq_handler_exit':
			list.append('irq')
			list.append(line[3])#irq
		elif type == 'softirq_exit':
			list.append('softirq')
			list.append(line[3])#vec
			list.append(line[4])#name
		self.__store_kv(kv, list, cpu)

	def __parser_filter(self, line):
		if line[2] == 'sched_wakeup':
			return False
		if line[2] == 'sched_migrate_task':
			return False
		if line[2] == 'sched_wakeup_new':
			return False
		if line[2] == 'softirq_raise':
			return False
		return True

	def get_task(self):
		return self.cpu_trace_task

	def parser_task(self, full):
		cpu = len(full)
		for cpu_id in range(0, cpu):
			stack = []
			begain = 0
			for line in full[cpu_id]:
				if self.__parser_filter(line) == False:
					continue
				if begain == 0:
					if line[2] == 'sched_switch':
						begain = 1
					else:
						continue
				self.__parser_time(cpu_id, line, self.cpu_trace_task, stack)
