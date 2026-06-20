# Buendelungsfaecher-Zuordnung

Ein kleiner Dienst, der User Stories aus heterogenen Quellen (CSV und
JSON) einliest, in ein gemeinsames Datenmodell ueberfuehrt und sie
regelbasiert den Buendelungsfaechern **SDM**, **EvP** und **GiD**
zuordnet. Die Anwendung wird ausschliesslich ueber die automatisch
generierte Swagger-Oberflaeche bedient.

- **Startseite:**  
  `http://localhost:8000` → Weiterleitung zu Swagger UI

## Was funktioniert

- Import von CSV-Dateien im Planner-Format (`POST /import/csv`)
- Import von JSON-Dateien im GitHub-Issues-Format (`POST /import/json`)
- Abruf aller bzw. einzelner User Stories im gemeinsamen Modell
- Regelbasierte Zuordnung zu SDM, EvP, GiD — sowohl fuer bereits
  importierte User Stories als auch fuer frei eingegebenen Text

## Projektstruktur

```
team-projekt/
├─ data/
│  ├─ userstories_planner.csv      Beispiel-Quelle CSV
│  └─ userstories_github.json      Beispiel-Quelle JSON
├─ src/
│  ├─ models.py        gemeinsames Datenmodell (UserStory)
│  ├─ importers.py      CSV/JSON einlesen + Mapping
│  ├─ rules.py          Regelwerk SDM/EvP/GiD
│  ├─ storage.py        einfacher In-Memory-Speicher
│  └─ main.py           FastAPI-Endpunkte

