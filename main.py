import sys
import ast
from compiler import validate  # I BUILT THIS; DON'T TOUCH IT

def is_valid_python_code(code: str) -> bool:
    """
    Checks whether the provided Python code is syntactically valid.
    """
    try:
        tree = ast.parse(code)
        compile(tree, filename="<ast>", mode="exec")
        return True
    except SyntaxError as e:
        print(f"[Syntax Error] {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3.11 main.py <filename.py>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source = file.read()
    except FileNotFoundError:
        print(f"[Error] File not found: {file_path}")
        sys.exit(1)

    print(f"Checking syntax for: {file_path}")
    if is_valid_python_code(source):
        print("[✓] Python syntax is valid.")
    else:
        print("[✗] Python syntax is invalid.")

    print("Compiler Output:\n" + "-"*20)
    compiler_result = validate(file_path)
    print(compiler_result)

if __name__ == "__main__":
    main()
