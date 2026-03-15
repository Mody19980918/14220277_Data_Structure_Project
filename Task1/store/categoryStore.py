from common.data_paths import category_file_path

def list_categories() -> list[str]:
    """
    List all categories in the library
    """
    categories: list[str] = []
    try:
        with open(category_file_path(), "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if line:
                    categories.append(line)
    except FileNotFoundError:
        return categories
    return categories


def append_category(category: str) -> None:
    """
    Append a category to the library
    """
    with open(category_file_path(), "a", encoding="utf-8") as file:
        file.write(f"{category}\n")


def overwrite_categories(categories: list[str]) -> None:
    """
    Overwrite the categories in the library
    """
    with open(category_file_path(), "w", encoding="utf-8") as file:
        for category in categories:
            file.write(f"{category}\n")
