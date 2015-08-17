# -*- coding: utf-8 -*-



# bubble_sort
def short_bubble_sort(a_list):
    length = len(a_list)

    for stop_num in xrange(length-1, 0, -1):
        sorted = True
        for i in xrange(stop_num):
            sorted = False
            if a_list[i] > a_list[i+1]:
                a_list[i], a_list[i+1] = a_list[i+1], a_list[i]
        if sorted:
            break

def bubble_sort(a_list):
    length = len(a_list)
    for stop_num in xrange(length, 0, -1):
        for i in xrange(stop_num-1):
            if a_list[i] > a_list[i+1]:
                a_list[i], a_list[i+1] = a_list[i+1], a_list[i]



# You may find it that selection sort makes
# the same number of comparisons as the bubble sort and is therefore alse O(n2). 
# But, due to the reduction in the number of exchanges, the selection sort typically executes faster in benchmark studies.


# selection sort
def selection_sort(a_list=None):
    length = len(a_list)
    for second_loop in xrange(length, 0, -1):
        max_position = 0
        for i in xrange(1, second_loop):
            if a_list[i] > a_list[max_position]:
                max_position = i
        a_list[second_loop-1], a_list[max_position] = a_list[max_position], a_list[second_loop-1]


# insertion sort

def insertion_sort(a_list):
    length = len(a_list)
    for index in xrange(1, length):
        current_value = a_list[index]
        insert_position = index
        while insert_position > 0 and a_list[insert_position-1] > current_value:
            a_list[insert_position] = a_list[insert_position-1]
            insert_position -= 1
        a_list[insert_position] = current_value


# shell sort 
def shell_sort(a_list):
    length = len(a_list)
    sublist_count = length // 2
    while sublist_count > 0:
        for start_position in xrange(sublist_count):
            insertion_gap_sort(a_list, length, start_position, sublist_count)
        sublist_count = sublist_count // 2
            
def insertion_gap_sort(a_list, lst_length, start_position, gap):
    for i in xrange(1, lst_length, gap):
        current_value = a_list[i]
        insert_position = i
        while insert_position > 0 and a_list[insert_position-1] > current_value:
            a_list[insert_position] = a_list[insert_position-1]
            insert_position -= 1
        a_list[insert_position] = current_value