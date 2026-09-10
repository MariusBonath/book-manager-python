# Book Manager – Bücherverwaltung

Eine kommandozeilenbasierte Bücherdatenbank in Python.  
Erstellt im Rahmen meiner **Umschulung zum Fachinformatiker Anwendungsentwicklung (IHK)** am CBW Hamburg.

---

## Inhalt

- [Funktionen](#funktionen)
- [Projektstruktur](#projektstruktur)
- [Schnellstart](#schnellstart)
- [Bedienung](#bedienung)
- [Konfiguration](#konfiguration)
- [Technische Konzepte](#technische-konzepte)
- [Beispieldaten](#beispieldaten)

---

## Funktionen

| Taste | Funktion | Beschreibung |
|-------|----------|--------------|
| `e` | Eintrag hinzufügen | Felder nacheinander eingeben, Nummer wird automatisch vergeben |
| `l` | Liste anzeigen | Alle Bücher als formatierte Tabelle |
| `f` | Suchen | Stichwortsuche über alle Felder, Groß-/Kleinschreibung ignoriert |
| `s` | Speichern | Daten dauerhaft als Pickle-Datei sichern |
| `o` | Sortieren | Alphabetisch nach Titel sortieren und anzeigen |
| `c` | CSV-Export | Alle Einträge in eine CSV-Datei exportieren |
| `i` | CSV-Import | Datensätze aus einer CSV-Datei laden |
| `n` | Einfügen | Neuen Eintrag an der ersten freien Stelle einfügen (Nummer automatisch) |
| `d` | Löschen | Eintrag nach Bestätigung löschen |
| `x` | Beenden | Programm beenden |

---

## Projektstruktur

```
book-manager-python/
│
├── main.py              # Einstiegspunkt: Konfiguration laden, Menü-Schleife
├── listclassMod.py      # Klasse Listclass: alle Datenoperationen (OOP)
├── editMod.py           # Eingabe, Validierung, Löschen, Einfügen
├── ioMod.py             # Sicheres Öffnen von Dateien (Fehlerbehandlung)
├── configMod.py         # Konfiguration aus .ini- und .json-Dateien laden
│
├── config/
│   ├── FlashMob.ini     # Dateipfade (Datenbankdatei, CSV, JSON)
│   └── books.json       # Spaltenköpfe, Eingabeaufforderungen, Validierungsregeln
│
└── data/
    └── books/
        ├── booklist.dat         # Pickle-Datei (wird beim ersten Speichern erzeugt)
        └── csv/
            └── booklist.csv     # Beispiel-CSV mit fünf Büchern
```

### Modulübersicht

```
main.py
  │
  ├── configMod.py   → liest FlashMob.ini und books.json
  ├── listclassMod.py
  │     ├── ioMod.py        → öffnet Dateien sicher
  │     └── editMod.py      → Eingabe und Validierung
  └── editMod.py     → Löschen und Einfügen (direkt)
```

---

## Schnellstart

**Voraussetzung:** Python 3.10 oder neuer, keine externen Pakete nötig.

```bash
# Repository klonen
git clone https://github.com/MariusBonath/book-manager-python.git
cd book-manager-python

# Programm starten
python main.py
```

Das Programm startet mit einer leeren Liste.  
Um die Beispieldaten zu laden: Taste `i` drücken, dann diesen Pfad eingeben:

```
./data/books/csv/booklist.csv
```

---

## Bedienung

### Bücher anzeigen

```
Taste: l
```

```
+------+-------------------------+------+-------------------------+----------+--------+
|no    |title                    |genre |author                   |price     |date    |
+------+-------------------------+------+-------------------------+----------+--------+
|001   |Dracula                  |007   |Bram Stocker             |222       |1897    |
|002   |Pippi Langstrumpf        |005   |Astrid Lindgren          |100       |1949    |
+------+-------------------------+------+-------------------------+----------+--------+
```

### Buch hinzufügen

```
Taste: e
```

Die Nummern werden automatisch vergeben. Zum Beenden der Eingabe `quit()` eingeben.

### Suchen

```
Taste: f
Suchbegriff eingeben: Stocker
→ findet alle Einträge, die "Stocker" in irgendeinem Feld enthalten
```

### Daten speichern

```
Taste: s
→ speichert alle Einträge in data/books/booklist.dat (Pickle-Format)
→ beim nächsten Start werden die Daten automatisch geladen
```

---

## Sicherheitshinweis

Das Programm speichert Bücher im **Pickle-Format** (`booklist.dat`). Pickle kann beliebigen Python-Code ausführen.  
**Wichtig:** Nur `booklist.dat`-Dateien laden, die du selbst mit diesem Programm erstellt hast. Lade niemals Pickle-Dateien von unbekannten Quellen.

---

## Konfiguration

Das Programm ist ohne Code-Änderungen anpassbar.

### `config/FlashMob.ini` – Dateipfade

```ini
[Paths]
fpath      = ./data/books/booklist.dat   ; Speicherdatei (Pickle)
fpath_csv  = ./data/books/csv/booklist.csv
fpath_json = ./config/books.json
```

### `config/books.json` – Felder und Validierung

```json
{
  "header":      ["no", "title", "genre", "author", "price", "date"],
  "col_widths":  [6, 25, 6, 25, 10, 8],
  "prompts":     ["Bitte Nr. eingeben: ", "Bitte Titel eingeben: ", ...],
  "format_specs": [
    ["DIGIT"],
    ["ALL"],
    ["ALNUM", "-"],
    ["ALPHA", " ", "-", "&", ".", "'"],
    ["FLOAT"],
    ["DIGIT"]
  ]
}
```

#### Validierungsregeln (`format_specs`)

| Schlüsselwort | Bedeutung |
|---------------|-----------|
| `"DIGIT"` | Nur Ziffern (0–9) |
| `"ALPHA"` | Nur Buchstaben + zusätzliche Sonderzeichen |
| `"ALNUM"` | Buchstaben und Ziffern + Sonderzeichen |
| `"FLOAT"` | Gültige Dezimalzahl (z. B. `12.99`) |
| `"ALL"` | Beliebige Eingabe erlaubt |

Zusätzliche erlaubte Zeichen werden als weitere Elemente in der Liste angegeben:  
`["ALPHA", " ", "-", "&"]` → Buchstaben, Leerzeichen, Bindestrich und & erlaubt.

---

## Technische Konzepte

Dieses Projekt demonstriert folgende Inhalte aus der Umschulung:

### Objektorientierte Programmierung (OOP)
- `Listclass` kapselt alle Datenoperationen in einer Klasse
- Konstruktor `__init__` lädt beim Start automatisch vorhandene Daten
- Private Methoden (`_lade_liste`, `_tabelle_ausgeben`) trennen interne Logik von der öffentlichen Schnittstelle

### Modulare Architektur
- Jede Datei hat eine klar abgegrenzte Aufgabe
- `main.py` kennt nur die öffentliche Schnittstelle der anderen Module
- Konfiguration liegt vollständig außerhalb des Codes

### Datei-I/O
- **Pickle** (`pickle.dump` / `pickle.load`) für binäre Persistenz
- **CSV** (`csv.writer` / `csv.reader`) für den Datenaustausch
- Zentrales `ioMod.fopen()` mit Fehlerbehandlung und automatischer Verzeichniserstellung

### Fehlerbehandlung
- Spezifische `except`-Blöcke (`FileNotFoundError`, `OSError`)
- Kein blindes `except:` ohne Fehlertyp

### Eingabevalidierung
- Regelbasiertes System: `DIGIT`, `ALPHA`, `ALNUM`, `FLOAT`, `ALL`
- Sonderzeichen pro Feld konfigurierbar
- Endlosschleife bis zur gültigen Eingabe

### Weitere Python-Konzepte
- **Lambda-Ausdruck** für die Sortierung: `key=lambda zeile: zeile[col]`
- **List Comprehension** für die Suche
- **`any()`** für die Prüfung über alle Felder
- **f-Strings** mit Formatangaben (`:<width>`, `:03`)
- **`with`-Anweisung** für sicheres Öffnen und Schließen von Dateien
- **Typ-Annotationen** (`str`, `list`, `int`, `bool`, `None`)

---

## Beispieldaten

Die Datei `data/books/csv/booklist.csv` enthält fünf Beispielbücher:

| Nr. | Titel | Genre | Autor | Preis | Jahr |
|-----|-------|-------|-------|-------|------|
| 001 | Dracula | 007 | Bram Stocker | 222 | 1897 |
| 002 | Pippi Langstrumpf | 005 | Astrid Lindgren | 100 | 1949 |
| 003 | Chemie des Todes | 004 | Simon Becket | 15 | 2006 |
| 004 | Frankenstein | 007 | Mary Shelley | 1000 | 1818 |
| 005 | Faust | 002 | J.W.v.Goethe | 200 | 1808 |

Import über Menü `i`, Pfad: `./data/books/csv/booklist.csv`

---

## Autor

**Marius Bonath**  
Umschulung: Fachinformatiker Anwendungsentwicklung (IHK) · CBW Hamburg · 2025–2027  
GitHub: [github.com/MariusBonath](https://github.com/MariusBonath)
