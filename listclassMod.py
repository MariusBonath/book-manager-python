# =============================================================================
# listclassMod.py – Kerndaten-Modul (Listclass)
# =============================================================================
#
# Dieses Modul enthält die Klasse "Listclass" – das Herzstück des Programms.
# Sie verwaltet die Bücherliste und stellt alle Operationen darauf bereit:
#   - Laden und Speichern (Pickle)
#   - Anzeigen als formatierte Tabelle
#   - Suchen
#   - Sortieren
#   - CSV-Export und CSV-Import
#   - Eintrag prüfen, löschen, einfügen
#
# Konzepte in dieser Datei:
#   - Klassen (class) und Objekte
#   - Konstruktor (__init__)
#   - Instanzvariablen (self.fpath, self._list)
#   - Private Methoden (Name beginnt mit _)
#   - Öffentliche Methoden (Public Interface)
#   - Pickle (binäres Speichern von Python-Objekten)
#   - CSV (kommagetrennte Textdateien)
#   - f-Strings und Formatierung (:<width>)
#   - List Comprehension
#   - Lambda-Ausdruck (für Sortierung)
#   - Generator-Ausdruck (any())
# =============================================================================


# -----------------------------------------------------------------------------
# Importe
# -----------------------------------------------------------------------------
# "csv"    → liest und schreibt CSV-Dateien (kommagetrennte Werte)
# "pickle" → speichert Python-Objekte binär auf der Festplatte

import csv
import pickle

# Unsere eigenen Hilfsmodule importieren
import editMod as em   # Eingabe und Validierung
import ioMod   as iom  # sicheres Öffnen von Dateien (Alias: iom statt io, um Standardmodul nicht zu überdecken)


# =============================================================================
# Klasse: Listclass
# =============================================================================

class Listclass:
    """
    Verwaltet eine Bücherliste als 2D-Liste (Liste von Sublisten).

    Interne Datenstruktur:
        self._list ist eine Liste von Listen (2-dimensional):

        [
            ["001", "Dracula",           "007", "Bram Stocker",   "222",  "1897"],
            ["002", "Pippi Langstrumpf", "005", "Astrid Lindgren","100",  "1949"],
            ["003", "Frankenstein",      "007", "Mary Shelley",   "1000", "1818"],
        ]

        Jede innere Liste = ein Buch (Datensatz / Sublist)
        Jedes Element     = ein Feld  (z. B. Titel, Autor, Preis)
    """

    # =========================================================================
    # Konstruktor
    # =========================================================================

    def __init__(self, fpath: str) -> None:
        """
        Wird automatisch aufgerufen, wenn ein Listclass-Objekt erstellt wird.
        Lädt sofort vorhandene Daten aus der Pickle-Datei.

        Beispiel:
            lco = Listclass("./data/books/booklist.dat")
            → lco._list enthält alle gespeicherten Bücher

        Args:
            fpath: Pfad zur Pickle-Datei (.dat) als String.
        """
        # Instanzvariablen: mit "self." sind sie im gesamten Objekt verfügbar
        self.fpath = fpath            # Speicherpfad merken
        self._list = self._lade_liste()  # Daten sofort beim Start laden


    # =========================================================================
    # Private Hilfsmethoden (interner Gebrauch)
    # =========================================================================
    # Namen mit führendem Unterstrich (_) sind konventionell "privat" –
    # sie sollen von außen nicht direkt aufgerufen werden.

    def _lade_liste(self) -> list:
        """
        Lädt die Bücherliste aus der Pickle-Datei.

        Pickle ist ein Python-spezifisches Binärformat.
        Es kann beliebige Python-Objekte speichern und laden –
        hier eine Liste von Listen.

        Returns:
            Die geladene Liste, oder eine leere Liste [] wenn
            die Datei noch nicht existiert oder beschädigt ist.
        """
        datei = iom.fopen(self.fpath, "rb")   # "rb" = read binary

        if datei is None:
            # Datei existiert noch nicht → leere Liste zurückgeben
            return []

        # "with datei:" schließt die Datei automatisch am Ende des Blocks
        try:
            with datei:
                return pickle.load(datei)   # Python-Objekt aus Binärdatei laden
        except (EOFError, pickle.UnpicklingError):
            # Speicherdatei beschädigt oder leer → leere Liste zurückgeben
            print("[!] Warnung: Speicherdatei beschaedigt. Starte mit leerer Liste.")
            return []


    def _tabelle_ausgeben(self, daten: list, spaltenbreiten: list, kopfzeile: list) -> None:
        """
        Gibt eine Liste von Datensätzen als formatierte Tabelle aus.

        Beispielausgabe:
            +------+-------------------------+------+
            |no    |title                    |genre |
            +------+-------------------------+------+
            |001   |Dracula                  |007   |
            +------+-------------------------+------+

        Wie die Formatierung funktioniert:
            f"{wert:<{breite}}"
              ^        ^
              |        Spaltenbreite (variable Breite per f-String)
              linksbündig ausrichten

        Args:
            daten:         Die anzuzeigende Liste (Liste von Sublisten).
            spaltenbreiten: Breite jeder Spalte in Zeichen.
            kopfzeile:     Spaltenüberschriften.
        """

        # Trennlinie bauen: "+------+-------------------------+..."
        # Beispiel: col_widths = [6, 25] → "+------+-------------------------+"
        trennlinie = "+" + "+".join("-" * b for b in spaltenbreiten) + "+"
        #                          ↑ für jede Breite b: b mal "-"

        # Kopfzeile bauen: "|no    |title                    |..."
        kopfzeilen_str = "|" + "|".join(
            f"{h:<{spaltenbreiten[i]}}"   # linksbündig in Spaltenbreite
            for i, h in enumerate(kopfzeile)
        ) + "|"

        # Ausgabe: Trennlinie – Kopfzeile – Trennlinie – Daten – Trennlinie
        print(trennlinie)
        print(kopfzeilen_str)
        print(trennlinie)

        for zeile in daten:
            # Jede Spalte auf die korrekte Breite bringen
            # Zu lange Werte werden gekürzt, um die Tabelle nicht zu sprengen
            datenzeile = "|" + "|".join(
                f"{str(zeile[i])[:spaltenbreiten[i]]:<{spaltenbreiten[i]}}"
                for i in range(len(zeile))
            ) + "|"
            print(datenzeile)

        print(trennlinie)


    # =========================================================================
    # Öffentliche Methoden (Public Interface)
    # =========================================================================
    # Diese Methoden werden von main.py und editMod.py aufgerufen.

    # -------------------------------------------------------------------------
    # Einträge hinzufügen
    # -------------------------------------------------------------------------

    def edit_list(self, prompts: list, format_specs: list) -> None:
        """
        Ermöglicht das interaktive Hinzufügen neuer Bücher.

        Die Nummern (erstes Feld) werden automatisch vergeben.
        Die Schleife läuft, bis der Nutzer "quit()" eingibt.

        Ablauf pro Buch:
            1. Nummer automatisch berechnen (letzter Eintrag + 1)
            2. Alle anderen Felder nacheinander abfragen
            3. Datensatz an die Liste anhängen

        Args:
            prompts:      Liste mit Eingabeaufforderungen.
            format_specs: Liste mit Validierungsregeln.
        """
        while True:
            sublist = []   # leere Liste für den neuen Datensatz

            for i in range(len(prompts)):

                if i == 0:
                    # Erste Spalte = Nummer → automatisch vergeben
                    try:
                        if self._list:
                            # Letzte Nummer validieren + 1, formatiert mit 3 Stellen
                            letzte_nr = int(self._list[-1][0])
                            naechste_nr = f"{letzte_nr + 1:03}"
                        else:
                            naechste_nr = "001"   # Liste ist leer → mit 001 starten
                    except (ValueError, IndexError):
                        # Beschädigte Nummer in letztem Eintrag → Fehlerbehandlung
                        print("[!] Fehler in der letzten Nummer. Setze Zaehler zurueck.")
                        naechste_nr = "001"
                    sublist.append(naechste_nr)
                    continue   # Nummer nicht abfragen, direkt zum nächsten Feld

                # Feld abfragen und validieren
                eingabe = em.edit_item(prompts[i], format_specs[i])

                if eingabe == "quit()":
                    # Nutzer möchte aufhören → Methode verlassen
                    return

                sublist.append(eingabe)

            # Kompletten Datensatz an die Liste anhängen
            self._list.append(sublist)


    # -------------------------------------------------------------------------
    # Liste anzeigen
    # -------------------------------------------------------------------------

    def show_list(self, spaltenbreiten: list, kopfzeile: list, daten: list = None) -> None:
        """
        Zeigt alle Bücher (oder eine übergebene Teilliste) als Tabelle an.

        Der Parameter "daten" hat den Standardwert None.
        Wenn nichts übergeben wird → gesamte interne Liste anzeigen.
        Wenn eine Liste übergeben wird (z. B. Suchergebnis) → diese anzeigen.

        Args:
            spaltenbreiten: Breite jeder Spalte.
            kopfzeile:      Spaltenüberschriften.
            daten:          Optionale Teilliste. Standard: None (= alle Einträge).
        """
        # Quelle bestimmen: übergebene Daten oder interne Liste
        quelle = daten if daten is not None else self._list

        if not quelle:
            # Leere Liste → Hinweis ausgeben
            print("Keine Einträge vorhanden.")
            return

        self._tabelle_ausgeben(quelle, spaltenbreiten, kopfzeile)


    # -------------------------------------------------------------------------
    # Suchen
    # -------------------------------------------------------------------------

    def search_item(self, spaltenbreiten: list, kopfzeile: list) -> None:
        """
        Durchsucht alle Felder aller Datensätze nach einem Stichwort.
        Groß-/Kleinschreibung wird dabei ignoriert.

        Wie die Suche funktioniert:
            List Comprehension + any():

            ergebnisse = [
                zeile
                for zeile in self._list
                if any(stichwort.lower() in str(feld).lower() for feld in zeile)
            ]

            → Für jede Zeile: Prüfe mit any(), ob das Stichwort
              in mindestens einem Feld vorkommt.
            → any() gibt True zurück, sobald eine Bedingung erfüllt ist.

        Args:
            spaltenbreiten: Spaltenbreiten für die Ausgabe.
            kopfzeile:      Spaltenüberschriften.
        """
        stichwort = input("Suchbegriff eingeben: ").strip()

        if not stichwort:
            print("Suchbegriff darf nicht leer sein.")
            return

        # List Comprehension: alle Zeilen filtern, die das Stichwort enthalten
        ergebnisse = [
            zeile
            for zeile in self._list
            if any(stichwort.lower() in str(feld).lower() for feld in zeile)
            # str(feld)   → Feld als String (auch Zahlen werden so vergleichbar)
            # .lower()    → Groß-/Kleinschreibung ignorieren
        ]

        if ergebnisse:
            print(f"\n{len(ergebnisse)} Ergebnis(se) für '{stichwort}':\n")
            self._tabelle_ausgeben(ergebnisse, spaltenbreiten, kopfzeile)
        else:
            print(f"Keine Ergebnisse für '{stichwort}' gefunden.")


    # -------------------------------------------------------------------------
    # Speichern
    # -------------------------------------------------------------------------

    def save_list(self) -> None:
        """
        Speichert die gesamte Bücherliste in der Pickle-Datei.

        Pickle konvertiert das Python-Objekt (self._list) in Binärdaten
        und schreibt sie auf die Festplatte.
        Beim nächsten Programmstart kann pickle.load() die Daten
        exakt wiederherstellen.
        """
        datei = iom.fopen(self.fpath, "wb")   # "wb" = write binary

        if datei is None:
            print("Datei konnte nicht zum Speichern geöffnet werden.")
            return

        # "with datei:" schließt die Datei automatisch
        with datei:
            pickle.dump(self._list, datei)   # Liste als Binärdaten schreiben

        print("Daten erfolgreich gespeichert.")


    # -------------------------------------------------------------------------
    # Sortieren
    # -------------------------------------------------------------------------

    def sort_list(self, col: int, update_self: bool = False) -> list:
        """
        Sortiert die Bücherliste nach einer bestimmten Spalte.

        Wie sorted() mit Lambda funktioniert:
            sorted(liste, key=lambda zeile: zeile[col])

            - sorted() gibt eine NEU sortierte Kopie zurück
            - key=...  gibt an, nach welchem Wert sortiert wird
            - lambda zeile: zeile[col]
                → anonyme Funktion: nimmt eine Zeile und gibt Spalte [col] zurück
            - Die Original-Liste bleibt standardmäßig unverändert

        Sortierlogik:
            - Für Spalten mit numerischen Werten (Nummer, Preis, Jahr):
              wird numerisch sortiert → "100" kommt vor "222"
            - Für Text-Spalten (Titel, Autor):
              wird alphabetisch sortiert

        Beispiel:
            sort_list(col=0)  → nach Nummer (numerisch)
            sort_list(col=1)  → nach Titel (alphabetisch)
            sort_list(col=4)  → nach Preis (numerisch)

        Args:
            col:         Spaltenindex, nach dem sortiert wird (0 = Nummer, 1 = Titel …).
            update_self: Wenn True, wird auch die interne Liste aktualisiert.

        Returns:
            Die sortierte Liste (Kopie).
        """
        # Hilfsfunktion: versucht, als Zahl zu sortieren, fallback zu String
        def sort_key(zeile):
            wert = zeile[col]
            try:
                # Versuche als Zahl zu interpretieren (funktioniert für "100", "12.5", etc.)
                if "." in str(wert):
                    return (0, float(wert))   # (0, Zahl) → Zahlen zuerst
                else:
                    return (0, int(wert))
            except ValueError:
                # Nicht numerisch → als String sortieren
                return (1, str(wert).lower())  # (1, String) → Strings nach Zahlen

        sortiert = sorted(self._list, key=sort_key)

        if update_self:
            # Interne Liste ersetzen (Sortierung dauerhaft übernehmen)
            self._list = sortiert

        return sortiert


    # -------------------------------------------------------------------------
    # CSV-Export
    # -------------------------------------------------------------------------

    def export2csv(self, fpath_csv: str, kopfzeile: list) -> None:
        """
        Exportiert alle Bücher in eine CSV-Datei.

        CSV (Comma-Separated Values) ist ein einfaches Textformat:
            no,title,genre,author,price,date
            001,Dracula,007,Bram Stocker,222,1897
            002,Pippi Langstrumpf,005,Astrid Lindgren,100,1949

        csv.writer übernimmt das korrekte Escaping (z. B. bei Feldern
        mit Kommas oder Anführungszeichen).

        Args:
            fpath_csv: Pfad zur Ziel-CSV-Datei.
            kopfzeile: Spaltenüberschriften für die erste Zeile.
        """
        datei = iom.fopen(fpath_csv, "w")   # "w" = write text

        if datei is None:
            print("CSV-Datei konnte nicht geöffnet werden.")
            return

        with datei:
            writer = csv.writer(datei)
            writer.writerow(kopfzeile)      # erste Zeile: Spaltenüberschriften
            writer.writerows(self._list)    # alle Datensätze auf einmal schreiben

        print(f"Daten exportiert nach '{fpath_csv}'.")


    # -------------------------------------------------------------------------
    # CSV-Import
    # -------------------------------------------------------------------------

    def import_csv(self, fpath: str) -> None:
        """
        Importiert Bücher aus einer CSV-Datei.

        Achtung: Der Import ersetzt die aktuelle Liste vollständig.

        Ablauf:
            1. CSV-Datei öffnen und alle Zeilen einlesen
            2. Erste Zeile = Kopfzeile (wird nicht als Datensatz übernommen)
            3. Restliche Zeilen = Datensätze (leere Zeilen und fehlerhafte Einträge werden gefiltert)

        Args:
            fpath: Pfad zur CSV-Quelldatei.
        """
        datei = iom.fopen(fpath, "rt")   # "rt" = read text

        if datei is None:
            print(f"Datei '{fpath}' konnte nicht geöffnet werden.")
            return

        with datei:
            reader = csv.reader(datei)
            alle_zeilen = list(reader)   # alle Zeilen als Liste einlesen

        if not alle_zeilen:
            print("CSV-Datei ist leer.")
            return

        kopfzeile    = alle_zeilen[0]   # erste Zeile = Kopfzeile

        # Datensätze filtern: leere Zeilen und Zeilen ohne Nummer entfernen
        datensaetze = []
        for zeile in alle_zeilen[1:]:
            # Leere Zeilen oder zu kurze Zeilen ignorieren
            if not zeile or not zeile[0]:
                continue
            # Nummer validieren (muss numerisch sein)
            try:
                int(zeile[0])
                datensaetze.append(zeile)
            except ValueError:
                print(f"[!] Ignoriere Zeile mit ungueltiger Nummer: {zeile}")
                continue

        # Aktuelle Liste durch importierte Daten ersetzen
        self._list = datensaetze

        print(f"{len(self._list)} Eintrag/Einträge importiert aus '{fpath}'.")
        print(f"Spalten: {kopfzeile}")


    # -------------------------------------------------------------------------
    # Hilfsmethoden für Suche, Löschen und Einfügen
    # -------------------------------------------------------------------------

    def check_number(self, nummer: str) -> int:
        """
        Sucht einen Datensatz anhand seiner Nummer (erstes Feld).

        enumerate() gibt gleichzeitig Index und Wert zurück:
            for i, zeile in enumerate(self._list):
                → i    = aktueller Index (0, 1, 2, …)
                → zeile = die innere Liste (Datensatz)

        Args:
            nummer: Die gesuchte Nummer als String, z. B. "003".

        Returns:
            Den Index des gefundenen Datensatzes,
            oder -1 wenn die Nummer nicht existiert.
        """
        for i, zeile in enumerate(self._list):
            if zeile[0] == nummer:
                return i   # gefunden → Index zurückgeben

        return -1   # nicht gefunden


    def delete_sublist(self, index: int) -> list:
        """
        Entfernt den Datensatz an Position "index" aus der Liste
        und gibt ihn zurück.

        list.pop(index) entfernt das Element an der angegebenen
        Position und gibt es zurück – in einem Schritt.

        Args:
            index: Position in der internen Liste (0-basiert).

        Returns:
            Der entfernte Datensatz als Liste.
        """
        return self._list.pop(index)


    def check_free_entry(self) -> int | None:
        """
        Sucht die erste Lücke in der Nummernfolge.

        Beispiel: Liste enthält 001, 002, 004, 005
            → Lücke bei Index 2 (Nummer 003 gehört zwischen Index 1 und 2)
            → gibt Listenindex 2 zurück (Einfügestelle)

        Wie es funktioniert:
            1. Prüfe, ob die erste Nummer > 1 ist → Lücke vor Index 0
            2. Vergleiche aufeinanderfolgende Nummern
            3. Wenn Nummer[i] - Nummer[i-1] > 1 → Lücke gefunden bei Index i

        Returns:
            Den Index der Einfügestelle, oder None wenn keine Lücke existiert.
        """
        if not self._list:
            return None   # Leere Liste → keine Lücke

        try:
            # Prüfe, ob die erste Nummer > 1 ist (Lücke vor dem ersten Eintrag)
            if int(self._list[0][0]) > 1:
                return 0   # Einfügen am Anfang

            # Prüfe Lücken zwischen Einträgen
            for i in range(1, len(self._list)):
                diff = int(self._list[i][0]) - int(self._list[i - 1][0])
                if diff > 1:
                    # Lücke gefunden → Einfügestelle ist Index i
                    return i
        except (ValueError, IndexError):
            # Fehlerhafte Nummern ignorieren
            pass

        return None   # keine Lücke


    def insert_sublist(self, index: int, sublist: list) -> None:
        """
        Fügt einen neuen Datensatz an der angegebenen Position ein.

        list.insert(index, element) verschiebt alle Elemente ab "index"
        um eine Position nach rechts und fügt das neue Element ein.

        Args:
            index:   Einfügeposition (0-basiert).
            sublist: Der neue Datensatz als Liste.
        """
        self._list.insert(index, sublist)
