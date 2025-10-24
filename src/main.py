import os
import asyncio
from re import Pattern
from dotenv import load_dotenv
from dataclasses import dataclass
from datetime import datetime
from email import utils
from typing import Optional
from pprint import pp

import regex

load_dotenv(override=True)

EMAILS_PATH = os.getenv("EMAILS_PATH", './backups')

@dataclass
class EmailData:
    source: Optional[str]
    destination: Optional[str]
    date: Optional[str]
    msg_id: Optional[str]
    content: str

def find_first(regex: Pattern[str], string: str) -> Optional[str]:
    results = regex.findall(string)
    return None if len(results) == 0 else results[0]

def find_datetime(regex, content) -> Optional[str]:
    datetime_string = find_first(regex, content)
    if datetime_string == None: return None 
    return utils.parsedate_to_datetime(datetime_string).isoformat()

async def get_email_data(email_path: str) -> EmailData:
    file = open(email_path, 'r')
    content = file.read()
    return EmailData(
        find_first(regex.email_from,content),
        find_first(regex.email_to,content),
        find_datetime(regex.email_date, content),
        find_first(regex.email_id,content),
        content
    )

async def main() -> None:
    #data = await get_email_data('./email_backups/itziar@adega.gal/01-Jul-2021_0/INBOX/email_1.eml')
    #pp(data)

if __name__ == "__main__":
    asyncio.run(main())
