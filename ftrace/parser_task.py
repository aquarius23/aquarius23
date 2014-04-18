#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string

class ftrace_task():
	cpu_trace_task = {}
	cpu_trace_time = {}
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
		if cpu_id == 0:
			type = line[2]
			if type == 'sched_switch':
				if len(stack) > 0:
					time = self.__calculate_pop(stack, line)
					print 'sched time: ' + str(time)
				self.__stack_push(stack, line)
				self.__stack_push(stack, '-')
			elif type == 'irq_handler_entry':
				self.__stack_push(stack, line)
				self.__stack_push(stack, '-')
			elif type == 'irq_handler_exit':
				time = self.__calculate_pop(stack, line)
				self.__stack_push(stack, time)
				print 'irq time ' + str(time)
			elif type == 'softirq_entry':
				self.__stack_push(stack, line)
				self.__stack_push(stack, '-')
			elif type == 'softirq_exit':
				time = self.__calculate_pop(stack, line)
				self.__stack_push(stack, time)
				print 'softirq time ' + str(time)

	def __store_kv(self, kv, line):
		cpu_id = line[0]
		if kv.has_key(cpu_id) == False:
			kv[cpu_id] = []
		kv[cpu_id].append(line)

	def __pop_kv(self, kv, cpu_id):
		return kv[cpu_id].pop()

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
				#self.__store_log(self.cpu_trace_task, line)
				self.__parser_time(cpu_id, line, self.cpu_trace_time, stack)
