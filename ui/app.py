"""
UI- Smart Compiler
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Setup path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / 'src'
sys.path.insert(0, str(src_dir))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator
from ast_visualizer import visualize_ast

# Page config
st.set_page_config(page_title="Smart Compiler", page_icon="🔧", layout="wide")

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
.success-box {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.error-box {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.warning-box {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
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

# Session
if 'compiled' not in st.session_state:
    st.session_state.compiled = False
if 'code' not in st.session_state:
    st.session_state.code = "x = 5\ny = 10\nz = x + y\nprint(z)"

# Header
st.markdown('<div class="main-header">🔧 Smart Compiler</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Examples")
    
    examples = {
        "✅ Correct Code": "x = 5\ny = 10\nz = x + y\nprint(z)",
        "❌ Typo: printt": "x = 5\ny = 10\nz = x + y\nprintt(z)",
        "❌ Typo: whiel": "x = 5\nwhiel (x < 10) {\n    x = x + 1\n    print(x)\n}",
        "✅ If-Else": "x = 15\nif (x > 10) {\n    print(x)\n} else {\n    print(0)\n}",
        "✅ Type Inference": "x = 5\ny = 3.14\nz = x + y\nprint(z)"
    }
    
    choice = st.selectbox("Choose:", list(examples.keys()))
    if st.button("📥 Load"):
        st.session_state.code = examples[choice]
        st.session_state.compiled = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🤖 ML Features")
    st.success("✓ Spell Checking")
    st.success("✓ Type Inference")
    
    st.markdown("---")
    st.caption("**Team Code Sages**")
    st.caption("CD-VI-T079-2026")

# Main
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Source Code")
    code_input = st.text_area("", value=st.session_state.code, height=300, key="editor")
    st.session_state.code = code_input
    
    if st.button("🚀 Compile", type="primary", use_container_width=True):
        st.session_state.compiled = True
        st.rerun()

with col2:
    st.markdown("### 📊 Status")
    
    if st.session_state.compiled and code_input.strip():
        try:
            # Phase 1: Lexer
            lexer = Lexer(code_input)
            tokens = lexer.tokenize()
            
            # Check for spell errors
            spell_errors = []
            for token in tokens:
                if hasattr(token, 'spell_warning') and token.spell_warning:
                    spell_errors.append(token.spell_warning)
            
            # If spell errors, stop here
            if spell_errors:
                st.markdown('<div class="warning-box"><b>🤖 ML Spell Checker Detected Typos!</b></div>', unsafe_allow_html=True)
                
                for err in spell_errors:
                    st.error(
                        f"**Line {err.get('line', '?')}:** "
                        f"Unknown identifier `{err['original']}`\n\n"
                        f"💡 **Did you mean `{err['suggestion']}`?**\n\n"
                        f"Confidence: {err['confidence']}%"
                    )
                
                st.warning("⚠️ Fix spelling errors to continue")
                st.session_state.result = None
            
            else:
                # Phase 2: Parser
                parser = Parser(tokens)
                ast = parser.parse()
                
                if not ast or parser.errors:
                    st.markdown('<div class="error-box"><b>❌ Syntax Errors</b></div>', unsafe_allow_html=True)
                    for err in parser.errors:
                        st.error(f"Line {err.get('line', '?')}: {err.get('message')}")
                    st.session_state.result = None
                
                else:
                    # Phase 3: Semantic
                    analyzer = SemanticAnalyzer()
                    success = analyzer.analyze(ast)
                    
                    if not success:
                        st.markdown('<div class="error-box"><b>❌ Semantic Errors</b></div>', unsafe_allow_html=True)
                        for err in analyzer.errors:
                            st.error(f"Line {err.get('line', '?')}: {err.get('message')}")
                        st.session_state.result = None
                    
                    else:
                        # Phase 4: CodeGen
                        codegen = CodeGenerator()
                        codegen.generate(ast)
                        
                        st.markdown('<div class="success-box"><b>✅ Compilation Successful!</b></div>', unsafe_allow_html=True)
                        
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Tokens", len(tokens))
                        c2.metric("Variables", len(analyzer.symbol_table.symbols))
                        c3.metric("TAC Lines", len(codegen.instructions))
                        
                        # SAVE RESULTS
                        st.session_state.result = {
                            'tokens': tokens,
                            'ast': ast,
                            'analyzer': analyzer,
                            'codegen': codegen
                        }
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            with st.expander("Debug Info"):
                import traceback
                st.code(traceback.format_exc())
            st.session_state.result = None
    else:
        st.info("👆 Enter code and click Compile")

# Results - ONLY if result exists
if st.session_state.compiled and st.session_state.get('result'):
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔤 Tokens", "🌳 AST", "🧠 Semantic", "💻 TAC"])
    
    with tab1:
        st.markdown("### Phase 1: Lexical Analysis")
        
        token_data = []
        for i, tok in enumerate(st.session_state.result['tokens'][:20], 1):
            token_data.append({
                "#": i,
                "Type": tok.type.name,
                "Value": str(tok.value),
                "Line": tok.line
            })
        
        st.dataframe(token_data, use_container_width=True, hide_index=True)
        
        if len(st.session_state.result['tokens']) > 20:
            st.caption(f"... and {len(st.session_state.result['tokens']) - 20} more tokens")
    
    with tab2:
        st.markdown("### Phase 2: Syntax Analysis")
        
        tree = visualize_ast(st.session_state.result['ast'])
        st.markdown(f'<div class="code-block">{tree}</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Phase 3: Semantic Analysis")
        
        st.markdown("**Symbol Table:**")
        
        # Get symbols
        symbols = st.session_state.result['analyzer'].symbol_table.symbols
        
        if symbols:
            sym_data = []
            for name, sym in symbols.items():
                sym_data.append({
                    "Variable": name,
                    "Type": sym.type,
                    "Line": sym.line
                })
            
            st.dataframe(sym_data, use_container_width=True, hide_index=True)
        else:
            st.info("No variables in this program")
        
        # Type promotions
        promotions = st.session_state.result['analyzer'].type_promotions
        
        if promotions:
            st.markdown("---")
            st.info("🧠 **ML Feature #2: Type Inference**")
            for p in promotions:
                st.success(f"Line {p['line']}: `{p['variable']}` promoted from `{p['from_type']}` to `{p['to_type']}`")
        else:
            st.success("✅ No type promotions needed")
    
    with tab4:
        st.markdown("### Phase 4: Code Generation")
        
        st.markdown("**Three-Address Code:**")
        
        # Get instructions
        instructions = st.session_state.result['codegen'].instructions
        
        if instructions:
            # Build TAC display
            tac_lines = []
            for i, instr in enumerate(instructions, 1):
                tac_lines.append(f"{i:3d}:  {str(instr)}")
            
            tac_output = "\n".join(tac_lines)
            st.markdown(f'<div class="code-block">{tac_output}</div>', unsafe_allow_html=True)
            
            # Download
            st.download_button(
                "📥 Download TAC",
                data=tac_output,
                file_name="output.tac",
                mime="text/plain"
            )
            
            # Stats
            st.markdown("---")
            st.markdown("**Code Generation Stats:**")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Instructions", len(instructions))
            col_b.metric("Temp Variables", st.session_state.result['codegen'].temp_counter)
            col_c.metric("Labels", st.session_state.result['codegen'].label_counter)
        else:
            st.warning("No TAC generated")

st.markdown("---")
st.caption("Smart Compiler • Team Code Sages • CD-VI-T079-2026")