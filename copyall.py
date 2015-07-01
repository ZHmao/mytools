# -*- coding: utf-8 -*-

import os
import codecs
import re
import logging

BASE_DIR = os.path.join(os.path.dirname(__file__), '/ALLFILE/').replace('\\', '/')

'''
support utf-8 only
mzh
2015-6-19
'''
def main():
	logger = logging.getLogger('main')
	logger.info('================================begin================================')

	my_counter = 0
	final_text = u''
	file_name_list = []
	for file_name in os.listdir(BASE_DIR):
		if os.path.isdir(BASE_DIR+file_name):
			logger.info(file_name+' is a directory')
			continue
		file_name_list.append(file_name)

	for file_name in file_name_list:
		logger.info('-----')

		if not os.path.isfile(BASE_DIR+file_name):
			logger.info(file_name+' not exist')
			continue
		
		my_counter += 1
		logger.info(my_counter)
		logger.info(file_name)

		text = ''
		with open(BASE_DIR+file_name, 'r') as fr:
			text = fr.read()
			if text.startswith(codecs.BOM_UTF8):
				#special text may be contains BOM
				#more detail in SO:reading-unicode-file-data-with-bom-chars-in-python
				text = text.decode('utf-8-sig')
			else:
				text = text.decode('utf-8')
		final_text += text
	
	with open('final.sql', 'w') as fw:
		final_text = final_text.encode('utf-8-sig')
		fw.write(final_text)

if __name__ == '__main__':
	logging.basicConfig(filename='log.txt', level=logging.INFO)
	main()
