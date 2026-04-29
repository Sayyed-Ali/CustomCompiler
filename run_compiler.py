"""
Complete Compiler Demo - Run all 4 phases on source code
Usage: python3 run_compiler.py
"""

import sys
sys.path.insert(0, 'src')

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator
from ast_nodes import print_ast


def run_compiler_demo():
    """Run complete compilation and show all phases"""
    
    # Source code to compile
    code = """x = 5
y = 3.14
z = x + y

if (z > 5.0) {
    print(z)
} else {
    print(0)
}

count = 0
while (count < 3) {
    count = count + 1
    print(count)
}"""
    
    print("\n" + "="*70)
    print("SMART COMPILER - ALL 4 PHASES DEMONSTRATION")
    print("="*70)
    
    # Show source code
    print("\n📝 SOURCE CODE:")
    print("-"*70)
    print(code)
    print("-"*70)
    
    # PHASE 1: LEXICAL ANALYSIS
    print("\n" + "="*70)
    print("PHASE 1: LEXICAL ANALYSIS")
    print("="*70)
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\n✓ Generated {len(tokens)} tokens\n")
    print("First 15 tokens:")
    for i, token in enumerate(tokens[:15], 1):
        print(f"  {i:2d}. {token}")
    
    if len(tokens) > 15:
        print(f"\n  ... and {len(tokens)-15} more tokens")
    
    print("\n✅ PHASE 1 COMPLETE!")
    
    # PHASE 2: SYNTAX ANALYSIS
    print("\n" + "="*70)
    print("PHASE 2: SYNTAX ANALYSIS (Parser)")
    print("="*70)
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    if not ast:
        print("\n❌ PARSING FAILED!")
        for error in parser.errors:
            print(f"  Error: {error['message']}")
        return False
    
    print(f"\n✓ Built Abstract Syntax Tree with {len(ast.statements)} statements\n")
    print("AST Structure:")
    print_ast(ast, indent=2)
    
    print("\n✅ PHASE 2 COMPLETE!")
    
    # PHASE 3: SEMANTIC ANALYSIS
    print("\n" + "="*70)
    print("PHASE 3: SEMANTIC ANALYSIS (Type Inference)")
    print("="*70)
    
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    if not success:
        print("\n❌ SEMANTIC ANALYSIS FAILED!")
        print(analyzer.generate_report())
        return False
    
    print(analyzer.generate_report())
    
    print("\n💡 ML Feature #2 in action:")
    print("   Type inference automatically determined all variable types!")
    print("   No explicit type declarations needed!")
    
    print("\n✅ PHASE 3 COMPLETE!")
    
    # PHASE 4: CODE GENERATION
    print("\n" + "="*70)
    print("PHASE 4: CODE GENERATION")
    print("="*70)
    
    codegen = CodeGenerator()
    tac = codegen.generate(ast)
    
    print(f"\n✓ Generated {len(tac)} TAC instructions\n")
    print("Three-Address Code (TAC):")
    print("-"*70)
    print(codegen.get_code())
    print("-"*70)
    
    print("\n✅ PHASE 4 COMPLETE!")
    
    # FINAL SUMMARY
    print("\n" + "="*70)
    print("🎉 COMPILATION SUCCESSFUL!")
    print("="*70)
    
    print(f"""
📊 COMPILATION STATISTICS:
   • Input Lines:        {len(code.split(chr(10)))}
   • Tokens Generated:   {len(tokens)}
   • AST Statements:     {len(ast.statements)}
   • Variables Tracked:  {len(analyzer.symbol_table.symbols)}
   • TAC Instructions:   {len(tac)}
   • Temp Variables:     {codegen.temp_counter}
   • Labels Created:     {codegen.label_counter}
   • Errors Found:       {len(analyzer.errors)}

🎯 ALL 4 PHASES EXECUTED SUCCESSFULLY!
""")
    
    return True


if __name__ == "__main__":
    print("\n🚀 Starting Compiler...")
    success = run_compiler_demo()
    
    if success:
        print("\n✅ Demo completed successfully!\n")
    else:
        print("\n❌ Demo failed with errors.\n")
        sys.exit(1)
