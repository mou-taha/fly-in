from simple_term_menu import TerminalMenu
from pathlib import Path as FileSystemPath
from enum import Enum


class Colors(Enum):
    """colors to use for zones

    Args:
        Enum (_type_): color code to use for print() function
    """

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    PURPLE = "\033[95m"
    BROWN = "\033[33m"
    ORANGE = "\033[38;5;208m"
    MARRON = "\033[38;5;88m"
    GOLD = "\033[38;5;220m"
    DARKRED = "\033[38;5;52m"
    CRIMSON = "\033[38;5;161m"
    VIOLET = "\033[95m"


def get_code_color(color_name: str) -> str:
    """find the code color from a string if the color doesn't exist.
    its return the code of color white

    Args:
        color_name (str): color name

    Returns:
        str: code color to use for print() function.
    """
    color_name = color_name.upper()
    return (
        Colors[color_name].value
        if color_name in Colors.__members__
        else Colors.WHITE.value
    )


def color_text(text: str, color_name: str) -> str:
    """take a string and add to it the desire color code at the beginning
    and rest it at the end with white.
    and for the color rainbow iterate over the text and add for each char
    a specific color.

    Args:
        text (str): desire text to color.
        color_name (str): color.

    Returns:
        str: return a colored string.
    """
    colors = [
        "\033[31m",  # Red
        "\033[93m",  # Bright Yellow
        "\033[32m",  # Green
        "\033[36m",  # Cyan
        "\033[34m",  # Blue
        "\033[35m",  # Magenta
    ]
    reset = Colors.WHITE.value

    # Apply a color to each character
    if color_name.upper() == "RAINBOW":
        text = "".join(
            f"{colors[i % len(colors)]}{char}{reset}"
            for i, char in enumerate(text)
        )
    else:
        color = get_code_color(color_name)
        return f"{color}{text}{reset}"

    return text + reset


def choose_map_file(project_root: FileSystemPath) -> str | None:
    """
    show a menu on terminal where the user can choose a map or a custom file.

    Args:
        project_root (FileSystemPath): root dir for the project

    Raises:
        ValueError: if no custom file provided.
        FileNotFoundError: if the custom file doesn't exist.

    Returns:
        str | None: none or selected file path.
    """
    maps_dir = project_root / "maps"
    available_files = sorted(p for p in maps_dir.rglob("*.txt") if p.is_file())
    menu_entries = []
    if available_files:
        menu_entries = [
            str(file_path.relative_to(project_root).name)
            for file_path in available_files
        ]
    menu_entries.append("Custom file path...")
    menu_entries.append("Exit")
    menu = TerminalMenu(
        menu_entries,
        title="Select a map file",
        menu_cursor="➜ ",
        menu_cursor_style=("fg_yellow", "bold"),
        menu_highlight_style=("bg_blue", "fg_gray", "bold"),
        clear_screen=False,
        cycle_cursor=True,
    )
    selected_index = menu.show()

    if selected_index is None:
        return None

    if isinstance(selected_index, (tuple, list)):
        if len(selected_index) == 0:
            return None
        selected_index = selected_index[0]

    if selected_index == len(menu_entries) - 1:
        return None

    if selected_index == len(menu_entries) - 2:
        custom_path = input("Enter the file path: ").strip()
        if not custom_path:
            raise ValueError("No custom path provided.")
        file_path = FileSystemPath(custom_path)
        if not file_path.is_absolute():
            file_path = project_root / file_path
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {custom_path}")
        return str(file_path)

    return str(available_files[selected_index])
