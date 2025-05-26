from compiler import validate
import ast
def is_valid_python_code(path: str) -> bool:
    with open(path, 'r') as f:
        code = f.read()
    try:    
        tree = ast.parse(code)
        compile(tree, filename="<ast>", mode="exec")
        return True
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        return False

if validate("test.py"):
    print("Code uses object-oriented programming.")
else:
    print("Not enough OOP patterns detected.")

if is_valid_python_code("test.py"):
    print("Is correct python code.")
else:
    print("Python code has issues.")