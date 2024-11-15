# Python Folder Structure Summarizer

A simple command-line tool that generates a markdown summary of a Python project's structure, including classes, methods, and their docstrings.

## Usage

```bash
python folder_summarizer.py <folder_path>
```

The script will create a markdown file in the `Output` directory named `{folder_name}_summary.md`.

## Example Output

```markdown
# Folder Structure
## my_project
### main.py
        - class MyClass: This is a sample class
            - method1: Handles data processing
            - method2: Performs calculations
### utils.py
        - helper_function: Utility function for data validation
```

## Features

- Recursively scans directories
- Detects Python classes and methods
- Extracts docstrings
- Generates hierarchical markdown structure
- Creates organized output in dedicated folder

## Requirements

- Python 3.6+
- No external dependencies
