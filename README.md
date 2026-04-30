# Smart Compiler for Mini Programming Language

A complete compiler implementation for a custom mini programming language, built from scratch in Python with machine learning-enhanced features for intelligent error detection and automatic type inference.

## Project Information

**Course:** Compiler Design (TCS-601)
**Team Name:** Code Sages
**Team ID:** CD-VI-T079-2026
**Institution:** Graphic Era University, Dehradun
**Semester:** VI (2026)

## Team Members

| Name | Student ID | Role |
|------|-----------|------|
| Mohd Ali | 230112026 | Team Lead |
| Khushi Vaish | 230221211 | Member |
| Divyanshu Yadav | 230211545 | Member |
| Riya Deo | 230121503 | Member |

## Overview

This project implements a complete four-phase compiler for a custom mini programming language. The compiler processes source code through lexical analysis, syntax analysis, semantic analysis, and code generation phases, producing Three-Address Code (TAC) as output. Two machine learning-inspired features have been integrated to enhance the developer experience: intelligent keyword spell correction and automatic type inference.

## Features

### Core Compilation Phases

1. **Lexical Analysis** - Converts source code into a stream of tokens with position tracking
2. **Syntax Analysis** - Constructs an Abstract Syntax Tree using recursive descent parsing
3. **Semantic Analysis** - Validates types, manages symbol table, and performs type inference
4. **Code Generation** - Produces optimized Three-Address Code with temporary variables and labels

### Machine Learning Features

1. **Intelligent Spell Correction**
   - Uses Levenshtein Distance algorithm
   - Detects keyword typos (e.g., "whiel" → "while", "printt" → "print")
   - Provides confidence scoring for suggestions
   - Threshold-based filtering to reduce false positives

2. **Automatic Type Inference**
   - Constraint-based type propagation
   - Eliminates need for explicit type declarations
   - Handles type promotion rules (e.g., int + float → float)
   - Supports literal type deduction

### User Interfaces

- **Web Interface** - Interactive Streamlit-based UI for code compilation and visualization
- **Command Line Interface** - Terminal-based compiler for batch processing

## Language Syntax

### Supported Data Types

- `int` - Integer numbers
- `float` - Floating-point numbers
- `string` - Text strings
- `bool` - Boolean values

### Supported Operations

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Logical: `&&`, `||`, `!`
- Assignment: `=`

### Control Structures

- Conditional statements: `if-else`
- Iterative statements: `while`
- Output statements: `print`

### Example Program

```
x = 5
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
}
```

## Project Structure

```
mini-compiler/
├── src/
│   ├── lexer.py              Lexical analyzer
│   ├── parser.py             Syntax analyzer
│   ├── semantic.py           Semantic analyzer
│   ├── codegen.py            Code generator
│   ├── ast_nodes.py          AST node definitions
│   ├── ast_visualizer.py     Tree visualization
│   ├── spell_checker.py      ML Feature 1: Spell checking
│   ├── type_inference.py     ML Feature 2: Type inference
│   ├── symbol_table.py       Symbol table management
│   └── error_reporter.py     Error formatting
├── tests/
│   ├── test_lexer.py         Lexer test suite
│   ├── test_parser.py        Parser test suite
│   ├── test_semantic.py      Semantic test suite
│   └── test_codegen.py       Code generator test suite
├── ui/
│   ├── app.py                Streamlit web interface
│   └── cli.py                Command line interface
├── examples/
│   ├── example1.txt          Sample program
│   └── example2.txt          Sample program
├── requirements.txt          Python dependencies
└── README.md                 Project documentation
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

Clone the repository:

```
git clone https://github.com/Sayyed-Ali/CustomCompiler.git
cd CustomCompiler
```

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Usage

### Running the Web Interface

Launch the Streamlit-based web interface:

```
streamlit run ui/app.py
```

The application will open in your default browser at `http://localhost:8501`.

### Running the Command Line Interface

Compile a source file:

```
python ui/cli.py examples/example1.txt
```

Save Three-Address Code to a file:

```
python ui/cli.py examples/example1.txt -o output.tac
```

Enable verbose output:

```
python ui/cli.py examples/example1.txt -v
```

### Running Tests

Execute all test suites:

```
pytest tests/
```

Run individual phase tests:

```
python tests/test_lexer.py
python tests/test_parser.py
python tests/test_semantic.py
python tests/test_codegen.py
```

Run tests with verbose output:

```
pytest -v tests/
```

## Compilation Pipeline

```
Source Code
    |
    v
[Lexer] -> Token Stream
    |
    v
[Parser] -> Abstract Syntax Tree
    |
    v
[Semantic Analyzer] -> Validated AST + Symbol Table
    |
    v
[Code Generator] -> Three-Address Code
```

## Technical Details

### Algorithms Implemented

1. **Levenshtein Distance** - Dynamic programming approach with O(m*n) time complexity for spell checking
2. **Recursive Descent Parser** - Handles operator precedence through hierarchical function calls
3. **Type Inference Engine** - Constraint-based propagation with promotion rules
4. **Post-Order AST Traversal** - Used for code generation with temporary variable management

### Implementation Approach

The compiler is implemented entirely from scratch in Python without using parser generators such as PLY or ANTLR. This design decision was made to provide deeper understanding of compiler construction principles and allow for full control over each phase.

## Testing

The project includes 44 comprehensive test cases covering all compilation phases:

| Phase | Test Count | Coverage |
|-------|-----------|----------|
| Lexer | 10 | Tokenization, operators, keywords, strings, comments, spell checker |
| Parser | 12 | Expressions, precedence, parentheses, control flow, operators |
| Semantic | 12 | Type inference, propagation, promotions, validation |
| Code Generation | 10 | Assignments, expressions, control flow, complete programs |

All 44 tests pass successfully.

## Statistics

- Total Lines of Code: Approximately 1,800
- Number of Modules: 13
- Test Cases: 44 (100% passing)
- Compilation Phases: 4
- Machine Learning Features: 2

## Future Scope

The following enhancements are planned for future iterations of this project:

1. **Function Support** - Add user-defined functions with parameters and return values, including recursion support and proper scope management

2. **Advanced Type System** - Implement arrays, dictionaries, and user-defined data structures with comprehensive type checking

3. **Code Optimization** - Add intermediate code optimization techniques such as constant folding, dead code elimination, and common subexpression elimination

## References

1. Aho, A.V., Lam, M.S., Sethi, R., Ullman, J.D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd Edition). Addison-Wesley.

2. Levenshtein, V.I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707-710.

3. Course materials and lectures from Compiler Design (TCS-601), Semester VI, Graphic Era University.

## License

This project is developed for educational purposes as part of the Compiler Design course at Graphic Era University.

## Contact

For questions or feedback regarding this project, please contact the team lead at qadriali54@gmail.com.