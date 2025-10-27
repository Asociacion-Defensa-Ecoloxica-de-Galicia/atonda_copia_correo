from dataclasses import dataclass
from typing import Optional, List, Self
from slugify import slugify
from email import utils as email_utils

@dataclass
class EmailData:
    source: str
    destination: str
    subject: str
    date: str
    @property
    def file_name(self):
        subject = self.subject if len(self.subject) <= 100 else f'{self.subject[0:97]}...'
        try:
            date = str(email_utils.parsedate_to_datetime(self.date))
        except:
            date = ''
        return slugify(f'{date}_{email_utils.parseaddr(self.source)[1]}_{email_utils.parseaddr(self.destination)}_{subject}')

@dataclass
class FoldersTree:
    path: str
    children: List[Self]