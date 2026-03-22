"""
Tests for Semantic Analyzer and Type Inference
Run with: python3 tests/test_semantic.py
"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer


def compile_code(code: str):
    """Helper function to compile code through all phases"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    if not ast:
        return None, None
    
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    return analyzer, success


def test_simple_type_inference():
    """Test: Type inference for simple literals"""
    print("\n" + "="*60)
    print("TEST 1: Simple Type Inference")
    print("="*60)
    
    code = """x = 5
y = 3.14
name = "Alice"
valid = true"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    # Verify
    assert success, "Should pass semantic analysis"
    assert analyzer.symbol_table.lookup('x').type == 'int'
    assert analyzer.symbol_table.lookup('y').type == 'float'
    assert analyzer.symbol_table.lookup('name').type == 'string'
    assert analyzer.symbol_table.lookup('valid').type == 'bool'
    
    print("\n✅ TEST 1 PASSED!")
    return True


def test_type_propagation():
    """Test: Type inference through expressions"""
    print("\n" + "="*60)
    print("TEST 2: Type Propagation (x + y)")
    print("="*60)
    
    code = """x = 5
y = 10
z = x + y"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    # z should be int (int + int = int)
    assert success
    assert analyzer.symbol_table.lookup('z').type == 'int'
    
    print("\n✅ TEST 2 PASSED! (z correctly inferred as int)")
    return True


def test_type_promotion():
    """Test: Type promotion (int + float = float)"""
    print("\n" + "="*60)
    print("TEST 3: Type Promotion (int + float → float)")
    print("="*60)
    
    code = """x = 5
y = 3.14
z = x + y"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    # z should be float (int + float = float with promotion)
    assert success
    assert analyzer.symbol_table.lookup('x').type == 'int'
    assert analyzer.symbol_table.lookup('y').type == 'float'
    assert analyzer.symbol_table.lookup('z').type == 'float'
    
    print("\n✅ TEST 3 PASSED! (Type promotion: int + float → float)")
    return True


def test_comparison_returns_bool():
    """Test: Comparison operators return bool"""
    print("\n" + "="*60)
    print("TEST 4: Comparison Returns Bool")
    print("="*60)
    
    code = """x = 5
y = 10
result = x > y"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    assert success
    assert analyzer.symbol_table.lookup('result').type == 'bool'
    
    print("\n✅ TEST 4 PASSED! (Comparison correctly returns bool)")
    return True


def test_if_condition_type():
    """Test: If condition must be bool"""
    print("\n" + "="*60)
    print("TEST 5: If Condition Type Check")
    print("="*60)
    
    code = """x = 5
if (x > 0) {
    y = 10
}"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    # Should pass - condition is bool
    assert success
    assert len(analyzer.errors) == 0
    
    print("\n✅ TEST 5 PASSED! (If condition correctly validated)")
    return True


def test_while_condition_type():
    """Test: While condition must be bool"""
    print("\n" + "="*60)
    print("TEST 6: While Condition Type Check")
    print("="*60)
    
    code = """count = 0
while (count < 3) {
    count = count + 1
}"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    assert success
    assert len(analyzer.errors) == 0
    
    print("\n✅ TEST 6 PASSED! (While condition correctly validated)")
    return True


def test_logical_operators():
    """Test: Logical operators with bool"""
    print("\n" + "="*60)
    print("TEST 7: Logical Operators (&&, ||)")
    print("="*60)
    
    code = """x = 5
y = 10
result = x > 0 && y < 20"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    assert success
    assert analyzer.symbol_table.lookup('result').type == 'bool'
    
    print("\n✅ TEST 7 PASSED! (Logical operators work correctly)")
    return True


def test_complex_expression():
    """Test: Complex expression with multiple operations"""
    print("\n" + "="*60)
    print("TEST 8: Complex Expression")
    print("="*60)
    
    code = """a = 5
b = 10
c = 2.5
result = a + b * c"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    # b * c = int * float = float
    # a + float = int + float = float
    # So result should be float
    assert success
    assert analyzer.symbol_table.lookup('result').type == 'float'
    
    print("\n✅ TEST 8 PASSED! (Complex expression correctly typed)")
    return True


def test_complete_program():
    """Test: Complete program with all features"""
    print("\n" + "="*60)
    print("TEST 9: Complete Program with Type Inference")
    print("="*60)
    
    code = """x = 5
y = 3.14
z = x + y

if (z > 5.0) {
    message = "Large"
    print(message)
}

count = 0
while (count < 3) {
    count = count + 1
    print(count)
}"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    assert success
    assert analyzer.symbol_table.lookup('x').type == 'int'
    assert analyzer.symbol_table.lookup('y').type == 'float'
    assert analyzer.symbol_table.lookup('z').type == 'float'
    assert analyzer.symbol_table.lookup('message').type == 'string'
    assert analyzer.symbol_table.lookup('count').type == 'int'
    
    print("\n✅ TEST 9 PASSED! (Complete program analyzed successfully)")
    return True


def test_unary_operators():
    """Test: Unary operators preserve type"""
    print("\n" + "="*60)
    print("TEST 10: Unary Operators")
    print("="*60)
    
    code = """x = 5
y = -x
valid = true
invalid = !valid"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    assert success
    assert analyzer.symbol_table.lookup('x').type == 'int'
    assert analyzer.symbol_table.lookup('y').type == 'int'  # -int = int
    assert analyzer.symbol_table.lookup('valid').type == 'bool'
    assert analyzer.symbol_table.lookup('invalid').type == 'bool'  # !bool = bool
    
    print("\n✅ TEST 10 PASSED! (Unary operators work correctly)")
    return True


def test_type_inference_showcase():
    """Test: Showcase type inference feature"""
    print("\n" + "="*60)
    print("TEST 11: TYPE INFERENCE SHOWCASE (ML Feature #2)")
    print("="*60)
    
    code = """x = 5
y = 3.14
z = x + y
valid = z > 5.0
message = "Result: "
count = 1"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput Code (NO TYPE DECLARATIONS!):\n{code}")
    print("\n🔍 Type Inference Results:")
    print(analyzer.generate_report())
    
    print("\n💡 What happened:")
    print("  • x = 5           → inferred as int")
    print("  • y = 3.14        → inferred as float")
    print("  • z = x + y       → inferred as float (int + float promotion)")
    print("  • valid = z > 5.0 → inferred as bool (comparison result)")
    print("  • message = \"...\" → inferred as string")
    print("  • count = 1       → inferred as int")
    
    assert success
    
    print("\n✅ TEST 11 PASSED! (Type inference working perfectly!)")
    return True


def test_multiple_assignments():
    """Test: Variable reassignment with same type"""
    print("\n" + "="*60)
    print("TEST 12: Multiple Assignments")
    print("="*60)
    
    code = """x = 5
x = 10
x = x + 1"""
    
    analyzer, success = compile_code(code)
    
    print(f"\nInput:\n{code}")
    print(analyzer.generate_report())
    
    assert success
    assert analyzer.symbol_table.lookup('x').type == 'int'
    
    print("\n✅ TEST 12 PASSED! (Reassignment works correctly)")
    return True


def run_all_tests():
    """Run all semantic analysis tests"""
    print("\n" + "🧪"*30)
    print("RUNNING SEMANTIC ANALYSIS TESTS - PHASE 3")
    print("🧪"*30)
    
    tests = [
        test_simple_type_inference,
        test_type_propagation,
        test_type_promotion,
        test_comparison_returns_bool,
        test_if_condition_type,
        test_while_condition_type,
        test_logical_operators,
        test_complex_expression,
        test_complete_program,
        test_unary_operators,
        test_type_inference_showcase,
        test_multiple_assignments,
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
        print("\nPhase 3 (Semantic Analysis + Type Inference) is complete!")
        print("ML Feature #2 (Type Inference) is working!")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()