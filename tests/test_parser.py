"""
Tests for the Parser
Run with: python3 tests/test_parser.py
"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from parser import Parser
from ast_nodes import *


def test_simple_assignment():
    """Test: x = 5"""
    print("\n" + "="*60)
    print("TEST 1: Simple Assignment (x = 5)")
    print("="*60)
    
    code = "x = 5"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput: {code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    # Verify
    assert ast is not None, "AST should not be None"
    assert len(ast.statements) == 1, "Should have 1 statement"
    assert isinstance(ast.statements[0], Assignment), "Should be Assignment"
    assert ast.statements[0].variable == 'x', "Variable should be 'x'"
    assert isinstance(ast.statements[0].expression, Literal), "Expression should be Literal"
    assert ast.statements[0].expression.value == 5, "Value should be 5"
    
    print("\n✅ TEST 1 PASSED!")
    return True


def test_arithmetic_expression():
    """Test: z = x + y * 2"""
    print("\n" + "="*60)
    print("TEST 2: Arithmetic Expression (z = x + y * 2)")
    print("="*60)
    
    code = "z = x + y * 2"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput: {code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    # Verify structure: z = x + (y * 2)
    assert ast is not None
    assert len(ast.statements) == 1
    assign = ast.statements[0]
    assert isinstance(assign, Assignment)
    assert assign.variable == 'z'
    
    # Expression should be: x + (y * 2)
    expr = assign.expression
    assert isinstance(expr, BinaryOp), "Top level should be BinaryOp"
    assert expr.operator == '+', "Top operator should be +"
    
    # Left side: x
    assert isinstance(expr.left, Variable), "Left should be Variable"
    assert expr.left.name == 'x'
    
    # Right side: y * 2
    assert isinstance(expr.right, BinaryOp), "Right should be BinaryOp"
    assert expr.right.operator == '*', "Right operator should be *"
    
    print("\n✅ TEST 2 PASSED!")
    return True


def test_operator_precedence():
    """Test: result = 2 + 3 * 4"""
    print("\n" + "="*60)
    print("TEST 3: Operator Precedence (2 + 3 * 4 = 14)")
    print("="*60)
    
    code = "result = 2 + 3 * 4"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput: {code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    # Should parse as: 2 + (3 * 4), NOT (2 + 3) * 4
    assign = ast.statements[0]
    expr = assign.expression
    
    # Top level: +
    assert expr.operator == '+', "Top operator should be +"
    
    # Left: 2
    assert isinstance(expr.left, Literal)
    assert expr.left.value == 2
    
    # Right: 3 * 4
    assert isinstance(expr.right, BinaryOp)
    assert expr.right.operator == '*'
    assert expr.right.left.value == 3
    assert expr.right.right.value == 4
    
    print("\n✅ TEST 3 PASSED! (Correct precedence: * before +)")
    return True


def test_parentheses():
    """Test: result = (2 + 3) * 4"""
    print("\n" + "="*60)
    print("TEST 4: Parentheses Override ((2 + 3) * 4 = 20)")
    print("="*60)
    
    code = "result = (2 + 3) * 4"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput: {code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    # Should parse as: (2 + 3) * 4
    assign = ast.statements[0]
    expr = assign.expression
    
    # Top level: *
    assert expr.operator == '*', "Top operator should be *"
    
    # Left: 2 + 3
    assert isinstance(expr.left, BinaryOp)
    assert expr.left.operator == '+'
    
    # Right: 4
    assert isinstance(expr.right, Literal)
    assert expr.right.value == 4
    
    print("\n✅ TEST 4 PASSED! (Parentheses correctly override precedence)")
    return True


def test_comparison_operators():
    """Test: valid = x > 5"""
    print("\n" + "="*60)
    print("TEST 5: Comparison Operators (x > 5)")
    print("="*60)
    
    code = "valid = x > 5"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput: {code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    assign = ast.statements[0]
    expr = assign.expression
    
    assert isinstance(expr, BinaryOp)
    assert expr.operator == '>'
    assert isinstance(expr.left, Variable)
    assert expr.left.name == 'x'
    assert isinstance(expr.right, Literal)
    assert expr.right.value == 5
    
    print("\n✅ TEST 5 PASSED!")
    return True


def test_if_statement():
    """Test: if (x > 0) { print(x) }"""
    print("\n" + "="*60)
    print("TEST 6: If Statement")
    print("="*60)
    
    code = """if (x > 0) {
    print(x)
}"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput:\n{code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    assert ast is not None
    assert len(ast.statements) == 1
    
    if_stmt = ast.statements[0]
    assert isinstance(if_stmt, IfStatement)
    
    # Check condition: x > 0
    assert isinstance(if_stmt.condition, BinaryOp)
    assert if_stmt.condition.operator == '>'
    
    # Check then block
    assert len(if_stmt.then_block) == 1
    assert isinstance(if_stmt.then_block[0], PrintStatement)
    
    # No else block
    assert if_stmt.else_block is None
    
    print("\n✅ TEST 6 PASSED!")
    return True


def test_if_else_statement():
    """Test: if-else"""
    print("\n" + "="*60)
    print("TEST 7: If-Else Statement")
    print("="*60)
    
    code = """if (x > 0) {
    print(x)
} else {
    print(0)
}"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput:\n{code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    if_stmt = ast.statements[0]
    assert isinstance(if_stmt, IfStatement)
    
    # Check then block
    assert len(if_stmt.then_block) == 1
    
    # Check else block exists
    assert if_stmt.else_block is not None
    assert len(if_stmt.else_block) == 1
    assert isinstance(if_stmt.else_block[0], PrintStatement)
    
    print("\n✅ TEST 7 PASSED!")
    return True


def test_while_loop():
    """Test: while (count < 3) { count = count + 1 }"""
    print("\n" + "="*60)
    print("TEST 8: While Loop")
    print("="*60)
    
    code = """while (count < 3) {
    count = count + 1
}"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput:\n{code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    assert ast is not None
    assert len(ast.statements) == 1
    
    while_stmt = ast.statements[0]
    assert isinstance(while_stmt, WhileStatement)
    
    # Check condition: count < 3
    assert isinstance(while_stmt.condition, BinaryOp)
    assert while_stmt.condition.operator == '<'
    
    # Check body
    assert len(while_stmt.body) == 1
    assert isinstance(while_stmt.body[0], Assignment)
    
    print("\n✅ TEST 8 PASSED!")
    return True


def test_multiple_statements():
    """Test: Multiple statements in sequence"""
    print("\n" + "="*60)
    print("TEST 9: Multiple Statements")
    print("="*60)
    
    code = """x = 5
y = 10
z = x + y
print(z)"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput:\n{code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    assert ast is not None
    assert len(ast.statements) == 4, f"Should have 4 statements, got {len(ast.statements)}"
    
    # Check each statement type
    assert isinstance(ast.statements[0], Assignment)
    assert isinstance(ast.statements[1], Assignment)
    assert isinstance(ast.statements[2], Assignment)
    assert isinstance(ast.statements[3], PrintStatement)
    
    print("\n✅ TEST 9 PASSED!")
    return True


def test_complete_program():
    """Test: Complete program with all features"""
    print("\n" + "="*60)
    print("TEST 10: Complete Program")
    print("="*60)
    
    code = """x = 5
y = 10
sum = x + y

if (sum > 10) {
    print(sum)
} else {
    print(0)
}

count = 0
while (count < 3) {
    count = count + 1
    print(count)
}"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput:\n{code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    assert ast is not None
    assert len(ast.statements) == 6, f"Should have 6 statements, got {len(ast.statements)}"
    
    # Verify statement types
    assert isinstance(ast.statements[0], Assignment)  # x = 5
    assert isinstance(ast.statements[1], Assignment)  # y = 10
    assert isinstance(ast.statements[2], Assignment)  # sum = x + y
    assert isinstance(ast.statements[3], IfStatement) # if-else
    assert isinstance(ast.statements[4], Assignment)  # count = 0
    assert isinstance(ast.statements[5], WhileStatement) # while
    
    print("\n✅ TEST 10 PASSED!")
    return True


def test_logical_operators():
    """Test: Logical AND and OR"""
    print("\n" + "="*60)
    print("TEST 11: Logical Operators (&&, ||)")
    print("="*60)
    
    code = "result = x > 0 && y < 10"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput: {code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    assign = ast.statements[0]
    expr = assign.expression
    
    # Top level should be &&
    assert isinstance(expr, BinaryOp)
    assert expr.operator == '&&'
    
    # Left: x > 0
    assert isinstance(expr.left, BinaryOp)
    assert expr.left.operator == '>'
    
    # Right: y < 10
    assert isinstance(expr.right, BinaryOp)
    assert expr.right.operator == '<'
    
    print("\n✅ TEST 11 PASSED!")
    return True


def test_unary_operators():
    """Test: Unary minus and not"""
    print("\n" + "="*60)
    print("TEST 12: Unary Operators (-, !)")
    print("="*60)
    
    code = "x = -5"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"\nInput: {code}")
    print(f"\nAST generated:")
    if ast:
        print_ast(ast)
    
    assign = ast.statements[0]
    expr = assign.expression
    
    assert isinstance(expr, UnaryOp)
    assert expr.operator == '-'
    assert isinstance(expr.operand, Literal)
    assert expr.operand.value == 5
    
    print("\n✅ TEST 12 PASSED!")
    return True


def run_all_tests():
    """Run all parser tests"""
    print("\n" + "🧪"*30)
    print("RUNNING PARSER TESTS - PHASE 2")
    print("🧪"*30)
    
    tests = [
        test_simple_assignment,
        test_arithmetic_expression,
        test_operator_precedence,
        test_parentheses,
        test_comparison_operators,
        test_if_statement,
        test_if_else_statement,
        test_while_loop,
        test_multiple_statements,
        test_complete_program,
        test_logical_operators,
        test_unary_operators,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ TEST ERROR: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
    
    # Final summary
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    print(f"\n✅ Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(tests)}")
    else:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nPhase 2 (Parser) is complete and working!")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()