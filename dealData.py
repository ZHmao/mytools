# coding: utf-8

__author__ = 'mzh'
# @since 2014-12-6

from xlrd.sheet import Sheet
import xlrd
import re


def get_excel_map(filename):
    book = xlrd.open_workbook(filename)
    allSheets = book.sheets()
    nameToSheetMap = {}
    for singleSheet in allSheets:
        #过滤隐藏的sheet
        if singleSheet.visibility != 0:
            continue
        sheet_data = get_sheet_data(singleSheet)
        strname = singleSheet.name
        strname = strname.encode('utf-8')
        nameToSheetMap[strname] = sheet_data

    return nameToSheetMap

##
#           ***********************
#           * 姓名 * 性别 * 年龄 * *
#           *  毛  *  男  * 12  * *
#           *  李  *  女  * 13  * *
#           ***********************
# 如上这样的sheet，返回的列表是：[{'姓名':'毛', '性别':'男', '年龄':'12'}, {'姓名':'李', '性别':'女', '年龄':'13'}]
def get_sheet_data(sheet):
        sheet_rows = sheet.nrows
        sheet_cols = sheet.ncols

        # 获取列名
        col_names = []
        for index in range(0, sheet_cols):
            col_names.append(sheet.cell_value(0, index))

        # 根据查出的所有列名，设置实际有用的列数
        actual_cols = len(col_names)
        # 获取所有行
        all_row_data = []
        for i in range(1, sheet_rows):
            row_map = {}
            for j in range(0, actual_cols):
                row_map[col_names[j]] = sheet.cell_value(i, j)
            all_row_data.append(row_map)
        return all_row_data

#根据给定的类SQL语句在sheet中进行查询
def query_sheet_data(sqlMap={}, sheetList=None):
    selectField = sqlMap['select']
    countField = sqlMap['count']
    sumField = sqlMap['sum']
    groupbyField = sqlMap['groupby']
    whereSql = sqlMap['where']
    keyToValueMap = {}
    
    if sheetList is not None:
        tempsheetList = []
        
        #过滤不满足条件的数据
        if whereSql is not None:
            wherePattern = re.compile('(?P<key>.*)(?P<sign>[=!]{1,2})(?P<value>.*)')
            whereMatch = wherePattern.match(whereSql)
            matchMap = whereMatch.groups()
            tempSymbol = matchMap['sign']
            if tempSymbol is '=':
                for datamap in sheetList:
                    whereValue = datamap[matchMap['key']]
                    if whereValue is matchMap['value']:
                        tempsheetList.append(datamap)
            elif tempSymbol is '!=':
                for datamap in sheetList:
                    whereValue = datamap[matchMap['key']]
                    if whereValue is matchMap['value']:
                        tempsheetList.append(datamap)
        
        #只留select的字段
        sheetList = tempsheetList
        tempsheetList = []                
        for datamap in sheetList:
            tempmap = {}
            for sel in selectField:
                tempmap[sel] = datamap[sel]
            tempsheetList.append(tempmap)
        
        sheetList = tempsheetList
        
        
#组装根据条件查询出的数据             
def constructReturnData(sheetList=None, groupby=None):
    keyIndex = []
    tempmap = {}
    for datamap in sheetList:
            satisfyFlag = False
            for single in groupby:
                pass

if __name__ == '__main__':
    ret_map = get_excel_map(r'123.xls')


