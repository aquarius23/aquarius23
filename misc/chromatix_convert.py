#!/usr/bin/python
#!coding=utf-8
import os

chromatix_old_name = 'ov4688'
chromatix_new_name = 'ov4688_primax'

def walk_path(path):
    childs = os.listdir(path)
    for child in childs:
        file = os.path.join(path, child)
        if os.path.isdir(file):
            walk_path(file)
        else:
            if cmp(file[-2:], 'py') != 0:
                name = file.replace(chromatix_old_name, chromatix_new_name)
                os.rename(file, name)
                replace_file(name)

def write_file(file, value):
    f = open(file, 'wb')
    f.write(value)
    f.flush()
    f.close()

def read_file(file):
    f = open(file, 'rb')
    if f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(0)
        value = f.read(size)
        return value

def replace_file(file):
    old_u = chromatix_old_name.upper()
    new_u = chromatix_new_name.upper()
    value = read_file(file)
    value = value.replace(chromatix_old_name, chromatix_new_name)
    value = value.replace(old_u, new_u)
    write_file(file, value)

walk_path('.')
