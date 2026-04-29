"""
Parser - Syntax Analysis
Shows spell suggestions before syntax errors
"""

from typing import List, Optional
from dataclasses import dataclass
from lexer import Token, TokenType
from ast_nodes import *


class Parser:
    """Parse tokens into Abstract Syntax Tree"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        self.errors = []
        self.warnings = []
    
    def error(self, message: str):
        """Record error"""
        # Check if current token has spell warning
        if self.current_token and hasattr(self.current_token, 'spell_warning'):
            warning = self.current_token.spell_warning
            # Show spell suggestion INSTEAD of confusing syntax error
            self.errors.append({
                'type': 'SPELLING_ERROR',
                'line': self.current_token.line,
                'column': self.current_token.column,
                'message': f"Unknown identifier '{warning['original']}' - did you mean '{warning['suggestion']}'? (Confidence: {warning['confidence']}%)"
            })
        else:
            self.errors.append({
                'type': 'SYNTAX_ERROR',
                'line': self.current_token.line if self.current_token else 0,
                'column': self.current_token.column if self.current_token else 0,
                'message': message
            })
    
    def advance(self):
        """Move to next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def expect(self, token_type: TokenType) -> bool:
        """Check if current token matches expected type"""
        if self.current_token and self.current_token.type == token_type:
            self.advance()
            return True
        
        # Better error messages
        if self.current_token:
            expected = token_type.name
            got = self.current_token.type.name
            
            # Simplify confusing messages
            if 'PAREN' in expected or 'BRACE' in expected:
                if 'LPAREN' in expected:
                    self.error(f"Missing opening parenthesis '('")
                elif 'RPAREN' in expected:
                    self.error(f"Missing closing parenthesis ')'")
                elif 'LBRACE' in expected:
                    self.error(f"Missing opening brace '{{'")
                elif 'RBRACE' in expected:
                    self.error(f"Missing closing brace '}}'")
            elif expected == 'ASSIGN':
                self.error(f"Missing assignment operator '='")
            else:
                self.error(f"Expected {expected} but got {got}")
        else:
            self.error(f"Unexpected end of input, expected {token_type.name}")
        
        return False
    
    def parse(self) -> Optional[Program]:
        """Parse tokens into AST"""
        statements = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                # Skip to next statement on error
                while self.current_token and self.current_token.type not in [TokenType.EOF, TokenType.IDENTIFIER, TokenType.IF, TokenType.WHILE, TokenType.PRINT]:
                    self.advance()
        
        if self.errors:
            return None
        
        return Program(statements)
    
    def parse_statement(self):
        """Parse a single statement"""
        if not self.current_token:
            return None
        
        # Assignment
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        
        # If statement
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        
        # While statement
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        
        # Print statement
        elif self.current_token.type == TokenType.PRINT:
            return self.parse_print_statement()
        
        else:
            self.error(f"Unexpected token: {self.current_token.type.name}")
            return None
    
    def parse_assignment(self):
        """Parse assignment: var = expression"""
        if not self.current_token:
            return None
        
        var_name = self.current_token.value
        line = self.current_token.line
        col = self.current_token.column
        
        self.advance()
        
        if not self.expect(TokenType.ASSIGN):
            return None
        
        expr = self.parse_expression()
        if not expr:
            return None
        
        return Assignment(var_name, expr, line, col)
    
    def parse_expression(self):
        """Parse expression (logical OR level)"""
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        """Parse logical OR"""
        left = self.parse_logical_and()
        
        while self.current_token and self.current_token.type == TokenType.OR:
            op = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            
            right = self.parse_logical_and()
            if not right:
                return None
            
            left = BinaryOp(op, left, right, line, col)
        
        return left
    
    def parse_logical_and(self):
        """Parse logical AND"""
        left = self.parse_comparison()
        
        while self.current_token and self.current_token.type == TokenType.AND:
            op = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            
            right = self.parse_comparison()
            if not right:
                return None
            
            left = BinaryOp(op, left, right, line, col)
        
        return left
    
    def parse_comparison(self):
        """Parse comparison operators"""
        left = self.parse_add_sub()
        
        while self.current_token and self.current_token.type in [
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL
        ]:
            op = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            
            right = self.parse_add_sub()
            if not right:
                return None
            
            left = BinaryOp(op, left, right, line, col)
        
        return left
    
    def parse_add_sub(self):
        """Parse addition and subtraction"""
        left = self.parse_mul_div()
        
        while self.current_token and self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            
            right = self.parse_mul_div()
            if not right:
                return None
            
            left = BinaryOp(op, left, right, line, col)
        
        return left
    
    def parse_mul_div(self):
        """Parse multiplication and division"""
        left = self.parse_unary()
        
        while self.current_token and self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            
            right = self.parse_unary()
            if not right:
                return None
            
            left = BinaryOp(op, left, right, line, col)
        
        return left
    
    def parse_unary(self):
        """Parse unary operators"""
        if self.current_token and self.current_token.type in [TokenType.MINUS, TokenType.NOT]:
            op = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            
            operand = self.parse_unary()
            if not operand:
                return None
            
            return UnaryOp(op, operand, line, col)
        
        return self.parse_primary()
    
    def parse_primary(self):
        """Parse primary expressions"""
        if not self.current_token:
            self.error("Unexpected end of expression")
            return None
        
        # Number
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            literal_type = 'float' if isinstance(value, float) else 'int'
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            return Literal(value, literal_type, line, col)
        
        # String
        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            return Literal(value, 'string', line, col)
        
        # Boolean
        elif self.current_token.type in [TokenType.TRUE, TokenType.FALSE]:
            value = self.current_token.type == TokenType.TRUE
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            return Literal(value, 'bool', line, col)
        
        # Variable
        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            line = self.current_token.line
            col = self.current_token.column
            self.advance()
            return Variable(name, line, col)
        
        # Parenthesized expression
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            if not expr:
                return None
            
            if not self.expect(TokenType.RPAREN):
                return None
            
            return expr
        
        else:
            self.error(f"Unexpected token in expression: {self.current_token.type.name}")
            return None
    
    def parse_if_statement(self):
        """Parse if statement"""
        line = self.current_token.line
        col = self.current_token.column
        
        self.advance()  # Skip 'if'
        
        if not self.expect(TokenType.LPAREN):
            return None
        
        condition = self.parse_expression()
        if not condition:
            return None
        
        if not self.expect(TokenType.RPAREN):
            return None
        
        if not self.expect(TokenType.LBRACE):
            return None
        
        then_block = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
            else:
                break
        
        if not self.expect(TokenType.RBRACE):
            return None
        
        else_block = None
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.advance()
            
            if not self.expect(TokenType.LBRACE):
                return None
            
            else_block = []
            while self.current_token and self.current_token.type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
                else:
                    break
            
            if not self.expect(TokenType.RBRACE):
                return None
        
        return IfStatement(condition, then_block, else_block, line, col)
    
    def parse_while_statement(self):
        """Parse while statement"""
        line = self.current_token.line
        col = self.current_token.column
        
        self.advance()  # Skip 'while'
        
        if not self.expect(TokenType.LPAREN):
            return None
        
        condition = self.parse_expression()
        if not condition:
            return None
        
        if not self.expect(TokenType.RPAREN):
            return None
        
        if not self.expect(TokenType.LBRACE):
            return None
        
        body = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        if not self.expect(TokenType.RBRACE):
            return None
        
        return WhileStatement(condition, body, line, col)
    
    def parse_print_statement(self):
        """Parse print statement"""
        line = self.current_token.line
        col = self.current_token.column
        
        self.advance()  # Skip 'print'
        
        if not self.expect(TokenType.LPAREN):
            return None
        
        expr = self.parse_expression()
        if not expr:
            return None
        
        if not self.expect(TokenType.RPAREN):
            return None
        
        return PrintStatement(expr, line, col)