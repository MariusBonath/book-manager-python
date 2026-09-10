# =============================================================================
# configMod.py – Konfigurationsmodul
# =============================================================================
#
# Dieses Modul liest alle Einstellungen aus zwei Konfigurationsdateien:
#
#   config/FlashMob.ini   → Dateipfade (wo liegen die Daten?)
#   config/books.json     → Programmeinstellungen (Spaltenköpfe, Validierung …)
#
# Warum externe Konfigurationsdateien?
#   → Einstellungen können geändert werden, OHNE den Python-Code anzufassen.
#   → Dasselbe Programm könnte so z. B. Filme oder Kontakte verwalten,
#     indem man nur die JSON-Datei anpasst.
#
# Konzepte in dieser Datei:
#   - import (Standardbibliotheken json und configparser)
#   - Funktionen mit Rückgabewert (return)
#   - Typ-Annotationen (str, dict, list)
#   - Private Hilfsfunktion (Name beginnt mit _)
#   - with-Anweisung (öffnet Datei und schließt sie automatisch)
# =============================================================================


# -----------------------------------------------------------------------------
# Importe
# -----------------------------------------------------------------------------
# "json"         → liest JSON-Dateien (JavaScript Object Notation)
# "ConfigParser" → liest .ini-Dateien (Schlüssel-Wert-Paare in Abschnitten)

import json
import os
from configparser import ConfigParser


# -----------------------------------------------------------------------------
# Konstante: Pfad zur .ini-Datei
# -----------------------------------------------------------------------------
# Konstanten schreibt man in Python konventionell in GROSSBUCHSTABEN.
# Der führende Unterstrich "_" zeigt: diese Variable ist nur für dieses
# Modul gedacht (modul-privat).
#
# os.path.dirname(__file__) gibt den Ordner dieser Datei zurück.
# So funktioniert die Konfiguration auch, wenn das Programm von
# woanders gestartet wird.

_INI_PFAD = os.path.join(os.path.dirname(__file__), "config", "FlashMob.ini")


# -----------------------------------------------------------------------------
# .ini-Datei einlesen
# -----------------------------------------------------------------------------
# ConfigParser liest Dateien im Format:
#
#   [Abschnitt]
#   schluessel = wert
#
# Beispiel aus FlashMob.ini:
#   [Paths]
#   fpath = ./data/books/booklist.dat
#
# Nach config.read() kann man auf Werte so zugreifen:
#   config["Paths"]["fpath"]  →  "./data/books/booklist.dat"

_config = ConfigParser()
gelesene_dateien = _config.read(_INI_PFAD)

if not gelesene_dateien:
    # Konfigurationsdatei nicht gefunden → Fehler mit hilfreicher Meldung
    print(f"FEHLER: Konfigurationsdatei nicht gefunden: {_INI_PFAD}")
    print("Das Programm kann nicht starten.")
    exit(1)

if "Paths" not in _config:
    # Erforderliche Sektion fehlt
    print("FEHLER: Sektion [Paths] in der Konfigurationsdatei nicht gefunden.")
    exit(1)


# =============================================================================
# Private Hilfsfunktion
# =============================================================================

def _lade_json(pfad_json: str) -> dict:
    """
    Öffnet eine JSON-Datei und gibt den Inhalt als Python-Dictionary zurück.

    JSON-Dateien sehen so aus:
        {
            "header": ["no", "title", "author"],
            "col_widths": [6, 25, 25]
        }

    Python wandelt das automatisch in ein Dictionary (dict) um:
        {"header": ["no", "title", "author"], "col_widths": [6, 25, 25]}

    Der Unterstrich am Anfang (_lade_json) zeigt: Diese Funktion ist
    nur innerhalb dieses Moduls gedacht.

    Args:
        pfad_json: Dateipfad zur JSON-Datei als String.

    Returns:
        Ein Python-Dictionary mit allen JSON-Einstellungen.
    """
    # "with open(...) as f:" öffnet die Datei und schließt sie
    # am Ende des Blocks automatisch – auch bei einem Fehler.
    with open(pfad_json, "rt", encoding="utf-8") as f:
        return json.load(f)   # json.load liest die Datei und gibt ein dict zurück


# =============================================================================
# Öffentliche Funktionen – Dateipfade aus der .ini-Datei
# =============================================================================

def get_fpath() -> str:
    """
    Gibt den Pfad zur Pickle-Datei (.dat) zurück.
    Dort werden die Bücherdaten dauerhaft gespeichert.

    Returns:
        Pfad als String, z. B. "./data/books/booklist.dat"
    """
    return _config["Paths"]["fpath"]


def get_fpath_csv() -> str:
    """
    Gibt den Standard-Pfad für den CSV-Export zurück.

    Returns:
        Pfad als String, z. B. "./data/books/csv/booklist.csv"
    """
    return _config["Paths"]["fpath_csv"]


def get_fpath_json() -> str:
    """
    Gibt den Pfad zur JSON-Konfigurationsdatei zurück.

    Returns:
        Pfad als String, z. B. "./config/books.json"
    """
    return _config["Paths"]["fpath_json"]


# =============================================================================
# Öffentliche Funktionen – Einstellungen aus der JSON-Datei
# =============================================================================

def get_prompts(pfad_json: str) -> list:
    """
    Gibt die Eingabeaufforderungen für jedes Feld zurück.

    Beispiel-Rückgabe:
        ["Bitte Nr. eingeben: ", "Bitte Titel eingeben: ", ...]

    Args:
        pfad_json: Pfad zur JSON-Datei.

    Returns:
        Liste mit Eingabeaufforderungen (Strings).
    """
    return _lade_json(pfad_json)["prompts"]


def get_header(pfad_json: str) -> list:
    """
    Gibt die Spaltenüberschriften zurück.

    Beispiel-Rückgabe:
        ["no", "title", "genre", "author", "price", "date"]

    Args:
        pfad_json: Pfad zur JSON-Datei.

    Returns:
        Liste mit Spaltenüberschriften (Strings).
    """
    return _lade_json(pfad_json)["header"]


def get_col_widths(pfad_json: str) -> list:
    """
    Gibt die Spaltenbreiten für die Tabellenanzeige zurück.

    Beispiel-Rückgabe:
        [6, 25, 6, 25, 10, 8]
        → Spalte "no" ist 6 Zeichen breit,
          Spalte "title" ist 25 Zeichen breit, usw.

    Args:
        pfad_json: Pfad zur JSON-Datei.

    Returns:
        Liste mit Spaltenbreiten (Ganzzahlen).
    """
    return _lade_json(pfad_json)["col_widths"]


def get_format_specs(pfad_json: str) -> list:
    """
    Gibt die Validierungsregeln für jedes Eingabefeld zurück.

    Jede Regel ist eine Liste. Das erste Element ist das Schlüsselwort,
    weitere Elemente sind zusätzlich erlaubte Zeichen.

    Beispiel-Rückgabe:
        [["DIGIT"], ["ALL"], ["ALNUM", "-"], ["ALPHA", " ", "-"], ["FLOAT"], ["DIGIT"]]

    Bedeutung der Schlüsselwörter:
        "DIGIT" → nur Ziffern (0–9)
        "ALPHA" → nur Buchstaben (a–z, A–Z) + erlaubte Sonderzeichen
        "ALNUM" → Buchstaben und Ziffern + erlaubte Sonderzeichen
        "FLOAT" → eine gültige Dezimalzahl (z. B. "12.99")
        "ALL"   → beliebige Eingabe erlaubt

    Args:
        pfad_json: Pfad zur JSON-Datei.

    Returns:
        Liste von Validierungsregeln (jede Regel ist selbst eine Liste).
    """
    return _lade_json(pfad_json)["format_specs"]
