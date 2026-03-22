"""
Syntax Analyzer (Parser)
Converts token stream into Abstract Syntax Tree (AST)
Uses Recursive Descent Parsing
"""

from typing import List, Optional
from lexer import Token, TokenType
from ast_nodes import *


class Parser:
    """
    Recursive Descent Parser
    Builds AST from token stream
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.errors: List[dict] = []
    
    def current_token(self) -> Optional[Token]:
        """Get current token without advancing"""
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Look ahead at next token(s)"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.tokens):
            return None
        return self.tokens[peek_pos]
    
    def advance(self) -> Token:
        """Move to next token and return current"""
        token = self.current_token()
        if self.pos < len(self.tokens):
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Optional[Token]:
        """
        Expect a specific token type.
        If found, advance and return it.
        If not found, report error.
        """
        token = self.current_token()
        
        if token is None:
            self.errors.append({
                'type': 'UNEXPECTED_EOF',
                'expected': token_type.name,
                'message': f"Expected {token_type.name} but reached end of file"
            })
            return None
        
        if token.type != token_type:
            self.errors.append({
                'type': 'UNEXPECTED_TOKEN',
                'expected': token_type.name,
                'got': token.type.name,
                'line': token.line,
                'column': token.column,
                'message': f"Expected {token_type.name} but got {token.type.name} at line {token.line}"
            })
            return None
        
        return self.advance()
    
    def parse(self) -> Optional[Program]:
        """
        Main parsing method
        Returns Program AST node or None if errors
        """
        statements = []
        
        while self.current_token() and self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                # Error occurred, try to recover by skipping to next statement
                self.advance()
        
        if self.errors:
            return None
        
        return Program(statements=statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """
        Parse a single statement
        Statement → Assignment | IfStatement | WhileStatement | PrintStatement
        """
        token = self.current_token()
        
        if not token or token.type == TokenType.EOF:
            return None
        
        # If statement
        if token.type == TokenType.IF:
            return self.parse_if_statement()
        
        # While statement
        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()
        
        # Print statement
        elif token.type == TokenType.PRINT:
            return self.parse_print_statement()
        
        # Assignment (starts with identifier or type keyword)
        elif token.type == TokenType.IDENTIFIER or token.type in [
            TokenType.INT, TokenType.FLOAT, TokenType.STRING_TYPE, TokenType.BOOL
        ]:
            return self.parse_assignment()
        
        else:
            self.errors.append({
                'type': 'UNEXPECTED_TOKEN',
                'token': token.type.name,
                'line': token.line,
                'column': token.column,
                'message': f"Unexpected token {token.type.name} at line {token.line}"
            })
            return None
    
    def parse_assignment(self) -> Optional[Assignment]:
        """
        Parse assignment statement
        Assignment → [Type] Identifier = Expression
        """
        # Optional type declaration
        if self.current_token().type in [TokenType.INT, TokenType.FLOAT, 
                                         TokenType.STRING_TYPE, TokenType.BOOL]:
            self.advance()  # Skip type for now (we'll use type inference)
        
        # Get identifier
        ident_token = self.expect(TokenType.IDENTIFIER)
        if not ident_token:
            return None
        
        variable_name = ident_token.value
        
        # Expect '='
        if not self.expect(TokenType.ASSIGN):
            return None
        
        # Parse expression
        expr = self.parse_expression()
        if not expr:
            return None
        
        return Assignment(
            variable=variable_name,
            expression=expr,
            line=ident_token.line,
            column=ident_token.column
        )
    
    def parse_if_statement(self) -> Optional[IfStatement]:
        """
        Parse if statement
        IfStatement → if (Expression) { Statement* } [else { Statement* }]
        """
        if_token = self.expect(TokenType.IF)
        if not if_token:
            return None
        
        # Expect '('
        if not self.expect(TokenType.LPAREN):
            return None
        
        # Parse condition
        condition = self.parse_expression()
        if not condition:
            return None
        
        # Expect ')'
        if not self.expect(TokenType.RPAREN):
            return None
        
        # Expect '{'
        if not self.expect(TokenType.LBRACE):
            return None
        
        # Parse then block
        then_block = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
            else:
                break
        
        # Expect '}'
        if not self.expect(TokenType.RBRACE):
            return None
        
        # Optional else block
        else_block = None
        if self.current_token() and self.current_token().type == TokenType.ELSE:
            self.advance()  # consume 'else'
            
            # Expect '{'
            if not self.expect(TokenType.LBRACE):
                return None
            
            else_block = []
            while self.current_token() and self.current_token().type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
                else:
                    break
            
            # Expect '}'
            if not self.expect(TokenType.RBRACE):
                return None
        
        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block,
            line=if_token.line,
            column=if_token.column
        )
    
    def parse_while_statement(self) -> Optional[WhileStatement]:
        """
        Parse while loop
        WhileStatement → while (Expression) { Statement* }
        """
        while_token = self.expect(TokenType.WHILE)
        if not while_token:
            return None
        
        # Expect '('
        if not self.expect(TokenType.LPAREN):
            return None
        
        # Parse condition
        condition = self.parse_expression()
        if not condition:
            return None
        
        # Expect ')'
        if not self.expect(TokenType.RPAREN):
            return None
        
        # Expect '{'
        if not self.expect(TokenType.LBRACE):
            return None
        
        # Parse body
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        # Expect '}'
        if not self.expect(TokenType.RBRACE):
            return None
        
        return WhileStatement(
            condition=condition,
            body=body,
            line=while_token.line,
            column=while_token.column
        )
    
    def parse_print_statement(self) -> Optional[PrintStatement]:
        """
        Parse print statement
        PrintStatement → print(Expression)
        """
        print_token = self.expect(TokenType.PRINT)
        if not print_token:
            return None
        
        # Expect '('
        if not self.expect(TokenType.LPAREN):
            return None
        
        # Parse expression
        expr = self.parse_expression()
        if not expr:
            return None
        
        # Expect ')'
        if not self.expect(TokenType.RPAREN):
            return None
        
        return PrintStatement(
            expression=expr,
            line=print_token.line,
            column=print_token.column
        )
    
    def parse_expression(self) -> Optional[ASTNode]:
        """
        Parse expression with operators
        Expression → Comparison ((&&||| ) Comparison)*
        """
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> Optional[ASTNode]:
        """
        LogicalOr → LogicalAnd (|| LogicalAnd)*
        """
        left = self.parse_logical_and()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type == TokenType.OR:
            op_token = self.advance()
            right = self.parse_logical_and()
            if not right:
                return None
            
            left = BinaryOp(
                operator=op_token.value,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_logical_and(self) -> Optional[ASTNode]:
        """
        LogicalAnd → Comparison (&& Comparison)*
        """
        left = self.parse_comparison()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type == TokenType.AND:
            op_token = self.advance()
            right = self.parse_comparison()
            if not right:
                return None
            
            left = BinaryOp(
                operator=op_token.value,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_comparison(self) -> Optional[ASTNode]:
        """
        Comparison → AddSub ((==|!=|<|<=|>|>=) AddSub)*
        """
        left = self.parse_add_sub()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type in [
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL
        ]:
            op_token = self.advance()
            right = self.parse_add_sub()
            if not right:
                return None
            
            left = BinaryOp(
                operator=op_token.value,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_add_sub(self) -> Optional[ASTNode]:
        """
        AddSub → MulDiv ((+|-) MulDiv)*
        """
        left = self.parse_mul_div()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.advance()
            right = self.parse_mul_div()
            if not right:
                return None
            
            left = BinaryOp(
                operator=op_token.value,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_mul_div(self) -> Optional[ASTNode]:
        """
        MulDiv → Unary ((*|/|%) Unary)*
        """
        left = self.parse_unary()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type in [
            TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO
        ]:
            op_token = self.advance()
            right = self.parse_unary()
            if not right:
                return None
            
            left = BinaryOp(
                operator=op_token.value,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_unary(self) -> Optional[ASTNode]:
        """
        Unary → (-|!) Primary | Primary
        """
        token = self.current_token()
        
        if token and token.type in [TokenType.MINUS, TokenType.NOT]:
            op_token = self.advance()
            operand = self.parse_unary()
            if not operand:
                return None
            
            return UnaryOp(
                operator=op_token.value,
                operand=operand,
                line=op_token.line,
                column=op_token.column
            )
        
        return self.parse_primary()
    
    def parse_primary(self) -> Optional[ASTNode]:
        """
        Primary → Number | String | true | false | Identifier | (Expression)
        """
        token = self.current_token()
        
        if not token:
            self.errors.append({
                'type': 'UNEXPECTED_EOF',
                'message': "Unexpected end of file in expression"
            })
            return None
        
        # Number
        if token.type == TokenType.NUMBER:
            self.advance()
            # Determine if int or float
            if isinstance(token.value, float):
                lit_type = 'float'
            else:
                lit_type = 'int'
            
            return Literal(
                value=token.value,
                literal_type=lit_type,
                line=token.line,
                column=token.column
            )
        
        # String
        elif token.type == TokenType.STRING:
            self.advance()
            return Literal(
                value=token.value,
                literal_type='string',
                line=token.line,
                column=token.column
            )
        
        # Boolean true
        elif token.type == TokenType.TRUE:
            self.advance()
            return Literal(
                value=True,
                literal_type='bool',
                line=token.line,
                column=token.column
            )
        
        # Boolean false
        elif token.type == TokenType.FALSE:
            self.advance()
            return Literal(
                value=False,
                literal_type='bool',
                line=token.line,
                column=token.column
            )
        
        # Identifier (variable reference)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Variable(
                name=token.value,
                line=token.line,
                column=token.column
            )
        
        # Parentheses (grouped expression)
        elif token.type == TokenType.LPAREN:
            self.advance()  # consume '('
            
            expr = self.parse_expression()
            if not expr:
                return None
            
            if not self.expect(TokenType.RPAREN):
                return None
            
            return expr
        
        else:
            self.errors.append({
                'type': 'UNEXPECTED_TOKEN',
                'token': token.type.name,
                'line': token.line,
                'column': token.column,
                'message': f"Unexpected token {token.type.name} in expression at line {token.line}"
            })
            return None


# Simple test
if __name__ == "__main__":
    from lexer import Lexer
    
    code = """
    x = 5
    y = 10
    z = x + y * 2
    print(z)
    """
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
    
    print("\n" + "="*60 + "\n")
    
    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    
    if ast:
        print("✓ Parsing successful!")
        print("\nAST:")
        print_ast(ast)
    else:
        print("✗ Parsing failed!")
        print("\nErrors:")
        for error in parser.errors:
            print(f"  {error}")