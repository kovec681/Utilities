#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  batch_rename.py
#  
#  Copyright 2021 Seth Borkovec
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os

def main(args):
	'''
	Purpose:
	To rename a batch of files in the same directory that have
	the same naming scheme.
	
	Usage:
	python3 batch_rename.py . file new-file
	
	Example:
	./file_1.txt -> ./new-file_1.txt
	'''
	
	if (len(args) == 1 and args[1] == 'help') or (len(args) != 4):
		print('USAGE: file_rename [directory] ' + \
			'[part of name to replace] [replace with]')
			
	else:
		dir = args[1]
		
		if os.path.isdir(dir):
			old_chars = args[2]
			new_chars = args[3]
			files = os.listdir(dir)
			dir += '/'
			
			count = 1
			total_files = len(files)
			
			print('\nWorking in directory ' + dir)
			for file in files:
				old_name = str(file)
				new_name = old_name.replace(old_chars, new_chars)
				print('Renaming file ' + str(count) + '/' + \
					str(total_files) + ':\t' + old_name + '\t-> ' + new_name + \
					'.')
				os.rename(os.path.join(dir + old_name), os.path.join(dir + \
					new_name))
				count += 1
				
			print('Finished.')
			
		else:
			print(dir + ' is not a valid directory.')
		
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
