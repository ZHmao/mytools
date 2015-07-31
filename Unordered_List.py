
class Node:
    def __init__(self, init_data):
        self.data = init_data
        self.next = None
        
    def set_data(self, new_data):
        self.data = new_data
    
    def get_data(self):
        return self.data
    
    def set_next(self, next_node):
        self.next = next_node
        
    def get_next(self):
        return self.next
    

class UnorderedList:
    def __init__(self):
        self.head = None
        self.count = 0
        
    def is_empty(self):
        if self.head == None:
            return True
        else:
            return False
        
    def size(self):
        return self.count
        
    def add(self, new_item):
        new_node = Node(new_item)
        new_node.set_next(self.head)
        self.head = new_node
        self.count += 1
    
    def append(self, new_item):
        new_node = Node(new_item)
        if self.head is None:
            self.head = new_node
        else:
            current == self.head
            while current.get_next() is not None:
                current = current.get_next()
            current.set_next(new_node)
        self.count += 1
        
    def insert(pos, new_item):
        new_node = Node(new_item)
        if pos == 0:
            new_node.set_next(self.head.get_next())
            self.head = new_node
        current = self.head
        for i in xrange(1, pos+1):
            previous = current
            current = current.get_next()
        new_node.set_next(current)
        previous.set_next(new_node)
        self.count += 1
        
    def remove(item):
        current = self.head
        previous = None
        while current.get_date != item:
            previous = current
            current = current.get_next()
        previous.set_next(current.get_next())
        current = None
        self.count -= 1
        
    def pop():
        current = self.head
        while current.get_next() is not None:
            current = current.get_next()
        item = current.get_data()
        current = None
        self.count -= 1
        return item
    
    def pop(pos):
        current = self.head
        if pos == 0:
            self.head = current.get_next()
            item = current.get_data()
            current = None
            return item
        for i in xrange(1, pos+1):
            previous = current
            current = current.get_next()
        item = current.get_data()
        previous.set_next(current.get_next)
        current = None
        self.count -= 1
        return item
    
    def index(item):
        current = self.head
        pos = 0
        while current.get_data() != item:
            current = current.get_next()
            pos += 1
        return pos