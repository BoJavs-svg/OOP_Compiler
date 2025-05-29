import re
import sys

class Parser:
    def __init__(self, source_code):
        self.tokens = self.tokenize(source_code)
        self.current = 0

        self.class_found = False
        self.instantiation_found = False
        self.self_method_found = False

    # --- Tokenization ---
    def tokenize(self, code):
        token_specification = [
            ('COMMENT_BLOCK_A', r'"""[\s\S]*?"""'),
            ('COMMENT_BLOCK_B', r"'''[\s\S]*?'''"),
            ('COMMENT',         r'#.*'),           
            ('CLASS',           r'class\b'),
            ('DEF',             r'def\b'),
            ('SELF',            r'self\b'),
            ('ASSIGN',          r'='),
            ('COLON',           r':'),
            ('COMMA',           r','),
            ('LPAREN',          r'\('),
            ('RPAREN',          r'\)'),
            ('CLASS_NAME',      r'[A-Z][a-zA-Z0-9]*'),
            ('IDENTIFIER',      r'[a-z_][a-zA-Z0-9_]*'),
            ('EOL',             r'\n'),
            ('SKIP',            r'[ \t]+'),
            ('INVALID',         r'.'),
        ]   

        token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
        tokens = []
        for mo in re.finditer(token_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            if kind in {'SKIP', 'COMMENT', 'COMMENT_BLOCK_A', 'COMMENT_BLOCK_B'}:
                continue
            elif kind == 'INVALID':
                #print(f"Invalid character: {value}")
                tokens.append(('INVALID', value))
            else:
                tokens.append((kind, value))
        tokens.append(('EOF', ''))
        return tokens

    def peek(self):
        return self.tokens[self.current][0]

    def match(self, expected_type):
        if self.peek() == expected_type:
            value = self.tokens[self.current][1]
            self.current += 1
            return value
        return None

    def expect(self, expected_type):
        value = self.match(expected_type)
        if value is None:
            raise SyntaxError(f"Expected {expected_type}, found {self.tokens[self.current]}")
        return value

    # --- Grammar Rules ---
    def parse(self):
        while self.peek() != 'EOF':
            try:
                self.stmt()
            except SyntaxError as e:
                # #print(f"Syntax error: {e}")
                self.sync()

    def stmt(self):
        if self.peek() == 'CLASS':
            self.class_def()
        elif self.peek() == 'DEF':
            self.method_self()
        elif self.peek() == 'IDENTIFIER':
            self.instantiation()
        elif self.peek() in {'CLASS_NAME', 'ASSIGN', 'LPAREN', 'RPAREN', 'COLON', 'INVALID'}:
            self.stray_line()
        elif self.peek() == 'EOL':
            self.match('EOL')
        else:
            raise SyntaxError("Unknown statement start")

    def class_def(self):
        self.expect('CLASS')
        name = self.expect('CLASS_NAME')
        if self.peek() == 'LPAREN':
            self.match('LPAREN')
            self.expect('CLASS_NAME')
            self.expect('RPAREN')
        self.expect('COLON')
        self.expect('EOL')
        # #print(f"[Parser] Found class definition: {name}")
        self.class_found = True


    def instantiation(self):
        var_name = self.expect('IDENTIFIER')
        self.expect('ASSIGN')
        class_name = self.expect('CLASS_NAME')
        self.expect('LPAREN')
        self.expect('RPAREN')
        self.expect('EOL')
        # #print(f"[Parser] Found instantiation: {var_name} = {class_name}()")
        self.instantiation_found = True

    def method_self(self):
        self.expect('DEF')
        method_name = self.expect('IDENTIFIER')
        self.expect('LPAREN')
        self.arg_list()
        self.expect('RPAREN')
        self.expect('COLON')
        self.expect('EOL')
        #print(f"[Parser] Found method with self: {method_name}")
        self.self_method_found = True

    def arg_list(self):
        self.expect('SELF')
        if self.peek() == 'COMMA':
            self.match('COMMA')
            self.arg_rest()

    def arg_rest(self):
        self.expect('IDENTIFIER')
        while self.peek() == 'COMMA':
            self.match('COMMA')
            self.expect('IDENTIFIER')

    def stray_line(self):
        # Just consume tokens until EOL
        while self.peek() not in {'EOL', 'EOF'}:
            self.current += 1
        if self.peek() == 'EOL':
            self.match('EOL')

    def sync(self):
        # Simple sync to next EOL
        while self.peek() not in {'EOL', 'EOF'}:
            self.current += 1
        if self.peek() == 'EOL':
            self.current += 1

    # def summary(self):
    #     #print("\n[Result] Detection Summary:")
    #     #print(f"  Class Found: {'YES' if self.class_found else 'NO'}")
    #     #print(f"  Instantiation Found: {'YES' if self.instantiation_found else 'NO'}")
    #     #print(f"  Method with self Found: {'YES' if self.self_method_found else 'NO'}")

    #     if self.class_found:
    #         #print("✅ Code uses object-oriented programming.")
    #     else:
    #         #print("⚠️ Not enough OOP patterns detected.")

def validate(source):
    # with open(path, 'r') as f:
    #     source = f.read()
    parser = Parser(source)
    parser.parse()
    # parser.summary()
    return parser.class_found
