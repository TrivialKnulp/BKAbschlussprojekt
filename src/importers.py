import csv
import io
import json
from typing import List

from .models import UserStory


def import_csv_text(text: str) -> List[UserStory]:
    reader = csv.DictReader(io.StringIO(text))
    stories: List[UserStory] = []

    for zeile in reader:
        tags_roh = zeile.get("Tags", "") or ""
        tags = [t.strip() for t in tags_roh.split(";") if t.strip()]

        story = UserStory(
            id=(zeile.get("ID") or "").strip(),
            titel=(zeile.get("Aufgabe") or "").strip(),
            beschreibung=(zeile.get("Beschreibung") or "").strip(),
            quelle="csv",
            prioritaet=(zeile.get("Prioritaet") or "mittel").strip() or "mittel",
            status=(zeile.get("Status") or "offen").strip() or "offen",
            tags=tags,
            zugewiesen_an=(zeile.get("ZugewiesenAn") or "").strip() or None,
            erstellt_am=(zeile.get("ErstelltAm") or "").strip() or None,
        )
        stories.append(story)

    return stories


def import_json_text(text: str) -> List[UserStory]:
    daten = json.loads(text)
    stories: List[UserStory] = []

    for eintrag in daten:
        story = UserStory(
            id=f"GH-{eintrag.get('number')}",
            titel=eintrag.get("title", ""),
            beschreibung=eintrag.get("body", ""),
            quelle="json",
            prioritaet=eintrag.get("priority", "mittel"),
            status=eintrag.get("status", "offen"),
            tags=list(eintrag.get("labels", [])),
            zugewiesen_an=eintrag.get("assignee"),
            erstellt_am=eintrag.get("created_at"),
        )
        stories.append(story)

    return stories
