import os
import asyncio
from dotenv import load_dotenv
from filesystem import copy_email_files, get_email_iterations_and_trays, get_emails_iterations, get_children_folders
from pprint import pp

load_dotenv(override=True)

EMAILS_PATH = os.getenv("EMAILS_PATH", '')
DESTINATION_PATH = os.getenv("DESTINATION_PATH", '')

if EMAILS_PATH == '' or DESTINATION_PATH == '': raise ValueError('Environment variables lost')

async def main() -> None:
    source_emails = await get_children_folders(EMAILS_PATH)
    email_iterations = await get_emails_iterations(EMAILS_PATH, source_emails)
    email_iterations_and_trays = await get_email_iterations_and_trays(EMAILS_PATH, email_iterations)
    await copy_email_files(EMAILS_PATH, DESTINATION_PATH, email_iterations_and_trays)

if __name__ == "__main__":
    asyncio.run(main())
