"""
Tests for Code Generator
Run with: python3 tests/test_codegen.py
"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator


def compile_to_tac(code: str):
    """Helper: Compile code to TAC"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    if not ast:
        return None
    
    analyzer = SemanticAnalyzer()
    if not analyzer.analyze(ast):
        return None
    
    codegen = CodeGenerator()
    tac = codegen.generate(ast)
    
    return codegen


def test_simple_assignment():
    """Test: x = 5"""
    print("\n" + "="*60)
    print("TEST 1: Simple Assignment")
    print("="*60)
    
    code = "x = 5"
    codegen = compile_to_tac(code)
    
    print(f"\nInput: {code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    # Should have 1 instruction: x = 5
    assert len(codegen.instructions) == 1
    assert str(codegen.instructions[0]) == "x = 5"
    
    print("\n✅ TEST 1 PASSED!")
    return True


def test_arithmetic_expression():
    """Test: z = x + y"""
    print("\n" + "="*60)
    print("TEST 2: Arithmetic Expression (x + y)")
    print("="*60)
    
    code = """x = 5
y = 10
z = x + y"""
    
    codegen = compile_to_tac(code)
    
    print(f"\nInput:\n{code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    # Should have:
    # x = 5
    # y = 10
    # t0 = x + y
    # z = t0
    assert len(codegen.instructions) == 4
    
    print("\n✅ TEST 2 PASSED!")
    return True


def test_operator_precedence():
    """Test: z = x + y * 2"""
    print("\n" + "="*60)
    print("TEST 3: Operator Precedence (x + y * 2)")
    print("="*60)
    
    code = "z = x + y * 2"
    codegen = compile_to_tac(code)
    
    print(f"\nInput: {code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    # Should have:
    # t0 = y * 2    (multiplication first)
    # t1 = x + t0   (then addition)
    # z = t1
    assert len(codegen.instructions) == 3
    assert 't0 = y * 2' in str(codegen.instructions[0])
    assert 't1 = x + t0' in str(codegen.instructions[1])
    
    print("\n✅ TEST 3 PASSED! (Correct precedence in TAC)")
    return True


def test_complex_expression():
    """Test: result = (a + b) * c"""
    print("\n" + "="*60)
    print("TEST 4: Complex Expression ((a + b) * c)")
    print("="*60)
    
    code = "result = (a + b) * c"
    codegen = compile_to_tac(code)
    
    print(f"\nInput: {code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    # Should have:
    # t0 = a + b
    # t1 = t0 * c
    # result = t1
    assert len(codegen.instructions) == 3
    
    print("\n✅ TEST 4 PASSED!")
    return True


def test_if_statement():
    """Test: if (x > 0) { y = 1 }"""
    print("\n" + "="*60)
    print("TEST 5: If Statement")
    print("="*60)
    
    code = """x = 5
if (x > 0) {
    y = 1
}"""
    
    codegen = compile_to_tac(code)
    
    print(f"\nInput:\n{code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    # Should have:
    # x = 5
    # t0 = x > 0
    # if_false t0 goto L0
    # y = 1
    # goto L1
    # L0:
    # L1:
    
    instructions_str = [str(i) for i in codegen.instructions]
    
    # Check for if_false
    assert any('if_false' in s for s in instructions_str)
    
    # Check for labels
    assert any('L0:' in s for s in instructions_str)
    assert any('L1:' in s for s in instructions_str)
    
    print("\n✅ TEST 5 PASSED!")
    return True

def test_if_else_statement():
    """Test: if-else"""
    print("\n" + "="*60)
    print("TEST 6: If-Else Statement")
    print("="*60)
    
    code = """x = 5
if (x > 0) {
    y = 1
} else {
    y = 0
}"""
    
    codegen = compile_to_tac(code)
    
    print(f"\nInput:\n{code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    instructions_str = [str(i) for i in codegen.instructions]
    
    # Check structure
    assert any('if_false' in s for s in instructions_str)
    assert any('goto' in s and 'L1' in s for s in instructions_str)
    
    print("\n✅ TEST 6 PASSED!")
    return True

def test_while_loop():
    """Test: while (count < 3) { count = count + 1 }"""
    print("\n" + "="*60)
    print("TEST 7: While Loop")
    print("="*60)
    
    code = """count = 0
while (count < 3) {
    count = count + 1
}"""
    
    codegen = compile_to_tac(code)
    
    print(f"\nInput:\n{code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    instructions_str = [str(i) for i in codegen.instructions]
    
    # Should have loop structure:
    # - Start label
    # - Condition check
    # - if_false to end
    # - Body
    # - goto back to start
    # - End label
    
    assert any('L0:' in s for s in instructions_str)  # Start label
    assert any('if_false' in s for s in instructions_str)
    assert any('goto L0' in s for s in instructions_str)  # Back to start
    
    print("\n✅ TEST 7 PASSED!")
    return True


def test_print_statement():
    """Test: print(x)"""
    print("\n" + "="*60)
    print("TEST 8: Print Statement")
    print("="*60)
    
    code = """x = 42
print(x)"""
    
    codegen = compile_to_tac(code)
    
    print(f"\nInput:\n{code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    instructions_str = [str(i) for i in codegen.instructions]
    
    assert any('print x' in s for s in instructions_str)
    
    print("\n✅ TEST 8 PASSED!")
    return True


def test_complete_program():
    """Test: Complete program"""
    print("\n" + "="*60)
    print("TEST 9: Complete Program with All Features")
    print("="*60)
    
    code = """x = 5
y = 10
z = x + y * 2

if (z > 15) {
    print(z)
} else {
    print(0)
}

count = 0
while (count < 3) {
    count = count + 1
    print(count)
}"""
    
    codegen = compile_to_tac(code)
    
    print(f"\nInput:\n{code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    # Should have many instructions
    assert len(codegen.instructions) > 15
    
    # Should have labels, jumps, prints
    instructions_str = [str(i) for i in codegen.instructions]
    assert any('if_false' in s for s in instructions_str)
    assert any('goto' in s for s in instructions_str)
    assert any('print' in s for s in instructions_str)
    
    print("\n✅ TEST 9 PASSED!")
    return True


def test_nested_expressions():
    """Test: Deeply nested expression"""
    print("\n" + "="*60)
    print("TEST 10: Nested Expressions")
    print("="*60)
    
    code = "result = a + b * c + d"
    codegen = compile_to_tac(code)
    
    print(f"\nInput: {code}")
    print("\nGenerated TAC:")
    print(codegen.get_code())
    
    # Should break down into multiple temps
    assert codegen.temp_counter >= 2
    
    print("\n✅ TEST 10 PASSED!")
    return True


def run_all_tests():
    """Run all code generation tests"""
    print("\n" + "🧪"*30)
    print("RUNNING CODE GENERATION TESTS - PHASE 4")
    print("🧪"*30)
    
    tests = [
        test_simple_assignment,
        test_arithmetic_expression,
        test_operator_precedence,
        test_complex_expression,
        test_if_statement,
        test_if_else_statement,
        test_while_loop,
        test_print_statement,
        test_complete_program,
        test_nested_expressions,
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
            import traceback
            traceback.print_exc()
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
        print("\nPhase 4 (Code Generation) is complete!")
        print("🎊 ALL 4 COMPILER PHASES ARE DONE! 🎊")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()