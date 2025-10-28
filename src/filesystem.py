from logging import exception
import os
from local_types import EmailData, FoldersTree
import email as email_tools
import csv

EXTENSION='eml'

async def get_children_folders(current_path: str) -> list[str]:
    folder_content = os.listdir(current_path)
    return list(filter(lambda child_path: os.path.isdir(f'{current_path}/{child_path}'), folder_content))

async def get_emails_iterations(source_path: str, emails: list[str]) -> dict[str,list[str]]:
    email_iterations = {}
    for email in [ {'path': f'{source_path}/{email}','address': email} for email in emails]:
        iterations = await get_children_folders(email['path'])
        email_iterations[email['address']] = iterations
    return email_iterations

async def get_email_iterations_and_trays(source_path: str, email_iterations: dict[str,list[str]]) -> dict[str,dict[str,list[str]]]:
    output: dict[str,dict[str,list[str]]] = {}
    for  email, iterations in email_iterations.items():
        trays = set()
        for iteration_path in [ f'{source_path}/{email}/{iteration}' for iteration in iterations ]:
            trays.update(await get_children_folders(iteration_path))
        output[email] = {'iterations': iterations, 'trays': list(trays)}
    return output

def get_moved_files() -> set:
    log_file = open('log.txt', 'r')
    log_contents = csv.reader(log_file, delimiter=';')
    moved_files = set()
    for row in log_contents:
        moved_files.add(row[0])
    log_file.close()
    return moved_files

async def copy_email_files(source_path: str, destination_folder: str, email_iterations_and_trays: dict[str,dict[str,list[str]]]):
    moved_files = get_moved_files()
    for email, email_data in email_iterations_and_trays.items():
        for iteration in email_data['iterations']:
            for tray in email_data['trays']:
                path = f'{source_path}/{email}/{iteration}/{tray}'
                if os.path.isdir(path):
                    path_contents = os.listdir(path)
                    for item in path_contents:
                        if os.path.isfile(f'{path}/{item}') and f'{path}/{item}' in moved_files:
                            print(f'Moved: {path}/{item}')
                    email_files = list(filter(lambda item: os.path.isfile(f'{path}/{item}') and not f'{path}/{item}' in moved_files, path_contents))
                    for email_file in email_files:
                        source_email_file = f'{path}/{email_file}'
                        print(source_email_file)
                        email_metadata = email_tools.message_from_binary_file(open(source_email_file,'rb'))
                        source_email = EmailData(
                            email_metadata['from'] or '',
                            email_metadata['to'] or '',
                            str(email_metadata['subject'] or ''),
                            email_metadata['date'] or '',
                        )
                        email_destination_folder_path = f'{destination_folder}/{email}/{tray}'
                        create_folder_if_not_exists(email_destination_folder_path)
                        destination_email_file = get_unique_email_file_name(email_destination_folder_path, source_email)
                        # try:
                        #     create_email_file(destination_email_file)
                        #     await move_email(source_email_file, destination_email_file)
                        # except Exception as exception:
                        #     error_log_file = open('log_errors.txt', 'a')
                        #     error_log_file.write(f'"{source_email_file}": "{exception}"\n')
                        #     error_log_file.close()
                        # else:
                        #     log_file = open('log.txt', 'a')
                        #     log_file.write(f'"{source_email_file}";"{destination_email_file}"\n')
                        #     log_file.close()

async def get_folder_tree(path: str) -> FoldersTree:
    folder_content = os.listdir(path)
    child_folders_paths = list(filter(lambda child_path: os.path.isdir(f'{path}/{child_path}'), folder_content))
    child_folders = [ await get_folder_tree(f'{path}/{folder_path}') for folder_path in child_folders_paths ]
    return FoldersTree(path,child_folders)

async def get_email_content(email_path: str) -> bytes:
    file = open(email_path, 'rb')
    return file.read()

def create_folder_if_not_exists(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def get_unique_email_file_name(path: str, email: EmailData) -> str:
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

async def move_email(source_email_file: str, destination_email_file: str) -> None:
    os.replace(source_email_file, destination_email_file)