import os
import re
import sys
from pathlib import Path

def extract_docstring(content, start_idx):
    """Extract docstring from the content starting at the given index."""
    docstring_match = re.search(r'"""(.*?)"""', content[start_idx:], re.DOTALL)
    if docstring_match:
        return docstring_match.group(1).strip()
    return None

def analyze_python_file(file_path):
    """Analyze a Python file and extract classes, methods, and their docstrings."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    structure = []
    
    for i, line in enumerate(lines):
        # Find classes
        class_match = re.match(r'\s*class\s+(\w+)', line)
        if class_match:
            class_name = class_match.group(1)
            docstring = extract_docstring(content, content.find(line))
            class_info = {'type': 'class', 'name': class_name, 'docstring': docstring, 'methods': []}
            structure.append(class_info)
            continue
            
        # Find methods
        method_match = re.match(r'\s*def\s+(\w+)', line)
        if method_match:
            method_name = method_match.group(1)
            docstring = extract_docstring(content, content.find(line))
            method_info = {'type': 'method', 'name': method_name, 'docstring': docstring}
            
            # If we're inside a class, add to last class's methods
            if structure and structure[-1]['type'] == 'class':
                structure[-1]['methods'].append(method_info)
            else:
                structure.append(method_info)
    
    return structure

def generate_markdown(folder_path):
    """Generate markdown output for the folder structure."""
    output = ["# Folder Structure\n"]
    
    def process_directory(directory, indent_level=0):
        path = Path(directory)
        
        # Add current directory to output
        if indent_level > 0:  # Don't add the root folder
            output.append(f"{'#' * (indent_level + 1)} {path.name}")
        
        # Process all items in directory
        for item in sorted(path.iterdir()):
            if item.is_file() and item.suffix == '.py':
                output.append(f"{'#' * (indent_level + 2)} {item.name}")
                
                # Analyze Python file
                try:
                    structure = analyze_python_file(item)
                    for element in structure:
                        if element['type'] == 'class':
                            doc_str = f": {element['docstring']}" if element['docstring'] else ""
                            output.append(f"        - {element['name']}{doc_str}")
                            for method in element['methods']:
                                doc_str = f": {method['docstring']}" if method['docstring'] else ""
                                output.append(f"            - {method['name']}{doc_str}")
                        else:  # standalone method
                            doc_str = f": {element['docstring']}" if element['docstring'] else ""
                            output.append(f"        - {element['name']}{doc_str}")
                except Exception as e:
                    output.append(f"        - Error reading file: {str(e)}")
            
            elif item.is_dir() and not item.name.startswith('.'):
                process_directory(item, indent_level + 1)
    
    process_directory(folder_path)
    return '\n'.join(output)

def main():
    if len(sys.argv) != 2:
        print("Usage: python folder_summarizer.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory")
        sys.exit(1)
    
    markdown_output = generate_markdown(folder_path)
    
    # Create Output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the folder name from the input path
    folder_name = os.path.basename(os.path.normpath(folder_path))
    
    # Write to output file in the Output directory with the folder name
    output_file = os.path.join(output_dir, f'{folder_name}_summary.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    
    print(f"Folder structure has been written to: {output_file}")

if __name__ == "__main__":
    main()
