"""
Symbol Table
Tracks variables, their types, and scopes
"""

from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class Symbol:
    """Represents a symbol (variable) in the symbol table"""
    name: str
    type: str  # 'int', 'float', 'string', 'bool', 'unknown'
    line: int
    column: int
    scope: str = "global"
    initialized: bool = True


class SymbolTable:
    """
    Symbol table for tracking variables and their types
    Supports basic scope management
    """
    
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.scopes: List[str] = ["global"]
        self.current_scope = "global"
    
    def enter_scope(self, scope_name: str):
        """Enter a new scope (for if/while blocks)"""
        self.scopes.append(scope_name)
        self.current_scope = scope_name
    
    def exit_scope(self):
        """Exit current scope"""
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope = self.scopes[-1]
    
    def add_symbol(self, name: str, symbol_type: str, line: int, column: int) -> bool:
        """
        Add a symbol to the table
        Returns True if successful, False if already exists
        """
        # For simplicity, we're using global scope for all variables
        # A more advanced implementation would track local scopes
        
        if name in self.symbols:
            # Variable already declared
            return False
        
        self.symbols[name] = Symbol(
            name=name,
            type=symbol_type,
            line=line,
            column=column,
            scope=self.current_scope
        )
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol by name"""
        return self.symbols.get(name)
    
    def update_type(self, name: str, new_type: str) -> bool:
        """Update the type of an existing symbol"""
        if name not in self.symbols:
            return False
        
        self.symbols[name].type = new_type
        return True
    
    def get_all_symbols(self) -> List[Symbol]:
        """Get all symbols in the table"""
        return list(self.symbols.values())
    
    def __repr__(self):
        """String representation for debugging"""
        lines = ["Symbol Table:"]
        lines.append(f"{'Name':<15} {'Type':<10} {'Scope':<10} {'Line':<5}")
        lines.append("-" * 45)
        
        for symbol in self.symbols.values():
            lines.append(f"{symbol.name:<15} {symbol.type:<10} {symbol.scope:<10} {symbol.line:<5}")
        
        return "\n".join(lines)


# Simple test
if __name__ == "__main__":
    st = SymbolTable()
    
    st.add_symbol("x", "int", 1, 1)
    st.add_symbol("y", "float", 2, 1)
    st.add_symbol("name", "string", 3, 1)
    
    print(st)
    print()
    
    # Lookup
    x_symbol = st.lookup("x")
    print(f"Lookup 'x': {x_symbol}")
    
    # Update type
    st.update_type("x", "float")
    print(f"\nAfter updating x to float:")
    print(st)