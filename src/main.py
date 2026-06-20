"""
Startet die Anwendung mit:
    uvicorn src.main:app --reload --port 8000 oder .venv\Scripts\python.exe -m uvicorn src.main:app --reload --port 8000
    http://localhost:8000        
"""

from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from . import storage
from .importers import import_csv_text, import_json_text
from .models import UserStory
from .rules import classify_story, classify_text


def _load_example_data() -> None:
    try:
        with open("data/userstories_planner.csv", encoding="utf-8") as f:
            storage.add_stories(import_csv_text(f.read()))
    except FileNotFoundError:
        pass


app = FastAPI(
    title="Buendelungsfaecher-Zuordnung",
    description=(
        "Liest User Stories aus heterogenen Quellen (CSV, JSON) ein, "
        "ueberfuehrt sie in ein gemeinsames Modell und ordnet sie "
        "regelbasiert den Buendelungsfaechern SDM, EvP und GiD zu."
    ),
    version="1.0.0",
    on_startup=[_load_example_data],
)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.post("/import/csv", tags=["Import"])
def import_csv(file: UploadFile = File(...)) -> dict:
    if not (file.filename or "").endswith(".csv"):
        raise HTTPException(status_code=422, detail="Nur .csv-Dateien erlaubt.")
    inhalt = file.file.read().decode("utf-8")
    stories = import_csv_text(inhalt)
    storage.add_stories(stories)
    return {"importiert": len(stories), "gesamt_gespeichert": storage.count()}


@app.post("/import/json", tags=["Import"])
def import_json(file: UploadFile = File(...)) -> dict:
    if not (file.filename or "").endswith(".json"):
        raise HTTPException(status_code=422, detail="Nur .json-Dateien erlaubt.")
    inhalt = file.file.read().decode("utf-8")
    stories = import_json_text(inhalt)
    storage.add_stories(stories)
    return {"importiert": len(stories), "gesamt_gespeichert": storage.count()}


@app.get("/userstories", response_model=List[UserStory], tags=["UserStories"])
def alle_userstories() -> List[UserStory]:
    return storage.get_all()


@app.get("/userstories/{story_id}", response_model=UserStory, tags=["UserStories"])
def eine_userstory(story_id: str) -> UserStory:
    story = storage.get_by_id(story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="User Story nicht gefunden")
    return story


class ZuordnungsAnfrage(BaseModel):
    titel: str
    beschreibung: Optional[str] = ""
    tags: Optional[List[str]] = []


@app.post("/classify", tags=["Zuordnung"])
def klassifizieren(eingabe: ZuordnungsAnfrage) -> dict:
    return classify_text(eingabe.titel, eingabe.beschreibung, eingabe.tags)


@app.get("/userstories/{story_id}/classify", tags=["Zuordnung"])
def userstory_klassifizieren(story_id: str) -> dict:
    story = storage.get_by_id(story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="User Story nicht gefunden")
    return classify_story(story)