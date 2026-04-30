"""
Semantic Analyzer
Performs semantic analysis and type checking
Integrates type inference (ML Feature #2)
"""

from typing import List, Dict, Optional
from ast_nodes import *
from symbol_table import SymbolTable, Symbol
from type_inference import TypeInferenceEngine


class SemanticAnalyzer:
    """
    Performs semantic analysis on the AST
    - Builds symbol table
    - Performs type inference
    - Validates types and scopes
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.type_engine = TypeInferenceEngine()
        self.errors: List[dict] = []
        self.warnings: List[dict] = []
        self.type_promotions: List[dict] = []
    
    def analyze(self, ast: Program) -> bool:
        """
        Main analysis method
        Returns True if no errors, False otherwise
        """
        # First pass: collect all variable declarations and infer types
        for statement in ast.statements:
            self.analyze_statement(statement)
        
        return len(self.errors) == 0
    
    def analyze_statement(self, stmt: ASTNode):
        """Analyze a single statement"""
        
        if isinstance(stmt, Assignment):
            self.analyze_assignment(stmt)
        
        elif isinstance(stmt, IfStatement):
            self.analyze_if_statement(stmt)
        
        elif isinstance(stmt, WhileStatement):
            self.analyze_while_statement(stmt)
        
        elif isinstance(stmt, PrintStatement):
            self.analyze_print_statement(stmt)
    
    def analyze_assignment(self, stmt: Assignment):
        """
        Analyze assignment statement
        This is where type inference happens!
        """
        # Infer the type of the expression
        expr_type = self.infer_expression_type(stmt.expression)
        
        # Check if variable already exists
        existing_symbol = self.symbol_table.lookup(stmt.variable)
        
        if existing_symbol:
            # Variable already declared - check type compatibility
            if existing_symbol.type != expr_type and existing_symbol.type != 'unknown':
                # Type mismatch - but allow if one can be promoted
                if (existing_symbol.type, expr_type) in self.type_engine.promotion_rules:
                    # Promotion allowed
                    self.type_promotions.append({
                        'variable': stmt.variable,
                        'from_type': existing_symbol.type,
                        'to_type': expr_type,
                        'line': stmt.line
                    })
                    self.symbol_table.update_type(stmt.variable, expr_type)
                else:
                    self.errors.append({
                        'type': 'TYPE_MISMATCH',
                        'variable': stmt.variable,
                        'expected': existing_symbol.type,
                        'got': expr_type,
                        'line': stmt.line,
                        'column': stmt.column,
                        'message': f"Cannot assign {expr_type} to variable '{stmt.variable}' of type {existing_symbol.type}"
                    })
        else:
            # New variable - add to symbol table with inferred type
            self.symbol_table.add_symbol(
                name=stmt.variable,
                symbol_type=expr_type,
                line=stmt.line,
                column=stmt.column
            )
    
    def analyze_if_statement(self, stmt: IfStatement):
        """Analyze if statement"""
        # Check condition type - should be bool
        cond_type = self.infer_expression_type(stmt.condition)
        
        if cond_type != 'bool' and cond_type != 'unknown':
            self.errors.append({
                'type': 'TYPE_MISMATCH',
                'expected': 'bool',
                'got': cond_type,
                'line': stmt.line,
                'column': stmt.column,
                'message': f"If condition must be bool, got {cond_type}"
            })
        
        # Analyze then block
        for statement in stmt.then_block:
            self.analyze_statement(statement)
        
        # Analyze else block if present
        if stmt.else_block:
            for statement in stmt.else_block:
                self.analyze_statement(statement)
    
    def analyze_while_statement(self, stmt: WhileStatement):
        """Analyze while statement"""
        # Check condition type - should be bool
        cond_type = self.infer_expression_type(stmt.condition)
        
        if cond_type != 'bool' and cond_type != 'unknown':
            self.errors.append({
                'type': 'TYPE_MISMATCH',
                'expected': 'bool',
                'got': cond_type,
                'line': stmt.line,
                'column': stmt.column,
                'message': f"While condition must be bool, got {cond_type}"
            })
        
        # Analyze body
        for statement in stmt.body:
            self.analyze_statement(statement)
    
    def analyze_print_statement(self, stmt: PrintStatement):
        """Analyze print statement"""
        # Just check that the expression has a valid type
        expr_type = self.infer_expression_type(stmt.expression)
        
        if expr_type == 'error':
            self.errors.append({
                'type': 'TYPE_ERROR',
                'line': stmt.line,
                'column': stmt.column,
                'message': f"Invalid expression in print statement"
            })
    
    def infer_expression_type(self, expr: ASTNode) -> str:
        """
        Infer the type of an expression
        Delegates to type inference engine
        """
        # Build a simple symbol table dict for the type engine
        symbol_types = {name: symbol.type for name, symbol in self.symbol_table.symbols.items()}
        
        return self.type_engine.infer_expression_type(expr, symbol_types)
    
    def check_variable_usage(self, expr: ASTNode):
        """
        Check that all variables are declared before use
        """
        if isinstance(expr, Variable):
            if not self.symbol_table.lookup(expr.name):
                self.errors.append({
                    'type': 'UNDEFINED_VARIABLE',
                    'variable': expr.name,
                    'line': expr.line,
                    'column': expr.column,
                    'message': f"Variable '{expr.name}' used before declaration"
                })
        
        elif isinstance(expr, BinaryOp):
            self.check_variable_usage(expr.left)
            self.check_variable_usage(expr.right)
        
        elif isinstance(expr, UnaryOp):
            self.check_variable_usage(expr.operand)
    
    def generate_report(self) -> str:
        """Generate a comprehensive analysis report"""
        lines = []
        
        lines.append("\n" + "="*60)
        lines.append(" SEMANTIC ANALYSIS REPORT")
        lines.append("="*60)
        
        # Symbol table
        lines.append("\n" + str(self.symbol_table))
        
        # Type promotions
        if self.type_promotions:
            lines.append("\n  Type Promotions:")
            for promo in self.type_promotions:
                lines.append(f"  Line {promo['line']}: {promo['variable']} "
                           f"{promo['from_type']} → {promo['to_type']}")
        
        # Errors
        if self.errors:
            lines.append(f"\n Errors: {len(self.errors)}")
            for error in self.errors:
                lines.append(f"  Line {error.get('line', '?')}: {error['message']}")
        else:
            lines.append("\n No errors found!")
        
        # Warnings
        if self.warnings:
            lines.append(f"\n⚠️  Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                lines.append(f"  Line {warning.get('line', '?')}: {warning['message']}")
        
        lines.append("\n" + "="*60)
        
        return "\n".join(lines)


# Simple test
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    
    code = """
    x = 5
    y = 3.14
    z = x + y
    
    if (z > 5.0) {
        print(z)
    }
    """
    
    print("Testing Semantic Analyzer\n")
    print("Code:")
    print(code)
    
    # Lexer
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    if ast:
        # Semantic analysis
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        
        print(analyzer.generate_report())
        
        if success:
            print("\n Semantic analysis passed!")
        else:
            print("\n Semantic analysis failed!")
    else:
        print(" Parsing failed!")