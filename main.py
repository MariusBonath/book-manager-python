# =============================================================================
# main.py – Einstiegspunkt des Book Manager
# =============================================================================
#
# Dieses Modul ist der Startpunkt des Programms.
# Es verbindet alle anderen Module miteinander und steuert
# die Hauptschleife (Menü).
#
# Ablauf:
#   1. Konfiguration laden  (configMod)
#   2. Datenobjekt anlegen  (listclassMod → Listclass)
#   3. Menü anzeigen + Nutzereingabe auswerten
#
# Konzepte in dieser Datei:
#   - Modulimporte
#   - Variablen und Funktionsaufrufe
#   - while-Schleife (Endlosschleife mit break)
#   - if/elif/else (Mehrfachverzweigung)
# =============================================================================


# -----------------------------------------------------------------------------
# Importe
# -----------------------------------------------------------------------------
# Wir importieren unsere eigenen Module mit einem kurzen Alias (z. B. "cfg"),
# damit der Code kürzer und lesbarer wird.

import listclassMod as lcm   # enthält die Klasse Listclass
import configMod    as cfg   # liest Einstellungen aus .ini- und .json-Dateien
import editMod      as em    # enthält Hilfsfunktionen für Eingabe und Löschen


# -----------------------------------------------------------------------------
# Konfiguration laden
# -----------------------------------------------------------------------------
# configMod liest zwei Konfigurationsdateien:
#   config/FlashMob.ini  → Dateipfade
#   config/books.json    → Spaltenköpfe, Eingabeaufforderungen, Validierungsregeln

path_json    = cfg.get_fpath_json()              # Pfad zur JSON-Datei

prompts      = cfg.get_prompts(path_json)        # Eingabeaufforderungen (z. B. "Titel: ")
format_specs = cfg.get_format_specs(path_json)   # Validierungsregeln    (z. B. ["ALL"])
col_widths   = cfg.get_col_widths(path_json)     # Spaltenbreiten für die Tabellenanzeige
header       = cfg.get_header(path_json)         # Spaltenüberschriften  (z. B. "title")

fpath     = cfg.get_fpath()                      # Pfad zur Speicherdatei (.dat)
fpath_csv = cfg.get_fpath_csv()                  # Pfad zur CSV-Datei


# -----------------------------------------------------------------------------
# Datenobjekt anlegen
# -----------------------------------------------------------------------------
# Wir erstellen ein Objekt der Klasse Listclass.
# Der Konstruktor (__init__) lädt beim Start automatisch vorhandene Daten.

lco = lcm.Listclass(fpath)   # lco = "list class object"


# -----------------------------------------------------------------------------
# Menü-Text (Konstante)
# -----------------------------------------------------------------------------
# MENU ist eine Konstante (wird nie verändert).
# Triple-Anführungszeichen (""") erlauben mehrzeilige Strings.

MENU = """
========================================
        BOOK MANAGER
========================================
  e - Eintrag hinzufügen
  l - Alle Bücher anzeigen
  f - Suchen
  s - Speichern
  o - Nach Titel sortieren
  c - Als CSV exportieren
  i - CSV importieren
  n - An freier Stelle einfügen
  d - Eintrag löschen
  x - Beenden
========================================"""


# -----------------------------------------------------------------------------
# Hauptschleife
# -----------------------------------------------------------------------------
# "while True" erzeugt eine Endlosschleife.
# Das Programm läuft so lange, bis der Nutzer "x" eingibt
# und wir die Schleife mit "break" verlassen.

while True:

    print(MENU)
    choice = input("Deine Wahl: ").strip().lower()
    # .strip()  → entfernt Leerzeichen am Anfang und Ende
    # .lower()  → wandelt Großbuchstaben in Kleinbuchstaben um
    #             "E" und "e" werden so gleich behandelt

    # -------------------------------------------------------------------------
    # Auswertung der Nutzereingabe
    # -------------------------------------------------------------------------

    if choice == "e":
        # Neuen Eintrag hinzufügen (Endlosschleife in edit_list,
        # quit() zum Beenden)
        lco.edit_list(prompts, format_specs)

    elif choice == "l":
        # Alle Bücher als formatierte Tabelle anzeigen
        lco.show_list(col_widths, header)

    elif choice == "f":
        # Volltextsuche über alle Felder
        lco.search_item(col_widths, header)

    elif choice == "s":
        # Daten in die .dat-Datei (Pickle) speichern
        lco.save_list()

    elif choice == "o":
        # Sortierung nach Titel (Spalte 1), Originalliste bleibt unverändert
        sorted_data = lco.sort_list(col=1)
        lco.show_list(col_widths, header, daten=sorted_data)

    elif choice == "c":
        # CSV-Export in die vorkonfigurierte Datei
        lco.export2csv(fpath_csv, header)

    elif choice == "i":
        # CSV-Import: Nutzer gibt den Dateipfad ein
        # Warnung: Import ersetzt die aktuelle Liste
        if lco._list:
            warnung = input("[!] Die aktuelle Liste wird ersetzt. Fortfahren? (J/N): ")
            if warnung.upper() != "J":
                print("Import abgebrochen.")
                continue
        import_path = input("Pfad zur CSV-Datei: ").strip()
        lco.import_csv(import_path)

    elif choice == "n":
        # Eintrag an der ersten freien Nummern-Lücke einfügen
        em.insert_sublist(lco, prompts, format_specs)

    elif choice == "d":
        # Eintrag löschen (mit Bestätigungsabfrage)
        em.delete_sublist(lco)

    elif choice == "x":
        # Programm sauber beenden
        # Erinnerung: Daten speichern nicht vergessen
        if lco._list:
            print("[*] Hinweis: Vergiss nicht, deine Aenderungen zu speichern (Taste 's')!")
        print("Auf Wiedersehen!")
        break   # verlässt die while-Schleife

    else:
        # Alles, was oben nicht abgedeckt wurde
        print("Unbekannte Eingabe. Bitte erneut versuchen.")
