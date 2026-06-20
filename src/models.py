"""
Gemeinsames Datenmodell fuer User Stories.

Egal aus welcher Quelle (CSV oder JSON) eine User Story stammt,
am Ende liegt sie in genau dieser Form vor.
"""

from typing import List, Optional
from pydantic import BaseModel


class UserStory(BaseModel):
    id: str
    titel: str
    beschreibung: Optional[str] = ""
    quelle: str                         # "csv" oder "json"
    prioritaet: Optional[str] = "mittel"
    status: Optional[str] = "offen"
    tags: List[str] = []
    zugewiesen_an: Optional[str] = None
    erstellt_am: Optional[str] = None
