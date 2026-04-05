# Smart Compiler for Mini Programming Language

A complete compiler implementation with ML-enhanced features for intelligent error detection and automatic type inference.

## 🎯 Project Overview

This is an educational compiler built from scratch in Python that demonstrates all four phases of compilation while incorporating machine learning-inspired features to improve developer experience. Developed as part of the Compiler Design course (TCS-601) at Graphic Era University.

**Team:** Code Sages (CD-VI-T079-2026)  
**Members:** Mohd Ali, Khushi Vaish, Divyanshu Yadav, Riya Deo

## ✨ Key Features

### Core Compilation Pipeline
- **Phase 1: Lexical Analysis** - Tokenization with intelligent keyword spell checking
- **Phase 2: Syntax Analysis** - Recursive descent parser with proper operator precedence
- **Phase 3: Semantic Analysis** - Symbol table management with automatic type inference
- **Phase 4: Code Generation** - Three-Address Code (TAC) output

### ML-Powered Features
1. **Intelligent Spell Correction** (Levenshtein Distance Algorithm)
   - Detects keyword typos: `whiel` → suggests `while` with 60% confidence
   - Uses edit distance calculation for smart suggestions

2. **Automatic Type Inference** (Constraint-based Propagation)
   - No need for explicit type declarations
   - Infers types from literals: `x = 5` → x is `int`
   - Propagates through expressions: `z = x + y` where x:int, y:float → z:float
   - Applies type promotion rules automatically

### User-Friendly Error Messages
- Line and column numbers for all errors
- Contextual suggestions for fixes
- Color-coded output for better readability

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://gitlab.com/MohdAlii/custom-compiler.git
cd custom-compiler

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Compiler

#### Option 1: Web Interface (Recommended)
```bash
streamlit run ui/app.py
```
Then open your browser to `http://localhost:8501`

#### Option 2: Command Line
```bash
# Compile a single file
python ui/cli.py examples/example1.txt

# With output file
python ui/cli.py examples/example1.txt -o output.tac
```

#### Option 3: Python API
```python
from src.lexer import Lexer
from src.parser import Parser
from src.semantic import SemanticAnalyzer
from src.codegen import CodeGenerator

# Your code
code = """
x = 5
y = 10
z = x + y
print(z)
"""

# Compile
lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

codegen = CodeGenerator()
tac = codegen.generate(ast)

# View output
print(codegen.get_code())
```

## 📂 Project Structure

```
mini-compiler/
├── src/
│   ├── lexer.py              # Tokenizer
│   ├── parser.py             # Recursive descent parser
│   ├── semantic.py           # Semantic analyzer
│   ├── codegen.py            # TAC generator
│   ├── spell_checker.py      # ML Feature #1
│   ├── type_inference.py     # ML Feature #2
│   ├── symbol_table.py       # Variable tracking
│   ├── ast_nodes.py          # AST node definitions
│   └── error_reporter.py     # Error formatting
├── tests/
│   ├── test_lexer.py         # 10 tests
│   ├── test_parser.py        # 12 tests
│   ├── test_semantic.py      # 12 tests
│   └── test_codegen.py       # 10 tests
├── ui/
│   ├── app.py                # Streamlit web UI
│   └── cli.py                # Command-line interface
├── examples/
│   ├── example1.txt          # Sample programs
│   └── example2.txt
├── requirements.txt          # Python dependencies
└── README.md
```

## 🧪 Running Tests
```bash
# Run all tests
pytest tests/

# Run specific phase tests
pytest tests/test_lexer.py
pytest tests/test_parser.py
pytest tests/test_semantic.py
pytest tests/test_codegen.py

# Run with verbose output
pytest -v tests/
```

**Test Coverage:** 44/44 tests passing (100%)

## 📖 Language Syntax

### Supported Types
- `int` - Integer numbers
- `float` - Floating-point numbers
- `string` - Text strings
- `bool` - Boolean values (true/false)

### Example Program
```python
# Variables (type inference!)
x = 5
y = 3.14
name = "Alice"
valid = true

# Arithmetic
z = x + y * 2

# Conditionals
if (z > 10.0) {
    print(z)
} else {
    print(0)
}

# Loops
count = 0
while (count < 3) {
    count = count + 1
    print(count)
}
```

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Logical: `&&`, `||`, `!`
- Assignment: `=`

## 🔬 Technical Details

### Algorithms Used

**Levenshtein Distance (Spell Checker)**
- Dynamic programming approach
- O(m×n) time complexity
- Calculates minimum edit operations between strings
- Used in Google Search, spell checkers, DNA sequencing

**Type Inference Engine**
- Literal-based type deduction
- Constraint propagation through AST
- Type promotion rules (int → float)
- Similar to TypeScript and Rust implementations

### Architecture
```
Source Code
↓
[Lexer] → Tokens
↓
[Parser] → Abstract Syntax Tree (AST)
↓
[Semantic Analyzer] → Validated AST + Symbol Table
↓
[Code Generator] → Three-Address Code (TAC)
```

## 📊 Project Statistics

- **Total Lines of Code:** ~1,800
- **Test Cases:** 44 (100% passing)
- **Phases Completed:** 4/4
- **ML Features:** 2
- **Development Time:** 6 weeks
- **Team Size:** 4 members

## 🎓 Educational Value

This project demonstrates:
- Complete compiler construction from scratch
- Lexical analysis and tokenization
- Context-free grammar parsing
- Symbol table management
- Type systems and inference
- Intermediate code generation
- Software testing best practices
- Team collaboration and version control

## 🤝 Contributing

This is an academic project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is developed for educational purposes as part of the Compiler Design course at Graphic Era University.

## 👥 Team

**Team Code Sages - CD-VI-T079-2026**

- **Mohd Ali** (Team Lead) - 230112026
- **Khushi Vaish** - 230221211
- **Divyanshu Yadav** - 230211545
- **Riya Deo** - 23012503

**Course:** Compiler Design (TCS-601)  
**Semester:** VI (2026)  
**Institution:** Graphic Era University

## 📚 References

- Aho, A.V., et al. - *Compilers: Principles, Techniques, and Tools* (Dragon Book)
- Levenshtein, V.I. (1966) - Binary codes capable of correcting deletions
- Course lectures and materials - Compiler Design, Semester VI

## 🙏 Acknowledgments

Special thanks to our course instructor and mentors for guidance throughout this project.

---

**Status:** ✅ All 4 phases complete | 44/44 tests passing | Ready for deployment
