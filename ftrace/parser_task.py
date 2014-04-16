#!/usr/bin/python
#!coding=utf-8
import os
import sys
import string

class ftrace_task():
	cpu_trace_task = {}

	def __parser_task(self, line):
		if line[2] == 'sched_wakeup':
			return
		if line[2] == 'sched_migrate_task':
			return
		if line[2] == 'sched_wakeup_new':
			return
		if line[2] == 'softirq_raise':
			return

		cpu_id = line[0]
		if self.cpu_trace_task.has_key(cpu_id) == False:
			self.cpu_trace_task[cpu_id] = []
		self.cpu_trace_task[cpu_id].append(line)

	def get_task(self):
		return self.cpu_trace_task

	def parser_task(self, full):
		cpu = len(full)
		for cpu_id in range(0, cpu):
			for line in full[cpu_id]:
				self.__parser_task(line)
