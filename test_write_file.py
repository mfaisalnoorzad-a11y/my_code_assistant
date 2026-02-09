from functions.write_file import write_file
from config import MAX_CHARS

def print_result(label: str, result: str) -> None:
    print(f"{label}")
    for line in result.splitlines():
        print(f"  {line}")
    print()

if __name__ == "__main__":
    print_result("Result for writing to lorem.txt:", write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print_result("Result for writing to pkg/morelorem.txt:", write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print_result("Result for writing to temp.txt:", write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
