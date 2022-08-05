# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:33:42 2021

@author: piy81
"""
import child

serial_number = ['A3CS0001', 'A3CS0002', 'A3CS0003', 'A3CS0004', 'A3CS0005', 'A3CS0006', 'A3CS0007', 'A3CS0008', 'A3CS0009', 'A3CS0010']

child_list = [child.Child(sn) for sn in serial_number]

for cl in child_list:
    cl.run()