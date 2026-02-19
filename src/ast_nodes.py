"""
AST Node Definitions
Dedfines all nodes types for our abstract syntax tree
"""

from dataclasses import dataclass, field
from typing import Optional, List, Any

@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int = 0
    column: int  = 0

@dataclass
class Program(ASTNode):
    """Root node - containsn list of statements"""
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class Assignment(ASTNode):
    """Cariable assigemnt: x=expression"""
    variable: str = ""
    expression: Optional[ASTNode] = None

@dataclass
class BinaryOp(ASTNode):
    """Binary operation: left op right"""
    operator: str = ""
    left: Optional[ASTNode] = None
    right: Optional[ASTNode] = None

@dataclass
class UnaryOp(ASTNode):
    """Unary operations: op operand"""
    operator: str = ""
    operand: Optional[ASTNode] = None

@dataclass
class Literal(ASTNode):
    """literal value: 5, 3.14, "hello", true"""
    value: Any = None
    literal_type: str = ""      # 'int', 'float', 'string', 'bool'

@dataclass
class Variable(ASTNode):
    """Variable references: x"""
    name: str = ""

@dataclass
class IfStatement(ASTNode):
    """"If-else statement"""
    condition: Optional[ASTNode] = None
    then_block: List[ASTNode] = field(default_factory=list)
    else_block: Optional[List[ASTNode]] = None

@dataclass
class WhileStatement(ASTNode):
    """while loop"""
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class PrintStatement(ASTNode):
    """print statement"""
    expression: Optional[ASTNode] = None


def print_ast(node: ASTNode, indent: int=0)->None:
    """print ast for debigginh"""

    prefix=" "*indent
    
    if isinstance(node, Program):
        print(f'{prefix}Program:')
        for stmt in node.statements:
            print_ast(stmt, indent+1)
    
    elif isinstance(node, Assignment):
        print(f'{prefix}Assignemnt: {node.variable}=')
        print_ast(node.expression, indent+1)

    elif isinstance(node, BinaryOp):
        print(f'{prefix}BinaryOp: {node.operator}')
        print_ast(node.left, indent+1)
        print_ast(node.right, indent+1)

    elif isinstance(node, UnaryOp):
        print(f'{prefix}UnaryOp: {node.operator}')
        print_ast(node.operand, indent+1)

    elif isinstance(node, Literal):
        print(f'{prefix}Literal: {node.value} ({node.literal_type})')

    elif isinstance(node, Variable):
        print(f"{prefix}Variable: {node.name}")

    elif isinstance(node, IfStatement):
        print(f'{prefix}If:')
        print(f'{prefix}Condition:')
        print_ast(node.condition, indent+2)
        print(f'{prefix}then:')
        for stmt in node.then_block:
            print_ast(stmt, indent+2)
        if node.else_block:
            print(f'{prefix} else:')
            for stmt in node.else_block:
                print_ast(stmt, indent+2)
    
    elif isinstance(node, WhileStatement):
        print(f'{prefix}While:')
        print(f'{prefix}Condition:')
        print_ast(node.condition, indent+2)
        print(f'{prefix}Body:')
        for stmt in node.body:
            print_ast(stmt, indent+2)
        
    elif isinstance(node, PrintStatement):
        print(f'{prefix}print:')
        print_ast(node.expression, indent+1)
    


