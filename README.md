# Mini Lisp Interpreter in Python

This project is a minimalist Lisp interpreter written in Python. It supports basic arithmetic, conditionals, function definitions (including lambdas), list operations, and a standard environment with built-in functions — all built from scratch with a focus on clarity and extensibility.

## Features

- Lisp-like syntax with support for:
  - Numbers, Symbols, and Lists
  - First-class functions and user-defined lambdas
  - Variable bindings and lexical scoping
  - Conditional expressions (`if`)
  - Built-in functions: arithmetic, comparison, logic, list operations
  - Type checking (`number?`, `list?`, `symbol?`, etc.)
  - `begin`, `define`, `lambda`, `set!`, and more

## Core Components

- **Parser**: Tokenizes and parses Lisp expressions into ASTs
- **Evaluator**: Recursively evaluates AST nodes in a given environment
- **Environment**: Manages variable/function scope and bindings
- **REPL**: Interactive Read-Eval-Print Loop for executing expressions

## Usage

To start the interpreter:

```bash
python main.py
