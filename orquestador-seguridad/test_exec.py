from app.runners.exec import run_command

result = run_command(["python", "--version"])
print(result)
