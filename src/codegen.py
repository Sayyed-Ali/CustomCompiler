"""
Code Generator
Generates Three-Address Code (TAC) from validated AST
"""

from typing import List, Optional
from ast_nodes import *


class TACInstruction:
    """Represents a single Three-Address Code instruction"""
    
    def __init__(self, op: str, arg1=None, arg2=None, result=None):
        self.op = op          # Operation: =, +, -, *, /, >, <, etc.
        self.arg1 = arg1      # First argument
        self.arg2 = arg2      # Second argument (for binary ops)
        self.result = result  # Result variable
    
    def __repr__(self):
        if self.op == '=':
            # Assignment: result = arg1
            return f"{self.result} = {self.arg1}"
        elif self.op in ['label']:
            # Label: L1:
            return f"{self.result}:"
        elif self.op in ['goto']:
            # Unconditional jump: goto L1
            return f"goto {self.result}"
        elif self.op in ['if_false', 'if_true']:
            # Conditional jump: if_false arg1 goto result
            return f"{self.op} {self.arg1} goto {self.result}"
        elif self.op == 'print':
            # Print: print arg1
            return f"print {self.arg1}"
        elif self.arg2 is None:
            # Unary operation: result = op arg1
            return f"{self.result} = {self.op}{self.arg1}"
        else:
            # Binary operation: result = arg1 op arg2
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


class CodeGenerator:
    """
    Generates Three-Address Code from AST
    """
    
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self) -> str:
        """Generate a new temporary variable"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self) -> str:
        """Generate a new label"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, op: str, arg1=None, arg2=None, result=None):
        """Emit a new TAC instruction"""
        instruction = TACInstruction(op, arg1, arg2, result)
        self.instructions.append(instruction)
        return instruction
    
    def generate(self, ast: Program) -> List[TACInstruction]:
        """
        Main code generation method
        Returns list of TAC instructions
        """
        for statement in ast.statements:
            self.generate_statement(statement)
        
        return self.instructions
    
    def generate_statement(self, stmt: ASTNode):
        """Generate code for a statement"""
        
        if isinstance(stmt, Assignment):
            self.generate_assignment(stmt)
        
        elif isinstance(stmt, IfStatement):
            self.generate_if_statement(stmt)
        
        elif isinstance(stmt, WhileStatement):
            self.generate_while_statement(stmt)
        
        elif isinstance(stmt, PrintStatement):
            self.generate_print_statement(stmt)
    
    def generate_assignment(self, stmt: Assignment):
        """
        Generate code for assignment
        Example: x = a + b * c
        
        TAC:
            t1 = b * c
            t2 = a + t1
            x = t2
        """
        # Generate code for the expression
        expr_result = self.generate_expression(stmt.expression)
        
        # Assign to variable
        self.emit('=', expr_result, None, stmt.variable)
    
    def generate_expression(self, expr: ASTNode) -> str:
        """
        Generate code for an expression
        Returns the name of the variable/temp holding the result
        """
        
        if isinstance(expr, Literal):
            # Literal values are used directly
            return str(expr.value)
        
        elif isinstance(expr, Variable):
            # Variable names are used directly
            return expr.name
        
        elif isinstance(expr, BinaryOp):
            return self.generate_binary_op(expr)
        
        elif isinstance(expr, UnaryOp):
            return self.generate_unary_op(expr)
        
        else:
            # Unknown expression type
            return "unknown"
    
    def generate_binary_op(self, expr: BinaryOp) -> str:
        """
        Generate code for binary operation
        Example: a + b
        
        Returns: temp variable holding result
        """
        # Generate code for left operand
        left = self.generate_expression(expr.left)
        
        # Generate code for right operand
        right = self.generate_expression(expr.right)
        
        # Create temp for result
        result = self.new_temp()
        
        # Emit instruction
        self.emit(expr.operator, left, right, result)
        
        return result
    
    def generate_unary_op(self, expr: UnaryOp) -> str:
        """
        Generate code for unary operation
        Example: -a or !flag
        """
        # Generate code for operand
        operand = self.generate_expression(expr.operand)
        
        # Create temp for result
        result = self.new_temp()
        
        # Emit instruction
        self.emit(expr.operator, operand, None, result)
        
        return result
    
    def generate_if_statement(self, stmt: IfStatement):
        """
        Generate code for if-else statement
        
        Pattern:
            <condition code>
            if_false <cond> goto L_else
            <then block>
            goto L_end
        L_else:
            <else block>
        L_end:
        """
        # Generate code for condition
        cond_result = self.generate_expression(stmt.condition)
        
        # Create labels
        label_else = self.new_label()
        label_end = self.new_label()
        
        # If condition is false, jump to else
        self.emit('if_false', cond_result, None, label_else)
        
        # Generate then block
        for statement in stmt.then_block:
            self.generate_statement(statement)
        
        # Jump to end (skip else block)
        self.emit('goto', None, None, label_end)
        
        # Else label
        self.emit('label', None, None, label_else)
        
        # Generate else block if present
        if stmt.else_block:
            for statement in stmt.else_block:
                self.generate_statement(statement)
        
        # End label
        self.emit('label', None, None, label_end)
    
    def generate_while_statement(self, stmt: WhileStatement):
        """
        Generate code for while loop
        
        Pattern:
        L_start:
            <condition code>
            if_false <cond> goto L_end
            <body>
            goto L_start
        L_end:
        """
        # Create labels
        label_start = self.new_label()
        label_end = self.new_label()
        
        # Start label
        self.emit('label', None, None, label_start)
        
        # Generate condition
        cond_result = self.generate_expression(stmt.condition)
        
        # If condition is false, exit loop
        self.emit('if_false', cond_result, None, label_end)
        
        # Generate body
        for statement in stmt.body:
            self.generate_statement(statement)
        
        # Jump back to start
        self.emit('goto', None, None, label_start)
        
        # End label
        self.emit('label', None, None, label_end)
    
    def generate_print_statement(self, stmt: PrintStatement):
        """Generate code for print statement"""
        # Generate code for expression
        expr_result = self.generate_expression(stmt.expression)
        
        # Emit print instruction
        self.emit('print', expr_result, None, None)
    
    def get_code(self) -> str:
        """Get TAC as formatted string"""
        lines = []
        for i, instruction in enumerate(self.instructions, 1):
            lines.append(f"{i:3d}:  {instruction}")
        return "\n".join(lines)
    
    def save_to_file(self, filename: str):
        """Save TAC to file"""
        with open(filename, 'w') as f:
            for instruction in self.instructions:
                f.write(str(instruction) + '\n')


# Simple test
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    from semantic import SemanticAnalyzer
    
    code = """
    x = 5
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
    }
    """
    
    print("="*60)
    print("CODE GENERATOR TEST")
    print("="*60)
    
    print("\nSource Code:")
    print(code)
    
    # Lexer
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(f"\n✓ Lexer: {len(tokens)} tokens generated")
    
    # Parser
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"✓ Parser: AST generated")
    
    # Semantic Analysis
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    print(f"✓ Semantic: Analysis complete")
    
    if success:
        # Code Generation
        print("\n" + "="*60)
        print("GENERATED THREE-ADDRESS CODE (TAC)")
        print("="*60)
        
        codegen = CodeGenerator()
        tac = codegen.generate(ast)
        
        print("\n" + codegen.get_code())
        
        print("\n" + "="*60)
        print(f"✓ Generated {len(tac)} TAC instructions")
        print("="*60)
    else:
        print("\n✗ Semantic analysis failed!")
        print(analyzer.generate_report())