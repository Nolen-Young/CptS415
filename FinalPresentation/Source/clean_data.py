# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 17:58:11 2019

@author: Nathan
"""
import os
import re

os.chdir('C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Data\\UpdateCrawl')

lines_to_add = []
for root, dirs, files in os.walk('.\\', topdown=True):
    for fname in files:
        if re.match('\d.txt', fname):
            next_dest = os.path.join(root,fname)
            with open(next_dest) as file:
                print(next_dest)
                lines = file.readlines()
                line = lines[0]
                tab_count = line.count('\t')
                if tab_count < 28:
                    print('\tEditing...')
                    line = line[:-1]+('\t'*(28-tab_count)+'\n')
                    lines[0] = line
                lines_to_add = lines
                    
            with open(next_dest, 'w') as file:
                file.writelines(lines_to_add)