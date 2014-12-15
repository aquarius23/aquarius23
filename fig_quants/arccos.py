#!/usr/bin/python
#!coding=utf-8
import math

def vec_acos(v1, v2):
	if len(v1) != len(v2):
		return 0
	ab = 0.0
	aa = 0.0
	bb = 0.0
	for i, a in enumerate(v1):
		b = v2[i]
		ab = ab + a*b
		aa = aa + a*a
		bb = bb + b*b
	val = ab / (math.sqrt(aa)*math.sqrt(bb))
	val = math.acos(val)
	deg = math.degrees(val)
	return deg
