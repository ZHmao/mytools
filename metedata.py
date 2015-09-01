# -*- coding: utf-8 -*-

import os 
import cx_Oracle as oracle

# 这里的字符集要保持与Oracle数据库所使用的一致，否则乱码。
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'


#
def get_where_condition(key, pk_list):
	where_sql = " where " + key + " in ("
	for pk in pk_list:
		where_sql = where_sql + "'" + pk + "',"
	where_sql = where_sql[:-1]
	where_sql += ")"
	return where_sql


def get_sql_head(table_name):
	return 'select * from ' + table_name

# type of bill_type_code must be the list
def get_billtemplet_data(bill_type_code=None):
	pass

#
def gen_sql(tables, pks):
	for table_name in tables:
		sql_head = get_sql_head(table_name)

# 默认tables[0]是主表，keys[0]是主表关键字
def get_templet_data(cur, tables, keys, codes):
	ret_text = ''
	if tables is not None and key is not None and keys is not None:
		main_sql = get_sql_head(tables[0])
		main_sql += get_where_condition(keys[0], codes)
		cur.execute(main_sql)
		results = cur.fetchall()
		if results is not None:
			
		else:
			return None

	else:
		return None

def get_mete_data():
	pass

def main():
	dsn = oracle.makedsn('ip', 'port', 'orcl')
	conn = oracle.connect('username', 'password', dsn)
	cur = conn.cursor()
	sql = ""
	cur.execute(sql)
	result = cur.fetchone()
	print result
	text = ""
	for value in result:
		value_type = type(value)
		if value_type == str:
			text = text + "'" + value + "'" + ","
		elif value_type == int or value == float:
			text = text + str(value) + ","
		elif value == None:
			text = text + "null" + ","
		else:
			print '[' + str(value_type) + ']: This type is out of my expected!'
	with open('test.sql', 'w') as fw:
		fw.write(text)

if __name__ == '__main__':
	main()