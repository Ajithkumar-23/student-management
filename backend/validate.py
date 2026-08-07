import ast
import os
import sys


files_to_check = [
    "app.py"
]


for file in files_to_check:

    if not os.path.exists(file):
        print(f"ERROR: {file} not found")
        sys.exit(1)

    try:
        with open(file, "r", encoding="utf-8") as f:
            source = f.read()

        ast.parse(source)

        print(f"SUCCESS: {file} syntax is valid")

    except SyntaxError as error:
        print(f"ERROR: Syntax error in {file}")
        print(error)
        sys.exit(1)


print("All validation checks passed")