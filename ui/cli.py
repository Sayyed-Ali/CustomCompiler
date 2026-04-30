#!/usr/bin/env python3
"""
Smart Compiler - CLI Tool
"""

import sys
import os
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / 'src'
sys.path.insert(0, str(src_dir))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

def compile_file(filepath, output=None, verbose=False):
    """Compile source file"""
    
    # Read file
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f" File not found: {filepath}")
        return False
    
    if verbose:
        print(f"\n{'='*60}")
        print(" SMART COMPILER")
        print(f"{'='*60}\n")
        print("Source:")
        print(code)
        print()
    
    # Compile
    try:
        # Phase 1: Lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        if verbose:
            print(f"✓ Lexer: {len(tokens)} tokens")
        
        # Phase 2: Parser
        parser = Parser(tokens)
        ast = parser.parse()
        
        if not ast:
            print("\n Parse errors:")
            for err in parser.errors:
                print(f"  {err.get('message', 'Unknown error')}")
            return False
        
        if verbose:
            print(f"✓ Parser: {len(ast.statements)} statements")
        
        # Phase 3: Semantic
        analyzer = SemanticAnalyzer()
        if not analyzer.analyze(ast):
            print("\n Semantic errors:")
            for err in analyzer.errors:
                print(f"  {err.get('message', 'Unknown error')}")
            return False
        
        if verbose:
            print(f"✓ Semantic: {len(analyzer.symbol_table.symbols)} variables")
        
        # Phase 4: Code Gen
        codegen = CodeGenerator()
        codegen.generate(ast)
        
        if verbose:
            print(f"✓ CodeGen: {len(codegen.instructions)} instructions")
        
        # Output TAC
        tac = codegen.get_code()
        
        if output:
            with open(output, 'w') as f:
                f.write(tac)
            print(f"\n TAC saved to: {output}")
        else:
            print("\nThree-Address Code:")
            print("-" * 60)
            print(tac)
            print("-" * 60)
        
        if verbose:
            print(f"\n Compilation successful!")
        
        return True
    
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Smart Compiler - Compile mini language programs"
    )
    parser.add_argument('file', help='Source file to compile')
    parser.add_argument('-o', '--output', help='Output TAC file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    success = compile_file(args.file, args.output, args.verbose)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()