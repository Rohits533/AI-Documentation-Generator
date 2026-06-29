import ast

class DocEngine:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)

    def extract_functions(self):
        """Extract all function names and their docstrings."""
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node) or ""
                functions.append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "docstring": docstring,
                    "body": ast.unparse(node.body)
                })
        return functions

    def extract_classes(self):
        """Extract all class names and their docstrings."""
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node) or ""
                classes.append({
                    "name": node.name,
                    "docstring": docstring,
                    "body": ast.unparse(node.body)
                })
        return classes

    def generate_readme(self, project_name="My Project"):
        """Generate a README from the code."""
        functions = self.extract_functions()
        classes = self.extract_classes()
        
        readme = f"# {project_name}\n\n"
        
        if functions:
            readme += "## Functions\n\n"
            for func in functions:
                readme += f"### `{func['name']}({', '.join(func['args'])})`\n\n"
                readme += f"{func['docstring'] or 'No description provided.'}\n\n"
        
        if classes:
            readme += "## Classes\n\n"
            for cls in classes:
                readme += f"### `{cls['name']}`\n\n"
                readme += f"{cls['docstring'] or 'No description provided.'}\n\n"
        
        readme += "## Installation\n\n"
        readme += "```bash\npip install -r requirements.txt\n```\n\n"
        readme += "## Usage\n\n"
        readme += "```python\n# Example usage\n```\n\n"
        
        return readme
