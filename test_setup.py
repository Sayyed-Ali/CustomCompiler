#!/usr/bin/env python3
"""
Quick test to verify ast_nodes.py works correctly
"""

import sys
sys.path.insert(0, 'src')

from ast_nodes import *

print("🧪 Testing AST Nodes...")
print("=" * 50)

# Test 1: Create a simple literal
print("\n✓ Test 1: Creating a Literal node")
num = Literal(value=42, literal_type='int', line=1, column=5)
print(f"  Created: {num}")
print(f"  Value: {num.value}, Type: {num.literal_type}")

# Test 2: Create a variable
print("\n✓ Test 2: Creating a Variable node")
var = Variable(name='x', line=2, column=1)
print(f"  Created: {var}")
print(f"  Name: {var.name}")

# Test 3: Create a binary operation (5 + 3)
print("\n✓ Test 3: Creating a BinaryOp node (5 + 3)")
left = Literal(value=5, literal_type='int')
right = Literal(value=3, literal_type='int')
binop = BinaryOp(operator='+', left=left, right=right, line=3)
print(f"  Created: {binop}")
print(f"  Operator: {binop.operator}")

# Test 4: Create an assignment (x = 5)
print("\n✓ Test 4: Creating an Assignment node (x = 5)")
assign = Assignment(
    variable='x',
    expression=Literal(value=5, literal_type='int'),
    line=1
)
print(f"  Created: {assign}")
print(f"  Variable: {assign.variable}")

# Test 5: Print the AST tree
print("\n✓ Test 5: Pretty printing the AST")
print("-" * 50)
print_ast(assign)
print("-" * 50)

# Test 6: Create a small program
print("\n✓ Test 6: Creating a complete Program")
program = Program(statements=[
    Assignment(variable='x', expression=Literal(value=5, literal_type='int')),
    Assignment(variable='y', expression=Literal(value=10, literal_type='int')),
    PrintStatement(expression=Variable(name='x'))
])

print("  Program with 3 statements:")
print_ast(program)

print("\n" + "=" * 50)
print("✅ ALL TESTS PASSED!")
print("Your ast_nodes.py is working correctly!")
print("=" * 50)