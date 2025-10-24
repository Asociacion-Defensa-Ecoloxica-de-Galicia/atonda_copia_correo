import os

def create_folder_if_not_exists(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)