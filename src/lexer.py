"""
Lexical Analyzer (lexer/tokenizer)
converst source code text into tokens
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto
from spell_checker import SpellChecker

class TokenType(Enum):
    "all possible token types"
    # Literals
    NUMBER = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()

    #Identifiers anf keyowrds
    IDENTIFIER = auto()

    # keywords
    INT = auto()
    FLOAT = auto()
    STRING_TYPE = auto()
    BOOL = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()

    # operands
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()

    # comparison
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # logical
    AND = auto()
    OR = auto()
    NOT = auto()

    # assignment
    ASSIGN = auto()

    # delimeters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    # special
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    """Represents a single token"""
    type: TokenType
    value: any
    line: int
    column: int

    def __repr__(self):
        return f'Token({self.type.name}, {self.value!r}, L{self.line}: C{self.column})'
    

class Lexer:
    """coverts source code into tokens"""

    def __init__(self, text:str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.spell_checker = SpellChecker()
        self.tokens: List[Token] = []
        self.errors: List[dict] = []

        # keyword mapping
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING_TYPE,
            'bool': TokenType.BOOL,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'print': TokenType.PRINT,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE
        }
    
    def current_char(self) -> Optional[str]:
        """get current char w/o advancing"""
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def peek_char(self, offset: int=1) -> Optional[str]:
        """look ahead at next char(s)"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def advance(self) -> Optional[str]:
        """move to next char"""
        if self.pos >= len(self.text):
            return None
        
        char = self.text[self.pos]
        self.pos += 1
        self.column += 1

        if char == '\n':
            self.line += 1
            self.column = 1

        return char

    def skip_whitespace(self):
        """skip spcae and tabs (but aline not newlines)"""
        while self.current_char() and self.current_char() in ' \t':
            self.advance()

    def skip_comment(self):
        """Skip single-line comments starting with //"""
        if self.current_char()=='/' and self.peek_char()=='/':
            # skip until end of line
            while self.current_char() and self.current_char()!='\n':
                self.advance()
            # now we are at '\n' advacne past it
            if self.current_char() == '\n':
                self.advance()


    def read_number(self) -> Token:
        """ read a number (integer or flaot)"""
        start_line = self.line
        start_col = self.column
        num_str = ''
        has_dot = False

        while self.current_char() and (self.current_char().isdigit() or self.current_char()=='.'):
            if self.current_char()=='.':
                if has_dot:
                    # second dot = error
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()

        # convert to appropridate type
        if has_dot:
            value = float(num_str)
        else:
            value = int(num_str)
        
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_string(self)->Token:
        """read a string literal"""
        start_line = self.line
        start_col = self.column

        # skip opeing quote
        quote_char = self.current_char() # " or '
        self.advance()

        string_value = ''

        while self.current_char() and self.current_char()!=quote_char:
            if self.current_char() == '\\':
                # handle escape sequemce
                self.advance()
                next_char = self.current_char()
                if next_char=='n':
                    string_value += '\n'
                elif next_char=='t':
                    string_value += '\t'
                elif next_char=='\\':
                    string_value += '\\'
                elif next_char==quote_char:
                    string_value += quote_char
                else:
                    string_value += next_char
                self.advance()
            else:
                string_value += self.current_char()
                self.advance()

        # skip closing quote
        if self.current_char()==quote_char:
            self.advance()
        else:
            self.errors.append({
                'type': 'UNTERMINATED_STRING',
                'line': start_line,
                'column': start_col,
                'message': 'Unterminated string literal'
            })

        return Token(TokenType.STRING, string_value, start_line, start_col)
    

    def read_identifier(self) -> Token:
        """Read identifier or keyword - checks spelling"""
        id_str = ''
        start_col = self.column
        start_line = self.line
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # Check if keyword
        token_type = self.keywords.get(id_str, TokenType.IDENTIFIER)
        
        # Create token
        token = Token(token_type, id_str, start_line, start_col)
        
        # ✅ CHECK SPELLING FOR EVERYTHING
        suggestion = self.spell_checker.check_keyword(id_str)
        if suggestion:
            token.spell_warning = suggestion
            token.spell_warning['line'] = start_line
            print(f"⚠️  Line {start_line}: '{id_str}' → '{suggestion['suggestion']}'?")
        
        return token
    

    def tokenize(self)->List[Token]:
        """ main tokenization method - converts entire text into tokens"""

        while self.pos<len(self.text):
            self.skip_whitespace()

            if self.current_char() is None:
                break
                
            # skip comments
            if self.current_char()=='/' and self.peek_char()=='/':
                self.skip_comment()
                continue

            char = self.current_char()
            start_line = self.line
            start_col = self.column

            # numbers
            if char.isdigit():
                self.tokens.append(self.read_number())

            # strings
            elif char in '"\'':
                self.tokens.append(self.read_string())

            # identifiers and keywords
            elif char.isalpha() or char=='_':
                self.tokens.append(self.read_identifier())

            # operators and delimeters (2-char)
            elif char=='=' and self.peek_char()=='=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', start_line, start_col))
            
            elif char=='!' and self.peek_char()=='=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_col))
            
            elif char=='<' and self.peek_char()=='=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
                
            elif char=='>' and self.peek_char()=='=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
            
            elif char=='&' and self.peek_char()=='&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.AND, '&&', start_line, start_col))
            
            elif char=='|' and self.peek_char()=='|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.OR, '||', start_line, start_col))
            
            # single char operators and delimeters
            elif char=='+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
            
            elif char=='-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
            
            elif char=='*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_col))
            
            elif char=='/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_col))
            
            elif char=='%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, '%', start_line, start_col))

            elif char=='=':
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col))
            
            elif char=='<':
                self.advance()
                self.tokens.append(Token(TokenType.LESS, '<', start_line, start_col))
            
            elif char=='>':
                self.advance()
                self.tokens.append(Token(TokenType.GREATER, '>', start_line, start_col))
            
            elif char=='!':
                self.advance()
                self.tokens.append(Token(TokenType.NOT, '!', start_line, start_col))
            
            elif char=='(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
            
            elif char==')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))

            elif char=='{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_col))
            
            elif char=='}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_col))
            
            elif char==';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col))
            
            elif char==',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
            
            elif char=='\n':
                self.advance()
                # we skip newlines is most cases
                continue

            else:
                # unknown char = error
                self.errors.append({
                    'type': 'INVALID_CHARACTER',
                    'line': start_line,
                    'column': start_col,
                    'char': char,
                    'message': f"Invalid character: '{char}'"
                })
                self.advance()

        # add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens


# simple test function
if __name__=="__main__":
    # test the lexer
    test_code = """
    x = 5
    y = 10
    z = x + y
    print(z)
    """

    lexer = Lexer(test_code)
    tokens = lexer.tokenize()

    print("Tokens:")
    for token in tokens:
        print(f" {token}")
    
    if lexer.errors:
        print("\nErrors:")
        for error in lexer.errors:
            print(f" {error}")
            
            



