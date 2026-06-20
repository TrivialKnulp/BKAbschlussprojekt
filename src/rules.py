"""
Rolle B: Fachlogik und Regelwerk.

Regelbasierte (keine KI!) Zuordnung einer User Story zu den
Buendelungsfaechern SDM, EvP und GiD anhand von Schluesselwoertern.
Jeder Treffer zaehlt 2 Punkte (= "starker Hinweis" laut Aufgabenstellung).
"""

from typing import Dict, List, Optional

from .models import UserStory

SDM_KEYWORDS = [
    "datenmodell", "feldzuordnung", "import", "json", "csv", "xml",
    "validierung", "datensatz", "struktur", "mapping",
]

EVP_KEYWORDS = [
    "api", "rest", "endpunkt", "anfrage", "antwort", "webhook",
    "workflow", "integration", "weiterverarbeitung",
]

GID_KEYWORDS = [
    "nutzer", "kunde", "dokumentation", "bedienung", "uebergabe",
    "beschreibung", "verstaendlich", "darstellung", "anleitung",
]


def _treffer(text: str, keywords: List[str]) -> List[str]:
    return [kw for kw in keywords if kw in text]


def classify_text(titel: str, beschreibung: str = "", tags: Optional[List[str]] = None) -> Dict:
    tags = tags or []
    text = " ".join([titel or "", beschreibung or "", " ".join(tags)]).lower()

    sdm_treffer = _treffer(text, SDM_KEYWORDS)
    evp_treffer = _treffer(text, EVP_KEYWORDS)
    gid_treffer = _treffer(text, GID_KEYWORDS)

    punkte = {
        "SDM": len(sdm_treffer) * 2,
        "EvP": len(evp_treffer) * 2,
        "GiD": len(gid_treffer) * 2,
    }
    begruendung = {
        "SDM": sdm_treffer,
        "EvP": evp_treffer,
        "GiD": gid_treffer,
    }

    gesamt_punkte = sum(punkte.values())
    if gesamt_punkte == 0:
        empfehlung = "keine klare Zuordnung moeglich"
    else:
        maximum = max(punkte.values())
        top_faecher = [fach for fach, p in punkte.items() if p == maximum]
        empfehlung = top_faecher[0] if len(top_faecher) == 1 else "Mischfall: " + " / ".join(top_faecher)

    return {
        "punkte": punkte,
        "begruendung": begruendung,
        "empfehlung": empfehlung,
    }


def classify_story(story: UserStory) -> Dict:
    return classify_text(story.titel, story.beschreibung, story.tags)
