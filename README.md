# Mini Langauge Compiler

A smart compiler for a custom mini programming langauge with ML-powered features.

## Features

- 4-phase compilation (Lexical -> Syntax -> Semantic -> Code Generation)
- Intelligent keyword spell correction using Levenshtein Distance
- Automatic type inference
- Web-based UI (Streamlit)
- Three-Address Code (TAC) generation

## Setup
```bash

# create virtual environemnt
python3 -m venv venv
source venc/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage 

### Web UI (Recommended)
```bash
streamlit run ui/app.py
```

### Command line
```bash
python ui/cli.py examples/example1.txt
```

## project structure
```
src/        - Compiler core
ui/         - User interfaces
tests/      - unit tests
examples/   - sample programs
docs/       - documentation
```

## team
Team ID CD-VI-T079-2026
Course: Compiler Design

