from config import MAX_CHARS
from functions.get_file_content import get_file_content


def print_result(label: str, result: str) -> None:
    print(f"{label}")
    for line in result.splitlines():
        print(f"  {line}")
    print()


def test_lorem_truncation() -> None:
    result = get_file_content("calculator", "lorem.txt")
    assert len(result) > MAX_CHARS, "lorem.txt should be truncated"
    assert f'truncated at {MAX_CHARS} characters' in result, "truncation message should appear"
    print("lorem.txt truncation test: passed")
    print(f"  length: {len(result)}")
    print(f"  ends with: ...{result[-80:]!r}")
    print()


if __name__ == "__main__":
    test_lorem_truncation()

    print_result("Result for main.py:", get_file_content("calculator", "main.py"))
    print_result("Result for pkg/calculator.py:", get_file_content("calculator", "pkg/calculator.py"))
    print_result("Result for /bin/cat:", get_file_content("calculator", "/bin/cat"))
    print_result("Result for pkg/does_not_exist.py:", get_file_content("calculator", "pkg/does_not_exist.py"))
