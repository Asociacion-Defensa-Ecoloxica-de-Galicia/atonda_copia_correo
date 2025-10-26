from dataclasses import dataclass
from typing import Optional, List, Self
from slugify import slugify

@dataclass
class EmailData:
    source: Optional[str]
    destination: Optional[str]
    subject: Optional[str]
    date: Optional[str]
    #content: bytes
    @property
    def file_name(self):
        subject = str(self.subject) or ''
        subject = subject if len(subject) <= 150 else f'{subject[0:147]}...'
        return slugify(f'{subject}_{self.date}')

@dataclass
class FoldersTree:
    path: str
    children: List[Self]