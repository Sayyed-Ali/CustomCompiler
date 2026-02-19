"""
Tests for the Lexer
"""
print(" Test file is loading...")

import sys
sys.path.insert(0, 'src')

from lexer import Lexer, TokenType
from spell_checker import KeywordSpellChecker
from error_reporter import ErrorReporter


def test_simple_assignment():
    """Test: x = 5"""
    print("\n" + "="*60)
    print("TEST 1: Simple Assignment (x = 5)")
    print("="*60)
    
    code = "x = 5"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nInput: {code}")
    print(f"\nTokens generated: {len(tokens)}")
    for token in tokens:
        print(f"  {token}")
    
    # Verify
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == 'x'
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == 5
    assert tokens[3].type == TokenType.EOF
    
    print("\n TEST 1 PASSED!")
    return True


def test_arithmetic_expression():
    """Test: z = x + y * 2"""
    print("\n" + "="*60)
    print("TEST 2: Arithmetic Expression (z = x + y * 2)")
    print("="*60)
    
    code = "z = x + y * 2"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nInput: {code}")
    print(f"\nTokens generated: {len(tokens)}")
    for token in tokens:
        print(f"  {token}")
    
    # Verify we have the right tokens
    assert tokens[0].type == TokenType.IDENTIFIER  # z
    assert tokens[1].type == TokenType.ASSIGN      # =
    assert tokens[2].type == TokenType.IDENTIFIER  # x
    assert tokens[3].type == TokenType.PLUS        # +
    assert tokens[4].type == TokenType.IDENTIFIER  # y
    assert tokens[5].type == TokenType.MULTIPLY    # *
    assert tokens[6].type == TokenType.NUMBER      # 2
    
    print("\n TEST 2 PASSED!")
    return True


def test_if_statement():
    """Test: if (x > 5) { print(x) }"""
    print("\n" + "="*60)
    print("TEST 3: If Statement")
    print("="*60)
    
    code = """if (x > 5) {
    print(x)
}"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nInput:\n{code}")
    print(f"\nTokens generated: {len(tokens)}")
    for token in tokens:
        print(f"  {token}")
    
    # Check for if keyword
    assert tokens[0].type == TokenType.IF
    assert tokens[1].type == TokenType.LPAREN
    assert tokens[2].type == TokenType.IDENTIFIER  # x
    assert tokens[3].type == TokenType.GREATER     # >
    
    print("\n TEST 3 PASSED!")
    return True


def test_keywords():
    """Test: All keywords are recognized"""
    print("\n" + "="*60)
    print("TEST 4: Keyword Recognition")
    print("="*60)
    
    code = "int float string bool if else while print true false"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nInput: {code}")
    print(f"\nTokens generated: {len(tokens)}")
    
    expected = [
        TokenType.INT, TokenType.FLOAT, TokenType.STRING_TYPE, TokenType.BOOL,
        TokenType.IF, TokenType.ELSE, TokenType.WHILE, TokenType.PRINT,
        TokenType.TRUE, TokenType.FALSE
    ]
    
    for i, expected_type in enumerate(expected):
        print(f"  {tokens[i]}")
        assert tokens[i].type == expected_type
    
    print("\n TEST 4 PASSED!")
    return True


def test_string_literal():
    """Test: String literals"""
    print("\n" + "="*60)
    print("TEST 5: String Literals")
    print("="*60)
    
    code = 'name = "Hello World"'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nInput: {code}")
    print(f"\nTokens generated: {len(tokens)}")
    for token in tokens:
        print(f"  {token}")
    
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == 'name'
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.STRING
    assert tokens[2].value == "Hello World"
    
    print("\n TEST 5 PASSED!")
    return True


def test_comparison_operators():
    """Test: Comparison operators"""
    print("\n" + "="*60)
    print("TEST 6: Comparison Operators")
    print("="*60)
    
    code = "x == 5 != 3 < 10 <= 20 > 1 >= 0"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nInput: {code}")
    print(f"\nTokens generated: {len(tokens)}")
    for token in tokens:
        print(f"  {token}")
    
    # Check operators
    assert tokens[1].type == TokenType.EQUAL       # ==
    assert tokens[3].type == TokenType.NOT_EQUAL   # !=
    assert tokens[5].type == TokenType.LESS        # 
    assert tokens[7].type == TokenType.LESS_EQUAL  # <=
    assert tokens[9].type == TokenType.GREATER     # >
    assert tokens[11].type == TokenType.GREATER_EQUAL  # >=
    
    print("\n TEST 6 PASSED!")
    return True


def test_comments():
    """Test: Comments are ignored"""
    print("\n" + "="*60)
    print("TEST 7: Comments")
    print("="*60)
    
    code = """x = 5  // This is a comment
// Another comment
y = 10"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nInput:\n{code}")
    print(f"\nTokens generated: {len(tokens)}")
    for token in tokens:
        print(f"  {token}")
    
    # Should only have: x = 5 y = 10 EOF
    # Comments should be ignored
    assert len([t for t in tokens if t.type != TokenType.EOF]) == 6  # x = 5 y = 10
    
    print("\n TEST 7 PASSED!")
    return True


def test_spell_checker():
    """Test: Spell checker (ML Feature #1)"""
    print("\n" + "="*60)
    print("TEST 8: Spell Checker (ML FEATURE #1)")
    print("="*60)
    
    checker = KeywordSpellChecker()
    
    test_cases = [
        ("whiel", "while"),
        ("fi", "if"),
        ("pritn", "print"),
        ("intt", "int"),
    ]
    
    for typo, expected in test_cases:
        suggestion = checker.suggest_correction(typo)
        print(f"\n  '{typo}' → '{suggestion['suggestion']}' (confidence: {suggestion['confidence']:.1f}%)")
        assert suggestion['suggestion'] == expected
    
    print("\n TEST 8 PASSED!")
    return True


def test_error_reporter():
    """Test: Error reporter displays nicely"""
    print("\n" + "="*60)
    print("TEST 9: Error Reporter")
    print("="*60)
    
    code = """x = 5
whiel (x > 0) {
    print(x)
}"""
    
    reporter = ErrorReporter(code)
    
    # Simulate a spelling error
    suggestion = {
        'original': 'whiel',
        'suggestion': 'while',
        'confidence': 80.0,
        'distance': 1,
        'all_suggestions': ['while']
    }
    
    print("\nDisplaying spell error:")
    reporter.report_spell_error('whiel', suggestion, 2, 0)
    
    print(" TEST 9 PASSED!")
    return True


def test_complete_program():
    """Test: Complete small program"""
    print("\n" + "="*60)
    print("TEST 10: Complete Program")
    print("="*60)
    
    code = """x = 5
y = 10
z = x + y

if (z > 10) {
    print(z)
} else {
    print(0)
}

count = 0
while (count < 3) {
    count = count + 1
}"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    reporter = ErrorReporter(code)
    
    print(f"\nInput:\n{code}")
    print(f"\nTokens generated: {len(tokens)}")
    
    # Display summary
    reporter.report_token_summary(tokens, lexer.errors)
    
    assert len(lexer.errors) == 0
    assert len(tokens) > 0
    
    print(" TEST 10 PASSED!")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + ""*30)
    print("RUNNING LEXER TESTS - PHASE 1")
    print(""*30)
    
    tests = [
        test_simple_assignment,
        test_arithmetic_expression,
        test_if_statement,
        test_keywords,
        test_string_literal,
        test_comparison_operators,
        test_comments,
        test_spell_checker,
        test_error_reporter,
        test_complete_program,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n TEST FAILED: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n TEST ERROR: {test.__name__}")
            print(f"  error: {e}")
            failed += 1
            
    #Final summary
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"\n Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"Failed: {failed}/{len(tests)}")
    else:
        print("\n ALL TESTS PASSED!")
        print("\nPhase 1(Lexer) is complete and working!")
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("Starting tests...")
    try:
        run_all_tests()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()