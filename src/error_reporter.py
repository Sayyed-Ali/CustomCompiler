"""
Error reporter
creates beautiful, helpful error messages for users
"""

from typing import List, Optional

class ErrorReporter:
    """"Formats and displays compilation errors in a user friendly way"""

    def __init__(self,source_code:str):
        self.source_code=source_code
        self.lines= source_code.split('\n')

    def report_lexer_error(self,error:dict):
        """"Display a lexical analysis error"""
        line_num =error['line']
        col_num =error['column']
        error_type =error['message']

        print(f"\n{'='*60}")
        print(f"LEXICAL ERROR")
        print(f"{'='*60}")

        #show the line with the error
        if 1 <=line_num <= len(self.lines):
            print(f"\nLine{line_num}:")
            print(f"{self.lines[line_num-1]}")

            #point to the error location
            pointer =' '*col_num + '^'
            print(f" {pointer}")

        #error message
        #print(f"\n{message}")
        print(f"Type: {error_type}")

        print(f"\n{'='*60}\n")


    def report_spell_error(self, word: str, suggestion: dict, line: int, column: int):
        """"This is called by our spell checker"""

        print(f"\n{'='*60}")
        print(f"POSSIBLE SPELLING ERROR")
        print(f"{'='*60}")

        #Show the line
        if 1 <= line <= len(self.lines):
            print(f"\nLine {line}:")
            print(f" {self.lines[line-1]}")

            #POint to the word
            pointer =' '* column +'^' * len(word)
            print(f" {pointer}")

        #Main message
        print(f"\n Unknown identifier:'{word}'")

        #ML-powered suggestion
        print(f"\n Did you mean: '{suggestion['suggestion']}'?")
        print(f" Confidence:{suggestion['confidence']:.1f}%")

        # Show corrected code
        if 1 <= line <= len(self.lines):
            corrected_line = self.lines[line - 1].replace(word, suggestion['suggestion'], 1)
            print(f"\n✓ Suggested fix:")
            print(f"  {corrected_line}")

        # Show alternatives
        if len(suggestion['all_suggestions']) > 1:
            print(f"\nOther possibilities:")
            for alt in suggestion['all_suggestions'][1:]:
                print(f"   • {alt}")
        
        print(f"\n{'='*60}\n")


    def report_token_summary(self, tokens: List, errors: List):
        """Display a summary of tokenization results"""
        print(f"\n{'='*60}")
        print(f"LEXICAL ANALYSIS SUMMARY")
        print(f"{'='*60}")
        
        # Count tokens by type
        from collections import Counter
        token_counts = Counter(token.type.name for token in tokens if token.type.name != 'EOF')
        
        print(f"\nTotal tokens: {len(tokens) - 1}")  # -1 for EOF
        print(f"Token types: {len(token_counts)}")
        if errors:
            print(f"\n⚠️  Errors found: {len(errors)}")
        else:
            print(f"\nNo errors found!")
        
        # Show token breakdown
        print(f"\nToken breakdown:")
        for token_type, count in token_counts.most_common():
            print(f"  {token_type:15s} : {count:3d}")
        
        print(f"\n{'='*60}\n")


    # Test the error reporter
if __name__ == "__main__":
    test_code = """x = 5
y = 10
whiel (x > 0) {
    print(x)
}"""

    reporter = ErrorReporter(test_code)
    
    # Test lexical error
    print("Test 1: Lexical Error")
    error = {
        'type': 'INVALID_CHARACTER',
        'line': 3,
        'column': 5,
        'char': '@',
        'message': "Invalid character: '@'"
    }
    reporter.report_lexer_error(error)
    
    # Test spell error
    print("\nTest 2: Spelling Error (ML Feature)")
    suggestion = {
        'original': 'whiel',
        'suggestion': 'while',
        'confidence': 80.0,
        'distance': 1,
        'all_suggestions': ['while', 'if']
    }
    reporter.report_spell_error('whiel', suggestion, 3, 0)