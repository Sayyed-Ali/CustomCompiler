"""
Smart Compiler - Web Interface
COMPLETE FIXED VERSION - Better errors, spell checking, AST tree
"""

import streamlit as st
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
from ast_visualizer import visualize_ast

# Page config
st.set_page_config(
    page_title="Smart Compiler",
    page_icon="🔧",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1E88E5;
    text-align: center;
    padding: 1rem;
    font-weight: bold;
}
.success-msg {
    background: #d4edda;
    border-left: 4px solid #28a745;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}
.error-msg {
    background: #f8d7da;
    border-left: 4px solid #dc3545;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}
.code-block {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 1.5rem;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 0.95rem;
    line-height: 1.8;
    overflow-x: auto;
    white-space: pre;
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'compiled' not in st.session_state:
    st.session_state.compiled = False
if 'code' not in st.session_state:
    st.session_state.code = """x = 5
y = 10
z = x + y
print(z)"""

# Header
st.markdown('<div class="main-header">🔧 Smart Compiler</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Examples")
    
    examples = {
        "✅ Basic (Correct)": "x = 5\ny = 10\nz = x + y\nprint(z)",
        "❌ Wrong Spelling": "x = 5\nwhiel (x < 10) {\n    x = x + 1\n    printt(x)\n}",
        "❌ Syntax Error": "x = 5\ny = 10\nz = x + y\nprintt(z)",
        "✅ If-Else": 'x = 15\nif (x > 10) {\n    print(x)\n} else {\n    print(0)\n}',
        "✅ While Loop": "count = 0\nwhile (count < 3) {\n    count = count + 1\n    print(count)\n}",
        "✅ Type Inference": "x = 5\ny = 3.14\nz = x + y\nprint(z)",
        "✅ Complete Program": 'x = 5\ny = 3.14\nz = x + y\n\nif (z > 5.0) {\n    print(z)\n}\n\ncount = 0\nwhile (count < 3) {\n    count = count + 1\n    print(count)\n}'
    }
    
    ex_choice = st.selectbox("Choose Example:", list(examples.keys()))
    if st.button("📥 Load Example"):
        st.session_state.code = examples[ex_choice]
        st.session_state.compiled = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ ML Features")
    st.success("🤖 Spell Checking")
    st.success("🧠 Type Inference")
    
    st.markdown("---")
    st.markdown("**Team Code Sages**")
    st.caption("CD-VI-T079-2026")

# Main area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Source Code")
    code_input = st.text_area(
        "",
        value=st.session_state.code,
        height=300,
        key="editor",
        help="Write your code here"
    )
    st.session_state.code = code_input
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("🚀 Compile", type="primary", use_container_width=True):
            st.session_state.compiled = True
            st.rerun()
    with col_btn2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.code = ""
            st.session_state.compiled = False
            st.rerun()

with col2:
    st.markdown("### 📊 Quick Stats")
    
    if st.session_state.compiled and code_input.strip():
        try:
            # Phase 1: Lexer
            lexer = Lexer(code_input)
            tokens = lexer.tokenize()
            
            # Check for lexer errors
            if lexer.errors:
                st.markdown('<div class="error-msg"><b>❌ Lexical Errors</b></div>', unsafe_allow_html=True)
                for err in lexer.errors:
                    st.error(f"Line {err['line']}: {err['message']}")
                st.session_state.result = {'success': False}
            else:
                # Phase 2: Parser
                parser = Parser(tokens)
                ast = parser.parse()
                
                if not ast or parser.errors:
                    st.markdown('<div class="error-msg"><b>❌ Syntax Errors</b></div>', unsafe_allow_html=True)
                    
                    # Show better error messages
                    if parser.errors:
                        for err in parser.errors:
                            # Make error message clearer
                            msg = err.get('message', 'Unknown error')
                            line = err.get('line', '?')
                            
                            # Simplify confusing messages
                            if 'Expected ASSIGN but got' in msg:
                                msg = f"Missing '=' assignment operator"
                            elif 'LPAREN' in msg or 'RPAREN' in msg:
                                msg = f"Missing parenthesis '(' or ')'"
                            elif 'LBRACE' in msg or 'RBRACE' in msg:
                                msg = f"Missing curly brace '{{' or '}}'"
                            
                            st.error(f"**Line {line}:** {msg}")
                    
                    st.session_state.result = {'success': False}
                else:
                    # Phase 3: Semantic
                    analyzer = SemanticAnalyzer()
                    success = analyzer.analyze(ast)
                    
                    if not success:
                        st.markdown('<div class="error-msg"><b>❌ Semantic Errors</b></div>', unsafe_allow_html=True)
                        for err in analyzer.errors:
                            st.error(f"Line {err.get('line', '?')}: {err.get('message', 'Unknown error')}")
                        st.session_state.result = {'success': False}
                    else:
                        # Phase 4: Code Generation
                        codegen = CodeGenerator()
                        tac = codegen.generate(ast)
                        
                        st.markdown('<div class="success-msg"><b>✅ Compilation Successful!</b></div>', unsafe_allow_html=True)
                        
                        # Stats
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Tokens", len(tokens))
                        c2.metric("Variables", len(analyzer.symbol_table.symbols))
                        c3.metric("TAC Lines", len(tac))
                        
                        # Save results
                        st.session_state.result = {
                            'tokens': tokens,
                            'ast': ast,
                            'analyzer': analyzer,
                            'codegen': codegen,
                            'success': True
                        }
        
        except Exception as e:
            st.markdown('<div class="error-msg"><b>❌ Compilation Error</b></div>', unsafe_allow_html=True)
            st.error(str(e))
            
            # Show detailed error for debugging
            with st.expander("🔍 Debug Info"):
                import traceback
                st.code(traceback.format_exc())
            
            st.session_state.result = {'success': False}
    else:
        st.info("👆 Enter code and click Compile")

# Results tabs
if st.session_state.compiled and 'result' in st.session_state and st.session_state.result.get('success'):
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔤 Tokens", "🌳 AST", "🧠 Semantic", "💻 TAC"])
    
    with tab1:
        st.markdown("### Phase 1: Lexical Analysis")
        
        # ✅ SPELL CHECKER - Check ALL tokens
        spell_warnings = []
        for token in st.session_state.result['tokens']:
            if hasattr(token, 'spell_warning') and token.spell_warning:
                spell_warnings.append(token.spell_warning)
        
        if spell_warnings:
            st.markdown("#### 🤖 ML Feature #1: Spell Checker Detected Typos!")
            
            for warning in spell_warnings:
                st.warning(
                    f"**Possible typo on line {warning.get('line', '?')}:**\n\n"
                    f"• You wrote: `{warning['original']}`\n\n"
                    f"• Did you mean: `{warning['suggestion']}`?\n\n"
                    f"• Confidence: **{warning['confidence']}%**\n\n"
                    f"• Edit distance: {warning['distance']}"
                )
        else:
            st.success("✅ No spelling errors detected!")
        
        st.markdown("---")
        st.markdown("**Token Stream:**")
        
        # Token table
        token_data = []
        for i, tok in enumerate(st.session_state.result['tokens'][:25], 1):
            # Add warning indicator if spell issue
            warning = "⚠️" if hasattr(tok, 'spell_warning') and tok.spell_warning else ""
            
            token_data.append({
                "#": i,
                "Type": tok.type.name,
                "Value": str(tok.value),
                "Line": tok.line,
                "⚠️": warning
            })
        
        st.dataframe(token_data, use_container_width=True, hide_index=True)
        
        if len(st.session_state.result['tokens']) > 25:
            st.caption(f"... and {len(st.session_state.result['tokens']) - 25} more tokens")
    
    with tab2:
        st.markdown("### Phase 2: Syntax Analysis")
        
        # Show tree
        tree_str = visualize_ast(st.session_state.result['ast'])
        
        st.markdown(f'<div class="code-block">{tree_str}</div>', unsafe_allow_html=True)
        
        st.info("💡 **Tree shows program structure:** Each node represents a language construct")
    
    with tab3:
        st.markdown("### Phase 3: Semantic Analysis")
        
        st.markdown("**Symbol Table:**")
        
        sym_data = []
        for name, sym in st.session_state.result['analyzer'].symbol_table.symbols.items():
            sym_data.append({
                "Variable": name,
                "Type": sym.type,
                "Declared at Line": sym.line
            })
        
        if sym_data:
            st.dataframe(sym_data, use_container_width=True, hide_index=True)
        else:
            st.info("No variables declared yet")
        
        # Type promotions
        if st.session_state.result['analyzer'].type_promotions:
            st.markdown("---")
            st.markdown("#### 🧠 ML Feature #2: Type Inference Active!")
            st.info("**Automatic type promotions detected:**")
            for p in st.session_state.result['analyzer'].type_promotions:
                st.success(
                    f"• **Line {p['line']}:** Variable `{p['variable']}` promoted\n\n"
                    f"  From: `{p['from_type']}` → To: `{p['to_type']}`"
                )
        else:
            st.success("✅ No type promotions needed - all types match!")
    
    with tab4:
        st.markdown("### Phase 4: Code Generation")
        
        st.markdown("**Three-Address Code (TAC):**")
        
        # Vertical TAC display
        tac_lines = []
        for i, instr in enumerate(st.session_state.result['codegen'].instructions, 1):
            tac_lines.append(f"{i:3d}:  {str(instr)}")
        
        tac_output = "\n".join(tac_lines)
        st.markdown(f'<div class="code-block">{tac_output}</div>', unsafe_allow_html=True)
        
        st.download_button(
            "📥 Download TAC File",
            data=tac_output,
            file_name="output.tac",
            mime="text/plain"
        )
        
        # Stats
        st.markdown("---")
        st.markdown("**Code Generation Statistics:**")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Instructions", len(st.session_state.result['codegen'].instructions))
        col_b.metric("Temp Variables", st.session_state.result['codegen'].temp_counter)
        col_c.metric("Labels", st.session_state.result['codegen'].label_counter)

# Footer
st.markdown("---")
st.caption("Smart Compiler • Team Code Sages • CD-VI-T079-2026 • Graphic Era University")