from functions.run_python_file import run_python_file


def print_result(label: str, result: str) -> None:
    print(f"{label}")
    for line in result.splitlines():
        print(f"  {line}")
    print()


if __name__ == "__main__":
    print_result("Result for main.py:", run_python_file("calculator", "main.py"))
    print_result("Result for main.py with args:", run_python_file("calculator", "main.py", ["3 + 5"]))
    print_result("Result for tests.py:", run_python_file("calculator", "tests.py"))
    print_result("Result for ../main.py:", run_python_file("calculator", "../main.py"))
    print_result("Result for nonexistent.py:", run_python_file("calculator", "nonexistent.py"))
    print_result("Result for lorem.txt:", run_python_file("calculator", "lorem.txt"))
