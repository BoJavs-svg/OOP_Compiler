import ast
import requests
import base64
import json
from datasets import load_dataset
from compiler import validate # I BUILT THIS; DONT TOUCH IT
import ast

class OOPValidator(ast.NodeVisitor):
    def __init__(self):
        self.has_class = False
        self.has_init = False
        self.uses_self = False
        self.inherits = False

    def visit_ClassDef(self, node):
        self.has_class = True

        # Check for inheritance
        self.inherits = len(node.bases) > 0

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Check if method uses self
                if item.args.args and item.args.args[0].arg == "self":
                    self.uses_self = True
                if item.name == "__init__":
                    self.has_init = True

        # Continue to walk into other parts of the class
        self.generic_visit(node)

def is_oop_class(source: str) -> bool:
    try:
        tree = ast.parse(source)
        validator = OOPValidator()
        validator.visit(tree)
        return validator.has_class
    except Exception as e:
        print(f"AST parsing error: {e}")
        return False

headers = {
    'Accept': 'application/vnd.github.v3+json',
    'X-GitHub-Api-Version': '2022-11-28',
    
}

def test_github_auth():
    response = requests.get("https://api.github.com/rate_limit", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Authenticated successfully.")
        print(f"Remaining rate limit: {data['rate']['remaining']} out of {data['rate']['limit']}")
    elif response.status_code == 401:
        print("❌ Authentication failed. Check your token.")
    else:
        print(f"⚠️ Unexpected status code {response.status_code}: {response.text}")

def getContext(data):
    repo_full_name = data["repo"]
    owner, repo_name = repo_full_name.split('/')
    patch = data["patch"]
    commit_sha = data["base_commit"]

    # Estimate changed files from patch — GitHub uses filenames starting with "+++ b/..."
    files_changed = []
    for line in patch.splitlines():
        if line.startswith("+++ b/"):
            filepath = line[6:]
            files_changed.append(filepath)
    if len(files_changed) == 1:
        file_path = files_changed[0]
        url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}?ref={commit_sha}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("Added " + files_changed[0] )
            content_json = response.json()
            encoded_content = content_json.get('content', '')
            decoded_content = base64.b64decode(encoded_content).decode('utf-8')
            return decoded_content
        else:
            print(f"Failed to fetch file content from GitHub (status {response.status_code}): {response.text}")
            return ""
    else:
        # print("Multiple files changed, skipping entry.")
        return ""

def is_valid_python_code(code: str) -> bool:
    try:    
        tree = ast.parse(code)
        compile(tree, filename="<ast>", mode="exec")
        return True
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        return False

# Main logic
true_positive = false_positive = false_negative = 0

test_github_auth()
with open("valid_oop_cases.jsonl", "w", encoding="utf-8") as output_file:
    dataset = load_dataset('SWE-bench/SWE-bench_Lite', split='test')
    for entry in dataset:
        source = getContext(entry)
        if not source or not is_valid_python_code(source):
            continue

        ground_truth = is_oop_class(source)
        compiler_result = validate(source)

        if compiler_result and ground_truth:
            true_positive += 1
            json_line = json.dumps(entry, ensure_ascii=False)
            output_file.write(json_line + "\n")
        elif compiler_result and not ground_truth:
            false_positive += 1
        elif not compiler_result and ground_truth:
            false_negative += 1
        # else: true negative (not counted here)

# Print accuracy metrics
precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) else 0
recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

print("\n📊 Results:")
print(f"✅ True Positives:  {true_positive}")
print(f"❌ False Positives: {false_positive}")
print(f"⚠️ False Negatives: {false_negative}")
print(f"\n🎯 Precision: {precision:.2f}")
print(f"🔍 Recall:    {recall:.2f}")
print(f"📈 F1 Score:  {f1:.2f}")