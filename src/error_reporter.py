"""
Error Reporter
Provides user-friendly error messages
"""

class ErrorReporter:
    """Formats and displays compilation errors"""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.split('\n')
    
    def report_error(self, error_type: str, line: int, column: int, message: str, suggestion: str = None):
        """
        Generate formatted error message
        
        Args:
            error_type: Type of error (LEXICAL, SYNTAX, SEMANTIC)
            line: Line number (1-indexed)
            column: Column number (1-indexed)
            message: Error description
            suggestion: Optional suggestion for fix
        """
        output = []
        output.append(f"\n {error_type} ERROR at line {line}, column {column}")
        output.append("-" * 60)
        
        # Show the problematic line
        if 0 <= line - 1 < len(self.lines):
            error_line = self.lines[line - 1]
            output.append(f"{line:4d} | {error_line}")
            
            # Show pointer to error location
            pointer = " " * (6 + column) + "^"
            output.append(pointer)
        
        output.append(f"\nError: {message}")
        
        if suggestion:
            output.append(f" Suggestion: {suggestion}")
        
        output.append("-" * 60)
        
        return "\n".join(output)