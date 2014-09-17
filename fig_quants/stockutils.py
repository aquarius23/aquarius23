#!/usr/bin/python
#!coding=utf-8
import time
import string

def get_date():
	return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def get_time():
	return time.strftime('%T',time.localtime(time.time()))

def next_jidu(year, jidu):
	if jidu >= 4:
		year = year + 1
		jidu = 0
	return year, jidu + 1
