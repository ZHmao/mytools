# -*- coding: utf-8 -*-

import os 
import cx_Oracle as oracle

# 这里的字符集要保持与Oracle数据库所使用的一致，否则乱码。
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'

###########################################################

# 单据模板表名
BILL_TEMPLET_TABLE_NAME = [
    'pub_billtemplet',
    'pub_billtemplet_b',
    'pub_billtemplet_t',
]

# 查询模板表名
QUERY_TEMPLET_TABLE_NAME = [
    'pub_query_templet',
    'pub_query_condition',
]

METEDATA_SQL = (
    # [1]
    ("select * from md_component where name in {codes}", "md_component"),

    # [2]
    ("select * from md_class where componentid in "
     "(select id from md_component where name in {codes})", "md_class"),

    # [3]
    ("select * from md_table where id in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes}))", "md_table"),

    # [4]
    ("select * from md_accessorpara where id in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes}))", "md_accessorpara"),

    # [5]
    ("select * from md_db_relation where endtableid in "
     "(select id from md_table where id in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes})))", "md_db_relation"),

    # [6]
    ("select * from md_association where componentid in "
     "(select id from md_component where name in {codes})", "md_association"),

    # [7]
    ("select * from md_column where tableid in "
     "(select id from md_table where id in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes})))", "md_column"),

    # [8]
    ("select * from md_property where classid in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes}))", "md_property"),

    # [9]
    ("select * from md_ormap where classid in "
     "(select id from md_table where id in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes})))", "md_ormap"),

    # [10]
    ("select * from md_enumValue where id in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes}))", "md_enumValue"),

    # [11]
    ("select * from md_bizItfMap where classid in "
     "(select id from md_class where componentid in "
     "(select id from md_component where name in {codes}))", "md_bizItfMap"),

    # [12]
    ("select * from mde_componentinfo where componentcode in {codes}", "mde_componentinfo"),

)

###########################################################

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
    for value in result_data:
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
    if tables is not None and keys is not None:
        """根据单据类型编码查出主模板"""
        main_sql = get_sql_head(tables[0])
        main_sql += get_where_condition(keys[0], codes)
        cur.execute(main_sql)
        pks = []
        results = cur.fetchall()
        if results:
            # modify 2015-9-10 查询主表pk名称叫 'ID'
            pk_index = -1
            column_desc = cur.description
            for index, cd in enumerate(column_desc):
                if cd[0] == 'ID':
                    pk_index = index
                    break
            if pk_index == -1:
                return
            all_keys = [column[0]+"," for column in column_desc]
            first_part = "insert into " + tables[0] + " (" + "".join(all_keys)[:-1] + ") values "
            for sr in results:
                pks.append(sr[pk_index])
                text = text + "\n" + first_part + get_value_sql_from_origin(sr) + ";"
        else:
            return None
        """根据主模板中的pk，去子模板中查"""
        # sql_list = gen_sql(tables[1:], keys[1], pks)
        sql_condition = get_where_condition(keys[1], pks)
        for table_name in tables[1:]:
            exec_sql = get_sql_head(table_name) + sql_condition
            cur.execute(exec_sql)
            results = cur.fetchall()
            if results is not None:
                all_keys = [column[0]+"," for column in cur.description]
                first_part = "insert into " + table_name + " (" + "".join(all_keys)[:-1] + ") values "
                for sr in results:
                    text = text + "\n" + first_part + get_value_sql_from_origin(sr) + ";"
                else:
                    pass
            else:
                return None
    return text

def get_query_templet(cur, codes):
    keys = ['node_code', 'pk_templet']
    text = get_templet_data(cur, QUERY_TEMPLET_TABLE_NAME, keys, codes)
    return text

def get_bill_templet(cur, codes):
    keys = ['pk_billtypecode', 'pk_billtemplet']
    text = get_templet_data(cur, BILL_TEMPLET_TABLE_NAME, keys, codes)
    return text

def get_mete_data(cur, codes):
    text = ""
    for exec_sql, table_name in METEDATA_SQL:
        exec_sql = exec_sql.format(codes=codes)
        cur.execute(exec_sql)
        results = cur.fetchall()
        if results is not None:
            all_keys = [column+"," for column in cur.description]
            head_part = "insert into " + table_name + " (" + all_keys[:-1] + ") values "
            for sr in results:
                text = text + "\n" + head_part + get_value_sql_from_origin(sr) + ";"
    return text

def main():
    dsn = oracle.makedsn('', '', '')
    conn = oracle.connect('', '', dsn)
    cur = conn.cursor()
    text = get_query_templet(cur, ['DYH10106','DYH30101'])
    with open('test.sql', 'w') as fw:
        fw.write(text)

if __name__ == '__main__':
    main()