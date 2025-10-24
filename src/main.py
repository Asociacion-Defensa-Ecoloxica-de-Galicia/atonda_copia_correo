import os
import asyncio
from dotenv import load_dotenv
from filesystem import email_to_file, get_email_data, get_folder_tree
from pprint import pp

load_dotenv(override=True)

EMAILS_PATH = os.getenv("EMAILS_PATH", '')
DESTINATION_PATH = os.getenv("DESTINATION_PATH", '')

if EMAILS_PATH == '' or DESTINATION_PATH == '': raise ValueError('Environment variables lost')

async def main() -> None:
    #email = get_email_data('email_backups/itziar@adega.gal/01-Jul-2021_0/INBOX/email_1.eml')
    #email_to_file(DESTINATION_PATH, email)
    tree = await get_folder_tree(EMAILS_PATH)
    pp(tree)

if __name__ == "__main__":
    asyncio.run(main())
