import ast

class OOPDetector(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.instantiations = []

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check if it's a class instantiation like Book()
        if isinstance(node.func, ast.Name):
            self.instantiations.append(node.func.id)
        self.generic_visit(node)

def analyze_oop(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = ast.parse(code)
    detector = OOPDetector()
    detector.visit(tree)

    print("[✓] OOP Analysis Result:")
    print("  Classes Found:", detector.classes)
    print("  Instantiations:", detector.instantiations)

    if detector.classes:
        print("✅ Code uses classes.")
    else:
        print("⚠️ No classes found.")

    if detector.instantiations:
        print("✅ Code uses object instantiations.")
    else:
        print("⚠️ No instantiations found.")

# Usage
analyze_oop('test.py')
