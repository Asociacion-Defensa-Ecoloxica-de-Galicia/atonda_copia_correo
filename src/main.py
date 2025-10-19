import imaplib
import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(override=True)

IMAP_SERVER = os.getenv("IMAP_SERVER", '')
REFERENCEDATE = os.getenv("REFERENCEDATE", '')
if IMAP_SERVER == '' or REFERENCEDATE == '': raise Exception("We need a IMAP_SERVER and REFERENCEDATE environment variable (or .env)")
SAVEDIR = os.getenv("SAVEDIR", "./emails")

found_emails = False

def save_email(folder: str, msg_id: bytes, msg_content: bytes, account_save_dir: str) -> None:
    """Save an email as an .eml file inside a folder-specific directory."""
    folder_dir = os.path.join(account_save_dir, folder)
    os.makedirs(folder_dir, exist_ok=True)
    filename = os.path.join(folder_dir, f"email_{msg_id.decode('utf-8')}.eml")
    with open(filename, "wb") as f:
        f.write(msg_content)

def list_folders(username: str, password: str) -> list[str]:
    """
    Connect to the IMAP server and list all folders.
    Returns a list of folder names.
    """
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    status, _ = mail.login(username, password)
    if status != "OK":
        print("Login failed while listing folders!")
        return []
    status, folders = mail.list()
    if status != "OK" or not folders:
        print("Failed to retrieve folders!")
        mail.logout()
        return []

    folder_list = []
    for folder_info in folders:
        # Typical response: b'(\\HasNoChildren) "/" "INBOX"'
        parts = folder_info.decode().split(' "/" ')
        if len(parts) == 2:
            folder = parts[1].strip('"')
        else:
            folder = folder_info.decode()
        folder_list.append(folder)
    mail.logout()
    return folder_list


def fetch_save_and_delete_email(folder: str, msg_id: bytes, account_save_dir: str, mail: imaplib.IMAP4_SSL):

    status, msg_data = mail.fetch(str(int(msg_id)), "(RFC822)")
    if status != "OK" or not msg_data:
        print(f"Failed to fetch email {msg_id.decode('utf-8')} in folder {folder}")
        mail.logout()
        return

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            raw_email = response_part[1]
            save_email(folder, msg_id, raw_email, account_save_dir)
            #print(f"Saved email {msg_id.decode('utf-8')} in folder {folder}")

    status, _ = mail.store(str(int(msg_id)), '+FLAGS', '\\Deleted')
    if status != 'OK': raise Exception(f'Unable to mark {msg_id} as deleted in folder {msg_id}')
    status, _ = mail.expunge()
    if status != 'OK': raise Exception(f'Unable to expurge {msg_id} message')    

def process_folder(folder: str, account_save_dir: str, username: str, password: str) -> None:
    """
    Synchronously retrieves all email IDs for the given folder,
    then downloads each email asynchronously.
    """

    global found_emails

    #print(f"Processing folder: {folder}")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    status, _ = mail.login(username, password)
    if status != "OK":
        print(f"Login failed for email {username} in folder {folder}!")
        return

    status, _ = mail.select(f'"{folder}"', readonly=False)
    if status != "OK":
        print(f"Unable to open mailbox {folder} for email {username}")
        mail.logout()
        return

    status, data = mail.search(None, f'(ALL BEFORE {REFERENCEDATE})')
    if status != "OK" or not data:
        print(f"Email search failed in folder {folder}!")
        mail.logout()
    email_ids = data[0].split()

    if len(email_ids) > 0:
        found_emails = True
        print(f'Found {len(email_ids)} e-mails in {folder} for {username}')

    #print(f"Folder '{folder}' has {len(email_ids)} emails.")

    for msg_id in email_ids:
        try:
            fetch_save_and_delete_email(folder, msg_id, account_save_dir, mail)
        except Exception as e:
            print('*'*10)
            break

    mail.close()
    mail.logout()

def proccess_accounts():
    accounts_file = open(os.path.dirname(__file__)+'/accounts.csv','r')
    accounts = [account.split(';') for account in accounts_file.readlines()]

    for index, account in enumerate(accounts):
        accounts[index] = [account[0], account[1].strip('\n')]

    for account in accounts:
        username, password = account
        if password == '': continue
        print(f'Account: {username}, {password}')
        account_save_dir = SAVEDIR+'/'+username+'/'+REFERENCEDATE+'_'+str(datetime.timestamp(datetime.now()))
        os.makedirs(account_save_dir, exist_ok=True)
        folders = [folder.split('"." ')[-1].replace('"', '') for folder in list_folders(username, password)]
        if not folders:
            print("No folders found!")
            return

        for folder in folders:
            process_folder(folder, account_save_dir, username, password)


async def main() -> None:

    global found_emails

    proccess_accounts()

    while found_emails:
        found_emails = False
        proccess_accounts()


if __name__ == "__main__":
    asyncio.run(main())
