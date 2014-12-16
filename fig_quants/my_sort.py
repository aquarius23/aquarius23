#!/usr/bin/python
#!coding=utf-8
import stocksort
import stockdb
db = stockdb.stockdb()
list = stocksort.get_vol()
db.write_data_crf('vol_sort', list)
