path = r"test\test2.py"

with open(path, "r") as f:
    code = f.read()

vars_ = {}

exec(code, None, vars_)

print(vars_)

