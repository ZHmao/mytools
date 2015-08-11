# -*- coding: utf-8 -*-

# ##使用Hash模拟一个简单的map
# 
# key仅仅能使用数值，并且假设put时，slots里面要么已经存在了改key，要么有多余空间




class MyMap:
    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size
        self.data = [None] * self.size
        
    def hash_func(self, key, size):
        return key % size
    
    def rehash(self, key, size):
        return (key+1) % size
    
    def put(self, key, value):
        hash_value = self.hash_func(key, self.size)
        
        if self.slots[hash_value] == None:
            self.slots[hash_value] = key
            self.data[hash_value] = value
        else:
            hash_value = self.rehash(hash_value, self.size)
            while self.slots[hash_value] != None and self.slots[hash_value] != key:
                hash_value = self.rehash(hash_value, self.size)
                
            if self.slots[hash_value] == None:
                self.slots[hash_value] = key
                self.data[hash_value] = value
            else:
                self.data[hash_value] = value
                
    def get(self, key):
        start = self.hash_func(key, self.size)
        found = False
        stop = False
        data = None
        
        current = start
        # self.slots[current] != None，如果发现为空，那这个key肯定没有存入
        while self.slots[current] != None and not found and not stop:
            if self.slots[current] == key:
                found = True
                data = self.data[current]
            else:
                current = self.rehash(current, self.size)
                if current == start:
                    stop = True
        return data
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.put(key, value)