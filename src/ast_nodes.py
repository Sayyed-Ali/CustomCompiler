"""
AST Node Definitions
"""

from typing import Optional, List, Any


class ASTNode:
    """Base class for all AST nodes"""
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column


class Program(ASTNode):
    """Root node - contains list of statements"""
    def __init__(self, statements=None, line=0, column=0):
        super().__init__(line, column)
        self.statements = statements if statements is not None else []


class Assignment(ASTNode):
    """Variable assignment"""
    def __init__(self, variable="", expression=None, line=0, column=0):
        super().__init__(line, column)
        self.variable = variable
        self.expression = expression


class BinaryOp(ASTNode):
    """Binary operation"""
    def __init__(self, operator="", left=None, right=None, line=0, column=0):
        super().__init__(line, column)
        self.operator = operator
        self.left = left
        self.right = right


class UnaryOp(ASTNode):
    """Unary operation"""
    def __init__(self, operator="", operand=None, line=0, column=0):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand


class Literal(ASTNode):
    """Literal value"""
    def __init__(self, value=None, literal_type="", line=0, column=0):
        super().__init__(line, column)
        self.value = value
        self.literal_type = literal_type


class Variable(ASTNode):
    """Variable reference"""
    def __init__(self, name="", line=0, column=0):
        super().__init__(line, column)
        self.name = name


class IfStatement(ASTNode):
    """If-else statement"""
    def __init__(self, condition=None, then_block=None, else_block=None, line=0, column=0):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block if then_block is not None else []
        self.else_block = else_block


class WhileStatement(ASTNode):
    """While loop"""
    def __init__(self, condition=None, body=None, line=0, column=0):
        super().__init__(line, column)
        self.condition = condition
        self.body = body if body is not None else []


class PrintStatement(ASTNode):
    """Print statement"""
    def __init__(self, expression=None, line=0, column=0):
        super().__init__(line, column)
        self.expression = expression


def print_ast(node, indent=0):
    """Print AST for debugging"""
    prefix = " " * indent
    
    if isinstance(node, Program):
        print(f'{prefix}Program:')
        for stmt in node.statements:
            print_ast(stmt, indent + 2)
    
    elif isinstance(node, Assignment):
        print(f'{prefix}Assignment: {node.variable} =')
        if node.expression:
            print_ast(node.expression, indent + 2)
    
    elif isinstance(node, BinaryOp):
        print(f'{prefix}BinaryOp: {node.operator}')
        if node.left:
            print_ast(node.left, indent + 2)
        if node.right:
            print_ast(node.right, indent + 2)
    
    elif isinstance(node, UnaryOp):
        print(f'{prefix}UnaryOp: {node.operator}')
        if node.operand:
            print_ast(node.operand, indent + 2)
    
    elif isinstance(node, Literal):
        print(f'{prefix}Literal: {node.value} ({node.literal_type})')
    
    elif isinstance(node, Variable):
        print(f'{prefix}Variable: {node.name}')
    
    elif isinstance(node, IfStatement):
        print(f'{prefix}If:')
        if node.condition:
            print(f'{prefix}  Condition:')
            print_ast(node.condition, indent + 4)
        if node.then_block:
            print(f'{prefix}  Then:')
            for stmt in node.then_block:
                print_ast(stmt, indent + 4)
        if node.else_block:
            print(f'{prefix}  Else:')
            for stmt in node.else_block:
                print_ast(stmt, indent + 4)
    
    elif isinstance(node, WhileStatement):
        print(f'{prefix}While:')
        if node.condition:
            print(f'{prefix}  Condition:')
            print_ast(node.condition, indent + 4)
        if node.body:
            print(f'{prefix}  Body:')
            for stmt in node.body:
                print_ast(stmt, indent + 4)
    
    elif isinstance(node, PrintStatement):
        print(f'{prefix}Print:')
        if node.expression:
            print_ast(node.expression, indent + 2)
    
    else:
        print(f'{prefix}{node.__class__.__name__}')