# -*- coding: utf-8 -*-

def sequential_search(a_list, item):
    pos = 0
    found = False
    length = len(a_list)
    
    while pos < length and not found:
        if a_list[pos] == item:
            found = True
            break
        pos += 1
        
    return found

print sequential_search([1,2,4], 3)


def binary_search(ordered_list, item):
    first = 0
    last = len(ordered_list)-1
    found = False
    
    while first <= last and not found:
        middle = (first + last) // 2
        if ordered_list[middle] == item:
            found = True
        else:
            if ordered_list[middle] > item:
                last = middle - 1
            else:
                first = middle + 1
                
    return found

print binary_search([], 5)


# 做 二分法 搜索时，要考虑给定的List，如果数据量较小，则不建议 使用。因为在对List进行排序时本身就比较耗时。
