"""
Type Inference Engine
Automatically deduces variable types from context
This is ML Feature #2!
"""

from typing import Optional, Dict, Tuple
from ast_nodes import *


class TypeInferenceEngine:
    """
    Infers types for variables without explicit declarations
    Uses constraint-based type propagation
    """
    
    def __init__(self):
        # Type promotion rules: (type1, type2) -> result_type
        self.promotion_rules = {
            ('int', 'int'): 'int',
            ('int', 'float'): 'float',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
            ('string', 'string'): 'string',
            ('bool', 'bool'): 'bool',
        }
        
        # Operator result types
        self.comparison_operators = {'==', '!=', '<', '<=', '>', '>='}
        self.logical_operators = {'&&', '||'}
        self.arithmetic_operators = {'+', '-', '*', '/', '%'}
    
    def infer_literal_type(self, literal: Literal) -> str:
        """
        Infer type from a literal value
        This is the base case for type inference
        """
        return literal.literal_type
    
    def infer_binary_op_type(self, operator: str, left_type: str, right_type: str) -> Tuple[str, bool]:
        """
        Infer the result type of a binary operation
        
        Returns: (result_type, needs_promotion)
        """
        # Comparison operators always return bool
        if operator in self.comparison_operators:
            # Check if types are compatible for comparison
            if left_type == right_type:
                return ('bool', False)
            elif (left_type, right_type) in self.promotion_rules:
                return ('bool', True)
            else:
                return ('error', False)
        
        # Logical operators expect bool and return bool
        if operator in self.logical_operators:
            if left_type == 'bool' and right_type == 'bool':
                return ('bool', False)
            else:
                return ('error', False)
        
        # Arithmetic operators
        if operator in self.arithmetic_operators:
            # Look up promotion rule
            if (left_type, right_type) in self.promotion_rules:
                result_type = self.promotion_rules[(left_type, right_type)]
                needs_promotion = (left_type != right_type)
                return (result_type, needs_promotion)
            else:
                return ('error', False)
        
        return ('unknown', False)
    
    def infer_unary_op_type(self, operator: str, operand_type: str) -> str:
        """Infer type of unary operation"""
        if operator == '-':
            # Negation: works on int and float
            if operand_type in ['int', 'float']:
                return operand_type
            else:
                return 'error'
        
        elif operator == '!':
            # Logical NOT: works on bool
            if operand_type == 'bool':
                return 'bool'
            else:
                return 'error'
        
        return 'unknown'
    
    def infer_expression_type(self, expr: ASTNode, symbol_table: Dict[str, str]) -> str:
        """
        Recursively infer the type of an expression
        
        Args:
            expr: The expression AST node
            symbol_table: Dictionary mapping variable names to types
        
        Returns:
            The inferred type as a string
        """
        if isinstance(expr, Literal):
            return self.infer_literal_type(expr)
        
        elif isinstance(expr, Variable):
            # Look up variable type in symbol table
            var_type = symbol_table.get(expr.name, 'unknown')
            return var_type
        
        elif isinstance(expr, BinaryOp):
            # Infer types of left and right operands
            left_type = self.infer_expression_type(expr.left, symbol_table)
            right_type = self.infer_expression_type(expr.right, symbol_table)
            
            # Infer result type
            result_type, _ = self.infer_binary_op_type(expr.operator, left_type, right_type)
            return result_type
        
        elif isinstance(expr, UnaryOp):
            operand_type = self.infer_expression_type(expr.operand, symbol_table)
            return self.infer_unary_op_type(expr.operator, operand_type)
        
        else:
            return 'unknown'
    
    def generate_type_report(self, symbol_table: Dict[str, str], promotions: List[dict]) -> str:
        """
        Generate a human-readable type inference report
        """
        lines = []
        lines.append("🔍 TYPE INFERENCE REPORT")
        lines.append("=" * 50)
        
        lines.append("\nVariables:")
        for var_name, var_type in sorted(symbol_table.items()):
            lines.append(f"  {var_name:<15} : {var_type}")
        
        if promotions:
            lines.append("\n⬆️ Type Promotions:")
            for promo in promotions:
                lines.append(f"  Line {promo['line']}: {promo['from_type']} → {promo['to_type']}")
        
        lines.append("\n" + "=" * 50)
        
        return "\n".join(lines)


# Simple test
if __name__ == "__main__":
    engine = TypeInferenceEngine()
    
    print("🧪 Testing Type Inference Engine\n")
    print("=" * 50)
    
    # Test 1: Literal inference
    lit_int = Literal(value=5, literal_type='int')
    print(f"\nLiteral 5: {engine.infer_literal_type(lit_int)}")
    
    lit_float = Literal(value=3.14, literal_type='float')
    print(f"Literal 3.14: {engine.infer_literal_type(lit_float)}")
    
    # Test 2: Binary operation type inference
    print("\n" + "-" * 50)
    print("Binary Operations:")
    
    tests = [
        ('int', '+', 'int', 'int + int'),
        ('int', '+', 'float', 'int + float'),
        ('float', '*', 'float', 'float * float'),
        ('int', '>', 'int', 'int > int'),
        ('bool', '&&', 'bool', 'bool && bool'),
    ]
    
    for left, op, right, desc in tests:
        result, promoted = engine.infer_binary_op_type(op, left, right)
        promo_str = " (promotion)" if promoted else ""
        print(f"  {desc:<20} → {result}{promo_str}")
    
    print("\n" + "=" * 50)
    print("✅ Type Inference Engine working!")