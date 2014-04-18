#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string

class ftrace_task():
	time_slice = 0
	cpu_number = 0
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
		list.append(cpu)
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

	def select_time_slice(self, ms):
		self.time_slice = ms

	def __split_task(self):
		task_time = []
		time_range = []
		ms = self.time_slice
		if ms <= 0:
			ms = 1000*60*60
		start_time = self.cpu_trace_task[0][0][1]
		for cpu_id in range(0, self.cpu_number):
			start = start_time
			end = start + ms
			list = []
			count = 0
			for line in self.cpu_trace_task[cpu_id]:
				if line[1] <= end:
					list.append(line)
				else:
					slice_range = 'start: ' + str(start) + '   --->   end: ' + str(end)
					if cpu_id == 0:
						time_range.append(slice_range)
						task_time.append(list)
					else:
						task_time[count].extend(list)
					start = end
					end = start + ms
					list = []
					list.append(line)
					count = count + 1

			slice_range = 'start: ' + str(start) + '   --->   end: ' + str(end)
			if cpu_id == 0:
				time_range.append(slice_range)
				task_time.append(list)
			else:
				task_time[count].extend(list)
		return time_range, task_time

	def get_task(self):
		return self.cpu_trace_task

	def item_percent(self, id, type):
		time, cost = self.__split_task()
		list = []
		for slice in cost:
			sum = 0
			count = 0
			for line in slice:
				line_cost = line[0]
				line_type = line[3]
				line_id = line[4]
				sum = sum + line_cost
				if type == line_type:
					if id == line_id:
						count = count + line_cost
			percent = count * 100 / sum
			percent = 'all: ' + str(sum) + '  cost: ' + str(count) + '  percent:' + str(percent) + '%'
			list.append(percent)
		return time, list

	def __top(self):
		time, cost = self.__split_task()
		list = []
		for slice in cost:
			dic = {}
			temp = []
			for line in slice:
				line_cost = line[0]
				line_id = line[4]
				line_type = line[3]
				key = line_type + ':' + line_id
				if key in dic:
					dic[key] = dic[key] + line_cost
				else:
					dic[key] = line_cost
			for key in dic.keys():
				item = []
				item.append(key)
				item.append(dic[key])
				temp.append(item)
			temp.sort(cmp = lambda x,y: cmp(x[1],y[1]), reverse = True)
			list.append(temp)
		return time, list

	def top(self, num):
		time, cost = self.__top()
		list = []
		for slice in cost:
			count = num
			temp = []
			for item in slice:
				if count > 0:
					temp.append(item)
				count = count - 1;
			list.append(temp)
		return time, list

	def task_percent(self, name):
		type = 'task'
		return self.item_percent(name, type)

	def irq_percent(self, irq):
		type = 'irq'
		return self.item_percent(irq, type)

	def softirq_percent(self, vec):
		type = 'softirq'
		return self.item_percent(vec, type)

	def parser_task(self, full):
		cpu = len(full)
		self.cpu_number = cpu
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
