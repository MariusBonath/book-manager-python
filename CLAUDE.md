# CLAUDE.md – Book Manager

## Projekt-Überblick

Kommandozeilenbasierte Bücherverwaltung in Python.
Entwickelt im Rahmen einer Umschulung zum Fachinformatiker Anwendungsentwicklung (IHK) am CBW Hamburg.

## Technisches Setup

- **Sprache:** Python 3.10+
- **Externe Pakete:** keine (nur Standardbibliothek)
- **Starten:** `python main.py`
- **Testdaten laden:** Menüpunkt `i` → `./data/books/csv/booklist.csv`

## Projektstruktur

```
main.py           → Einstiegspunkt, Menü-Schleife
listclassMod.py   → Klasse Listclass (alle Datenoperationen)
editMod.py        → Eingabe-Validierung, Löschen, Einfügen
ioMod.py          → Sicheres Öffnen von Dateien
configMod.py      → Konfiguration aus .ini und .json laden

config/
  FlashMob.ini    → Dateipfade
  books.json      → Spalten, Prompts, Validierungsregeln

data/books/
  booklist.dat    → Pickle-Speicherdatei (wird beim ersten Speichern erzeugt)
  csv/booklist.csv → Beispieldaten (5 Bücher)
```

## Architektur

- **Datenhaltung:** `self._list` in `Listclass` — 2D-Liste, jede innere Liste = ein Datensatz
- **Persistenz:** Python `pickle` (binär), CSV für Import/Export
- **Konfiguration:** `FlashMob.ini` für Pfade, `books.json` für Programmeinstellungen
- **Validierung:** Regelbasiert — DIGIT, ALPHA, ALNUM, FLOAT, ALL (in `editMod.py`)

## Wichtige Entscheidungen

- `csv.writer` statt manueller String-Konkatenation (korrektes Escaping bei Sonderzeichen)
- Spezifische Exception-Handler (`FileNotFoundError`, `OSError`) — kein blindes `except:`
- FLOAT-Validierung auf den ganzen String, nicht zeichenweise

## Kommentierungsstil

Alle Dateien sind **anfänger- und unterrichtsfreundlich** auf Deutsch kommentiert.
Jedes Python-Konzept wird an der Stelle erklärt, wo es verwendet wird.
Kommentare beibehalten und bei neuen Funktionen im gleichen Stil weiterführen.

## Benutzer-Kontext

- **Name:** Marius Bonath
- **GitHub:** github.com/MariusBonath
- **Zweck:** Portfolio-Projekt für Praktikumsbewerbung als Fachinformatiker AE
- **Niveau:** Umschüler, ca. 1 Jahr Python-Erfahrung
- **Sprache:** Deutsch bevorzugt (Code-Kommentare, Erklärungen, Commit-Messages)

## Konventionen

- Variablennamen auf Deutsch (z.B. `eingabe`, `kopfzeile`, `trennlinie`)
- Docstrings auf Deutsch mit Args / Returns
- Keine Übertreibungen bei Kompetenzen — realistisch und ehrlich bleiben
- Neue Features nur hinzufügen wenn sie dem aktuellen Ausbildungsstand entsprechen
