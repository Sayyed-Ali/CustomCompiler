"""
AST Visualizer - Creates beautiful tree diagrams
"""

from ast_nodes import *

def visualize_ast(ast):
    """
    Create visual tree of AST with proper hierarchy
    Returns string with tree structure
    """
    lines = []
    lines.append("🌳 Abstract Syntax Tree\n")
    
    # Create tree structure
    tree_lines = build_tree(ast, "", True, True)
    lines.extend(tree_lines)
    
    return "\n".join(lines)


def build_tree(node, prefix, is_last, is_root=False):
    """
    Build tree structure recursively
    """
    lines = []
    
    # Choose connector
    if is_root:
        connector = ""
    elif is_last:
        connector = "└── "
    else:
        connector = "├── "
    
    # Get node display
    display = get_node_display(node)
    lines.append(f"{prefix}{connector}{display}")
    
    # Get children
    children = get_children(node)
    
    if not children:
        return lines
    
    # Choose extension
    if is_root:
        extension = ""
    elif is_last:
        extension = "    "
    else:
        extension = "│   "
    
    # Draw children
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        child_lines = build_tree(child, prefix + extension, is_last_child, False)
        lines.extend(child_lines)
    
    return lines


def get_node_display(node):
    """Get display text for node"""
    
    if isinstance(node, Program):
        return "📦 Program"
    
    elif isinstance(node, Assignment):
        return f"📌 Assignment: {node.variable} ="
    
    elif isinstance(node, Literal):
        return f"📝 Literal: {node.value} ({node.literal_type})"
    
    elif isinstance(node, Variable):
        return f"🔤 Variable: {node.name}"
    
    elif isinstance(node, BinaryOp):
        return f"⚙️  BinaryOp: {node.operator}"
    
    elif isinstance(node, UnaryOp):
        return f"➖ UnaryOp: {node.operator}"
    
    elif isinstance(node, IfStatement):
        return "🔀 IfStatement"
    
    elif isinstance(node, WhileStatement):
        return "🔁 WhileStatement"
    
    elif isinstance(node, PrintStatement):
        return "🖨️  PrintStatement"
    
    else:
        return node.__class__.__name__


def get_children(node):
    """Get child nodes for tree"""
    
    if isinstance(node, Program):
        return node.statements
    
    elif isinstance(node, Assignment):
        return [node.expression] if node.expression else []
    
    elif isinstance(node, BinaryOp):
        children = []
        if node.left:
            children.append(node.left)
        if node.right:
            children.append(node.right)
        return children
    
    elif isinstance(node, UnaryOp):
        return [node.operand] if node.operand else []
    
    elif isinstance(node, IfStatement):
        children = []
        if node.condition:
            children.append(node.condition)
        if node.then_block:
            children.extend(node.then_block)
        if node.else_block:
            children.extend(node.else_block)
        return children
    
    elif isinstance(node, WhileStatement):
        children = []
        if node.condition:
            children.append(node.condition)
        if node.body:
            children.extend(node.body)
        return children
    
    elif isinstance(node, PrintStatement):
        return [node.expression] if node.expression else []
    
    return []