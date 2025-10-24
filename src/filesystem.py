import os
from local_types import EmailData, FoldersTree
import regex

EXTENSION='eml'

async def get_folder_tree(path: str) -> FoldersTree:
    folder_content = os.listdir(path)
    child_folders_paths = list(filter(lambda child_path: os.path.isdir(f'{path}/{child_path}'), folder_content))
    child_folders = [ await get_folder_tree(f'{path}/{folder_path}') for folder_path in child_folders_paths ]
    return FoldersTree(path,child_folders)

def get_email_data(email_path: str) -> EmailData:
    file = open(email_path, 'r')
    content = file.read()
    return EmailData(
        regex.find_first(regex.email_from, content),
        regex.find_first(regex.email_to, content),
        regex.find_first(regex.email_subject, content),
        regex.find_datetime(regex.email_date, content),
        regex.find_first(regex.email_id, content),
        content
    )

def create_folder_if_not_exists(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def unique_email_file_name(path: str, email: EmailData) -> str:
    proposed_file_path_without_extension = f'{path}/{email.file_name}'
    counter=0
    file_path_without_extension = f'{proposed_file_path_without_extension}' if counter < 1 else f'{proposed_file_path_without_extension}({counter})'
    file_path = f'{file_path_without_extension}.{EXTENSION}'
    while os.path.exists(file_path):
        counter+=1
        file_path_without_extension = f'{proposed_file_path_without_extension}' if counter < 1 else f'{proposed_file_path_without_extension}({counter})'
        file_path = f'{file_path_without_extension}.{EXTENSION}'
    return file_path
        
def create_email_file(email_file_path: str) -> None:
    email_file = open(email_file_path, 'w')
    email_file.write('')
    email_file.close()

def save_email_content_to_file(email_file_path: str, email: EmailData) -> None:
    email_file = open(email_file_path, 'w')
    email_file.write(email.content)
    email_file.close()

def email_to_file(path: str, email: EmailData) -> None:
    create_folder_if_not_exists(path)
    email_file_path = unique_email_file_name(path, email)
    create_email_file(email_file_path)
    save_email_content_to_file(email_file_path, email)