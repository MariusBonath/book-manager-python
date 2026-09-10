# =============================================================================
# ioMod.py – Datei-Ein-/Ausgabe-Hilfsmodul
# =============================================================================
#
# Dieses Modul enthält eine einzige Funktion: fopen().
# Sie öffnet eine Datei sicher – auch wenn das Verzeichnis noch nicht existiert.
#
# Warum ein eigenes Modul dafür?
#   → Fehlerbehandlung an einer zentralen Stelle
#   → Alle anderen Module rufen einfach io.fopen(...) auf
#     und müssen sich nicht selbst um fehlende Verzeichnisse kümmern
#
# Konzepte in dieser Datei:
#   - import os (Standardbibliothek für Betriebssystem-Operationen)
#   - try/except (Fehlerbehandlung / Exception Handling)
#   - Spezifische Ausnahmen (FileNotFoundError, OSError)
#   - os.path-Funktionen (Pfadoperationen)
#   - Typ-Annotationen
# =============================================================================


# -----------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------
# Das Modul "os" stellt Funktionen für das Betriebssystem bereit:
#   os.path.dirname()  → extrahiert den Verzeichnispfad aus einem Dateipfad
#   os.path.isdir()    → prüft, ob ein Verzeichnis existiert
#   os.makedirs()      → legt ein Verzeichnis an (inkl. Unterverzeichnisse)

import os


# =============================================================================
# Funktion: fopen
# =============================================================================

def fopen(fpath: str, mode: str):
    """
    Öffnet eine Datei sicher und gibt das Datei-Objekt zurück.

    Wenn die Datei oder das Verzeichnis noch nicht existiert,
    wird das Verzeichnis automatisch angelegt.

    Dateimodi (mode):
        "rb"  → lesen,   binär    (Pickle laden)
        "wb"  → schreiben, binär  (Pickle speichern)
        "rt"  → lesen,   Text     (CSV lesen)
        "w"   → schreiben, Text   (CSV schreiben)

    Args:
        fpath: Dateipfad als String, z. B. "./data/books/booklist.dat"
        mode:  Öffnungsmodus als String

    Returns:
        Ein geöffnetes Datei-Objekt, oder None bei einem Fehler.
    """

    # os.path.dirname() extrahiert den Ordner-Teil eines Dateipfads.
    # Beispiel: "./data/books/booklist.dat"  →  "./data/books"
    dirname = os.path.dirname(fpath)

    # -------------------------------------------------------------------------
    # Erster Öffnungsversuch
    # -------------------------------------------------------------------------
    # Normalfall: Die Datei existiert bereits → einfach öffnen.
    #
    # "b" not in mode prüft, ob der Modus Text oder Binär ist.
    # Bei Textdateien (rt, w) geben wir encoding="utf-8" an,
    # damit Umlaute (ä, ö, ü) korrekt gelesen/geschrieben werden.
    # Bei Binärdateien (rb, wb) darf encoding NICHT angegeben werden.

    try:
        return open(fpath, mode, encoding="utf-8" if "b" not in mode else None)

    except FileNotFoundError:
        # -----------------------------------------------------------------------
        # Datei nicht gefunden
        # -----------------------------------------------------------------------
        # Im Lesemodus ("rb", "rt") ist das normal → still None zurückgeben
        if "r" in mode:
            # Lesen aus nicht existierender Datei ist OK (z. B. beim ersten Start)
            return None

        # Im Schreibmodus ("wb", "w") → Verzeichnis anlegen und nochmal versuchen
        if dirname and not os.path.isdir(dirname):
            # os.makedirs legt alle fehlenden Unterordner auf einmal an.
            # exist_ok=True verhindert einen Fehler, falls der Ordner doch
            # schon existiert (z. B. durch einen anderen Prozess).
            os.makedirs(dirname, exist_ok=True)
            print(f"Verzeichnis angelegt: {dirname}")

        # Zweiter Öffnungsversuch (nach dem Anlegen des Verzeichnisses)
        try:
            return open(fpath, mode, encoding="utf-8" if "b" not in mode else None)
        except OSError as e:
            # OSError fängt alle weiteren Datei-Fehler ab
            # (z. B. keine Schreibrechte)
            print(f"Fehler beim Öffnen von '{fpath}': {e}")
            return None

    except OSError as e:
        # Anderer Fehler beim ersten Versuch (z. B. Pfad zu lang, Rechte fehlen)
        print(f"Fehler beim Öffnen von '{fpath}': {e}")
        return None
