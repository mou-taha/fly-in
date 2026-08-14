from simple_term_menu import TerminalMenu  # type: ignore
from pathlib import Path as FileSystemPath


def choose_map_file(project_root: FileSystemPath) -> str | None:
    maps_dir = project_root / "maps"
    available_files = sorted(p for p in maps_dir.rglob("*.txt") if p.is_file())
    menu_entries = []
    if available_files:
        menu_entries = [
            str(file_path.relative_to(project_root))
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
