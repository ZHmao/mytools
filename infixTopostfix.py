# -*- coding: utf-8 -*-

# convert infix expression to postfix expression
class Stack:
    def __init__(self):
        self.items = []
        
    def is_empty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
    
    # get the top value of stack, but not remove it.
    def peek(self):
        return self.items[len(self.items)-1]
    
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        return self.items.pop()
    

def infix_to_postfix(expr):
    # precedence
    prec = {'*': 5, '/': 5, '+': 3, '-': 3, '(': 2}
    
    output = []
    op_stack = Stack()
    expr_list = expr.split(' ')
    for char in expr_list:
        if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            output.append(char)
        elif char == '(':
            op_stack.push(char)
        elif char == ')':
            while op_stack.peek() != '(':
                output.append(op_stack.pop())
            op_stack.pop()
        else:
            while (not op_stack.is_empty()) and (prec[op_stack.peek()] > prec[char]):
                output.append(op_stack.pop())
            op_stack.push(char)
    while not op_stack.is_empty():
        output.append(op_stack.pop())
    
    return ''.join(output)

print(infix_to_postfix('A * B + C * D'))
print(infix_to_postfix('( A + B ) * ( C + D )'))