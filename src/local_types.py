from dataclasses import dataclass
from typing import Optional, List, Self

@dataclass
class EmailData:
    source: Optional[str]
    destination: Optional[str]
    subject: Optional[str]
    date: Optional[str]
    msg_id: Optional[str]
    content: str
    @property
    def file_name(self):
        return f'from_{self.source}_to_{self.destination}_{self.subject}_{self.date}'

@dataclass
class FoldersTree:
    path: str
    children: List[Self]