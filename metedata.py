# -*- coding: utf-8 -*-

import os 
import cx_Oracle as oracle
import logging
import datetime

# 这里的字符集要保持与Oracle数据库所使用的一致，否则乱码。
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'

###########################################################

logger_instance = None

# 单据模板表名
BILL_TEMPLET_TABLE_NAME = (
    'pub_billtemplet',
    'pub_billtemplet_b',
    'pub_billtemplet_t',
)

# 查询模板表名
QUERY_TEMPLET_TABLE_NAME = (
    'pub_query_templet',
    'pub_query_condition',
)

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
    global logger_instance
    
    text = ""
    if tables is not None and keys is not None:
        """根据单据类型编码查出主模板"""
        main_sql = get_sql_head(tables[0])
        main_sql += get_where_condition(keys[0], codes)
        cur.execute(main_sql)
        pks = []
        results = cur.fetchall()
        if results:
            # modify 2015-9-11 查询主表pk名称叫 'ID'
            if tables[0] == 'pub_query_templet':
                pk_field = 'ID'
            else:
                pk_field = keys[1]
            pk_index = -1
            column_desc = cur.description
            for index, cd in enumerate(column_desc):
                if cd[0] == pk_field:
                    pk_index = index
                    break
            if pk_index == -1:
                return
            all_keys = [column[0]+"," for column in column_desc]
            first_part = "insert into " + tables[0] + " (" + "".join(all_keys)[:-1] + ") \n values "
            for sr in results:
                pks.append(sr[pk_index])
                text = text + "\n" + first_part + get_value_sql_from_origin(sr) + ";"
        else:
            logger_instance.info(u'该表[{}]中没有数据！'.format(tables[0]))
            return None
        """根据主模板中的pk，去子模板中查"""
        # sql_list = gen_sql(tables[1:], keys[1], pks)
        sql_condition = get_where_condition(keys[1], pks)
        for table_name in tables[1:]:
            exec_sql = get_sql_head(table_name) + sql_condition
            cur.execute(exec_sql)
            results = cur.fetchall()
            if results:
                all_keys = [column[0]+"," for column in cur.description]
                first_part = "insert into " + table_name + " (" + "".join(all_keys)[:-1] + ") \n values "
                for sr in results:
                    text = text + "\n" + first_part + get_value_sql_from_origin(sr) + ";"
            else:
                logger_instance.info(u'该表[{}]中没有数据！'.format(table_name))
                return None
    """清除原数据，先删除字表中的数据"""
    delete_text = ""
    tables.reverse()
    for table_name in tables:
        delete_text  = (delete_text + "delete from " + table_name
                        + " " + get_where_condition(keys[1], pks) + ";\n")
    text = delete_text + text
    return text

def get_query_templet(cur, codes):
    global logger_instance
    logger_instance.info(u'========查询模板========')
    
    keys = ['node_code', 'PK_TEMPLET']
    text = get_templet_data(cur, list(QUERY_TEMPLET_TABLE_NAME), keys, codes)
    if text:
        logger_instance.info(u'完成!')
    return text

def get_bill_templet(cur, codes):
    global logger_instance
    logger_instance.info(u'========单据模板========')
    
    keys = ['pk_billtypecode', 'PK_BILLTEMPLET']
    text = get_templet_data(cur, list(BILL_TEMPLET_TABLE_NAME), keys, codes)
    if text:
        logger_instance.info(u'完成!')
    return text

def get_mete_data(cur, pks):
    global logger_instance
    logger_instance.info(u'=========元数据========')
    
    text = ""
    pk_condition = "("
    for pk in pks:
        pk_condition = pk_condition + "'" + pk + "',"
    pk_condition = pk_condition[:-1] + ")"
    for exec_sql, table_name in METEDATA_SQL:
        exec_sql = exec_sql.format(codes=pk_condition)
        cur.execute(exec_sql)
        results = cur.fetchall()
        if results is not None:
            all_keys = [column[0]+"," for column in cur.description]
            head_part = "insert into " + table_name + " (" + "".join(all_keys)[:-1] + ") \n values "
            for sr in results:
                text = text + "\n" + head_part + get_value_sql_from_origin(sr) + ";"
            logger_instance.info(table_name)
        else:
            logger_instance.info('{} is empty!'.format(table_name))
    """清除原数据，先删除字表中的数据"""
    delete_text = ""
    all_sql = list(METEDATA_SQL)
    all_sql.reverse()
    for single in all_sql:
        single = list(single)
        single[0] = single[0].replace("select *", "delete")
        single[0] = single[0].format(codes=pk_condition)
        delete_text = delete_text + single[0] + ";\n"
    text = delete_text + text
    if text:
        logger_instance.info(u'完成!')
    return text

def main():
    global logger_instance
    logging.basicConfig(filename=os.path.join(os.getcwd(), 'metedatalog.txt'),
                        level=logging.INFO,
                        format='[%(lineno)s] - %(message)s')    
    logger_instance = logging.getLogger()
    logger_instance.setLevel(logging.INFO)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger_instance.info('=============================================')
    logger_instance.info('================Start========================')
    logger_instance.info('========={}================'.format(now))
    logger_instance.info('=============================================')
    
    data_src_ip = ''
    data_src_port = ''
    data_src_instance = ''
    usr_name = ''
    usr_password = ''
    dsn = oracle.makedsn(data_src_ip, data_src_port, data_src_instance)
    try:
        conn = oracle.connect(usr_name, usr_password, dsn)
        cur = conn.cursor()
    except oracle.DatabaseError, exc:
        error, = exc.args
        logger_instance.info(u'数据库连接出错')
        logger_instance.info('Oracle-Error-Code: {}'.format(error.code))
        logger_instance.info('Oracle-Error-Msg: {}'.format(error.message))
        return

    logger_instance.info(u'--数据库连接成功！')    
    
    query_templet_text = get_query_templet(cur, ['DYH20302'])
    bill_templet_text = get_bill_templet(cur, ['MC08'])
    mete_text = get_mete_data(cur, ['sampleflowcard'])
    with open('test.sql', 'w') as fw:
        fw.write(mete_text+bill_templet_text+query_templet_text)

    logger_instance.info('================ End ========================')

if __name__ == '__main__':
    main()