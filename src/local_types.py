from dataclasses import dataclass
from typing import List, Self
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
        try:
            date = str(email_utils.parsedate_to_datetime(self.date))
        except:
            date = ''
        source = email_utils.parseaddr(self.source)[1]
        destination = email_utils.parseaddr(self.destination)[1]
        name =  slugify(f'{date}_{source}_{destination}_{self.subject}') 
        return name if len(name) <= 200 else f'{name[0:195]}[...]'

@dataclass
class FoldersTree:
    path: str
    children: List[Self]