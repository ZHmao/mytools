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
	where_sql = where_sql[:-1] + ")"
	return where_sql


def get_sql_head(table_name):
	return 'select * from ' + table_name

# type of bill_type_code must be the list
def get_billtemplet_data(bill_type_code=None):
	pass

#
def gen_sql(tables, key, pks):
	sql_condition = get_where_condition(key, pks)
	for table_name in tables:
		sql_head = get_sql_head(table_name)
		yield sql_head + sql_condition
		


def get_value_sql_from_origin(result_data):
	text = "("
	for value in result:
		value_type = type(value)
		if value_type == str:
			text = text + "'" + value + "'" + ","
		elif value_type == int or value == float:
			text = text + str(value) + ","
		elif value == None:
			text = text + "null" + ","
		else:
			pass
	text = text[:-1] + ")"
	return text

# 默认tables[0]是主表，keys[0]是主表关键字
def get_templet_data(cur, tables, keys, codes):
	text = ""
	if tables is not None and key is not None and keys is not None:
		'''根据单据类型编码查出主模板'''
		main_sql = get_sql_head(tables[0])
		main_sql += get_where_condition(keys[0], codes)
		cur.execute(main_sql)
		pks = []
		results = cur.fetchall()
		if results is not None:
			pk_index = cur.description.index(keys[1])
			all_keys = [column+"," for column in cur.description]
			first_part = "insert into " + tables[0] + " (" + all_keys[:-1] + ") values "
			for sr in results:
				pks.append(sr[pk_index])
				text = text + "\n" + first_part + get_value_sql_from_origin(sr) + ";"
		else:
			return None
		'''根据主模板中的pk，去子模板中查'''
		# sql_list = gen_sql(tables[1:], keys[1], pks)
		sql_condition = get_where_condition(keys[1], pks)
		for table_name in tables[1:]:
			exec_sql = get_sql_head(table_name) + sql_condition
			cur.execute()
			results = cur.fetchall()
			if results is not None:
				all_keys = [column+"," for column in cur.description]
				first_part = "insert into " + table_name + " (" + all_keys[:-1] + ") values "
				for sr in results:
					pks.append(sr[pk_index])
					text = text + "\n" + first_part + get_value_sql_from_origin(sr) + ";"
				else:
					pass
			else:
				return None
	return text

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