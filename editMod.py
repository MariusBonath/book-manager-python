# =============================================================================
# editMod.py – Eingabe, Validierung und Bearbeitung
# =============================================================================
#
# Dieses Modul kümmert sich um:
#   - Prüfen, ob eine Nutzereingabe dem erwarteten Format entspricht
#   - Solange nachfragen, bis die Eingabe gültig ist
#   - Einen Datensatz löschen (mit Bestätigung)
#   - Einen neuen Datensatz an einer freien Stelle einfügen
#
# Konzepte in dieser Datei:
#   - Funktionen (def)
#   - Parameter und Rückgabewerte (return)
#   - try/except (Fehlerbehandlung)
#   - for-Schleifen und while-Schleifen
#   - if/elif/else
#   - Typ-Annotationen (str, list, bool, None)
#   - String-Methoden (.isdigit(), .isalpha(), .isalnum(), .upper(), .strip())
# =============================================================================


# =============================================================================
# Private Hilfsfunktion: Dezimalzahl prüfen
# =============================================================================

def _ist_dezimalzahl(wert: str) -> bool:
    """
    Prüft, ob ein String in eine Dezimalzahl (float) umgewandelt werden kann.

    Beispiele:
        "12.99"  → True   (gültige Dezimalzahl)
        "100"    → True   (Ganzzahl ist auch float-kompatibel)
        "abc"    → False  (kein gültiger Zahlenwert)
        "12,99"  → False  (Komma statt Punkt → ungültig)

    Der führende Unterstrich (_) zeigt: Diese Funktion ist
    nur für dieses Modul gedacht (modul-privat).

    Args:
        wert: Der zu prüfende String.

    Returns:
        True wenn der String eine gültige Dezimalzahl ist, sonst False.
    """
    try:
        float(wert)   # Konvertierungsversuch
        return True
    except ValueError:
        # ValueError wird ausgelöst, wenn float() den String nicht umwandeln kann
        return False


# =============================================================================
# Funktion: check_item – Eingabe gegen eine Regel prüfen
# =============================================================================

def check_item(eingabe: str, format_spec: list) -> bool:
    """
    Prüft, ob eine Eingabe der angegebenen Validierungsregel entspricht.

    Aufbau von format_spec:
        Das erste Element ist das Schlüsselwort (die Regel).
        Alle weiteren Elemente sind zusätzlich erlaubte Zeichen.

    Beispiele für format_spec:
        ["DIGIT"]              → nur Ziffern erlaubt
        ["ALPHA", " ", "-"]   → Buchstaben + Leerzeichen + Bindestrich erlaubt
        ["FLOAT"]             → muss eine Dezimalzahl sein
        ["ALL"]               → alles erlaubt

    Schlüsselwörter:
        "ALL"   → beliebige Eingabe (keine Prüfung)
        "DIGIT" → nur Ziffern (0–9)
        "ALPHA" → nur Buchstaben (a–z, A–Z) + Sonderzeichen aus der Liste
        "ALNUM" → Buchstaben und Ziffern + Sonderzeichen aus der Liste
        "FLOAT" → muss als Dezimalzahl lesbar sein (z. B. "12.99")

    Args:
        eingabe:     Der eingegebene String.
        format_spec: Validierungsregel als Liste.

    Returns:
        True wenn die Eingabe gültig ist, False wenn nicht.
    """

    # Leere Eingabe ist immer ungültig
    if not eingabe:
        return False

    regel   = format_spec[0]          # erstes Element = Schlüsselwort
    extras  = format_spec[1:]         # alle weiteren = zusätzlich erlaubte Zeichen

    # -------------------------------------------------------------------------
    # FLOAT-Prüfung: funktioniert auf dem ganzen String, nicht zeichenweise
    # -------------------------------------------------------------------------
    # "12.99" enthält einen Punkt – der ist bei DIGIT-Prüfung ungültig.
    # Deshalb behandeln wir FLOAT als Sonderfall.
    if regel == "FLOAT":
        return _ist_dezimalzahl(eingabe)

    # -------------------------------------------------------------------------
    # Zeichenweise Prüfung für alle anderen Regeln
    # -------------------------------------------------------------------------
    # Wir gehen jedes Zeichen der Eingabe durch.
    # Sobald ein Zeichen die Regel verletzt → return False
    for zeichen in eingabe:
        if regel == "ALL":
            # Alle Zeichen erlaubt → weiter zum nächsten Zeichen
            continue

        elif regel == "DIGIT" and zeichen.isascii() and zeichen.isdigit():
            # isascii() → prüft, ob Zeichen ASCII ist (verhindert Hochziffern wie ²)
            # isdigit() → True für "0" bis "9"
            continue

        elif regel == "ALPHA" and (zeichen.isalpha() or zeichen in extras):
            # isalpha() → True für Buchstaben (einschließlich Umlaute)
            # zeichen in extras → True für zusätzlich erlaubte Zeichen
            continue

        elif regel == "ALNUM" and (zeichen.isascii() and zeichen.isalnum() or zeichen in extras):
            # isascii() → prüft, ob Zeichen ASCII ist
            # isalnum() → True für Buchstaben und Ziffern
            # extras können auch Nicht-ASCII-Zeichen sein (z. B. Umlaute)
            continue

        elif zeichen in extras:
            # Sonderzeichen, das explizit erlaubt ist
            continue

        else:
            # Zeichen ist ungültig → Eingabe insgesamt ungültig
            return False

    # Alle Zeichen haben die Prüfung bestanden
    return True


# =============================================================================
# Funktion: edit_item – Eingabe einlesen und validieren
# =============================================================================

def edit_item(prompt: str, format_spec: list) -> str:
    """
    Fordert den Nutzer zur Eingabe auf und wiederholt die Abfrage,
    bis die Eingabe der Validierungsregel entspricht.

    Sonderfall: Gibt der Nutzer "quit()" ein, wird die Eingabe
    sofort zurückgegeben – ohne Validierung. Das erlaubt dem
    aufrufenden Code, die Eingabe abzubrechen.

    Beispiel:
        titel = edit_item("Bitte Titel eingeben: ", ["ALL"])
        → gibt den eingegebenen Titel zurück

    Args:
        prompt:      Anzeige-Text (Eingabeaufforderung).
        format_spec: Validierungsregel (siehe check_item).

    Returns:
        Die validierte Eingabe als String, oder "quit()" bei Abbruch.
    """
    while True:
        # .strip() entfernt führende und nachfolgende Leerzeichen
        eingabe = input(prompt).strip()

        if eingabe == "quit()":
            # Abbruch-Signal → sofort zurückgeben, ohne zu prüfen
            return eingabe

        if check_item(eingabe, format_spec):
            # Eingabe ist gültig → zurückgeben
            return eingabe

        # Eingabe ist ungültig → Hinweis ausgeben und nochmal fragen
        print(f"  Ungültige Eingabe. Erlaubtes Format: {format_spec}")


# =============================================================================
# Funktion: delete_sublist – Datensatz löschen
# =============================================================================

def delete_sublist(lco) -> None:
    """
    Fragt den Nutzer nach einer Datensatz-Nummer und löscht diesen
    nach einer Bestätigungsabfrage.

    Ablauf:
        1. Nummer eingeben
        2. Prüfen, ob Nummer existiert
        3. Bestätigung abfragen (J/N)
        4. Bei "J" löschen und Bestätigung ausgeben

    Args:
        lco: Ein Listclass-Objekt (enthält die Bücherliste).

    Returns:
        None (kein Rückgabewert – die Änderung erfolgt direkt im Objekt)
    """
    # Nummer vom Nutzer einlesen
    del_nummer = input("Bitte Nummer des zu löschenden Eintrags eingeben: ").strip()

    # In der Liste nach der Nummer suchen
    # check_number() gibt den Index zurück, oder -1 wenn nicht gefunden
    del_index = lco.check_number(del_nummer)

    if del_index != -1:
        # Nummer wurde gefunden → Bestätigung abfragen
        bestaetigung = input(f"Eintrag {del_nummer} wirklich löschen? (J/N): ")

        # .upper() wandelt "j" → "J", damit Groß- und Kleinschreibung egal ist
        if bestaetigung.upper() == "J":
            geloescht = lco.delete_sublist(del_index)
            # geloescht[0] = Nummer, geloescht[1] = Titel
            print(f"Gelöscht: {geloescht[0]} – {geloescht[1]}")
        else:
            print("Löschen abgebrochen.")
    else:
        print(f"Nummer '{del_nummer}' nicht gefunden.")


# =============================================================================
# Funktion: insert_sublist – Datensatz an freier Stelle einfügen
# =============================================================================

def insert_sublist(lco, prompts: list, format_specs: list) -> None:
    """
    Fügt einen neuen Datensatz an der ersten freien Lücke in der
    Nummernfolge ein.

    Beispiel: Wenn die Liste 001, 002, 004, 005 enthält,
    ist Nummer 003 frei → neuer Eintrag wird dort eingefügt.
    Die Nummer wird automatisch vergeben.

    Gibt es keine Lücke, wird eine Fehlermeldung ausgegeben.
    In diesem Fall kann der Nutzer über "e" (edit_list) anhängen.

    Args:
        lco:          Listclass-Objekt (enthält die Bücherliste).
        prompts:      Eingabeaufforderungen für jedes Feld.
        format_specs: Validierungsregeln für jedes Feld.

    Returns:
        None
    """
    # check_free_entry() sucht nach der ersten Lücke in der Nummernfolge
    # und gibt den Listenindex zurück
    freier_index = lco.check_free_entry()

    if freier_index is None:
        # Keine Lücke vorhanden
        print("Keine freie Stelle gefunden. Nutze 'e', um einen neuen Eintrag anzuhängen.")
        return

    # Nummer für diese Einfügestelle berechnen
    try:
        if freier_index < len(lco._list):
            # Lücke zwischen Einträgen: nächste Nummer = vorhergehende + 1
            naechste_nr = f"{int(lco._list[freier_index - 1][0]) + 1:03}" if freier_index > 0 else "001"
        else:
            # Lücke am Ende: nächste Nummer = letzter Eintrag + 1
            naechste_nr = f"{int(lco._list[-1][0]) + 1:03}"
    except (ValueError, IndexError):
        # Fehler bei Nummernberechnung → Fallback
        naechste_nr = "001"

    print(f"Einfügen an Nummer: {naechste_nr}")

    # Datensatz Feld für Feld einlesen (aber nicht das erste Feld = Nummer)
    sublist = [naechste_nr]  # erste Spalte = automatisch vergebene Nummer

    for i in range(1, len(prompts)):  # ab Index 1 (Nummer überspringen)
        eingabe = edit_item(prompts[i], format_specs[i])

        if eingabe == "quit()":
            # Nutzer hat abgebrochen → nichts einfügen
            print("Einfügen abgebrochen.")
            return

        sublist.append(eingabe)

    # Fertigen Datensatz in die Liste einfügen
    lco.insert_sublist(freier_index, sublist)
    print("Eintrag erfolgreich eingefügt.")
