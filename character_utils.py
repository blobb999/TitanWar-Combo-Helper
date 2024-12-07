#character_utils.py:

from itertools import combinations

def calculate_best_combination(data, available_characters, preselected, language, valid_cards=None, max_slots=6):
    """
    Berechnet die beste Kombination von Charakteren, um die maximale Anzahl an Karten zu aktivieren.

    Args:
        data (dict): Die Datenstruktur, die Karten und benötigte Charaktere beschreibt.
        available_characters (set): Alle verfügbaren Charaktere basierend auf der aktuellen Sprache.
        preselected (set): Bereits vorausgewählte Charaktere.
        language (str): Die aktuelle Sprache ('DE' oder 'EN').
        valid_cards (dict): Gefilterte Buffs, die berücksichtigt werden sollen (optional).
        max_slots (int): Maximale Anzahl an wählbaren Charakteren.

    Returns:
        list: Die beste Kombination von Charakteren.
    """
    # Wenn valid_cards angegeben ist, berücksichtigen Sie nur diese Buffs
    if valid_cards is not None:
        relevant_cards = valid_cards
    else:
        relevant_cards = data

    # Sammeln aller Charaktere, die in den relevanten Buffs vorkommen
    relevant_characters = {
        char[language]
        for card_info in relevant_cards.values()
        for char in card_info["characters"]
    } & available_characters  # Nur Charaktere, die auch verfügbar sind

    max_cards = 0
    best_combination = []

    for combo in combinations(relevant_characters - preselected, max_slots - len(preselected)):
        combined_set = preselected.union(combo)
        activated_cards = {
            card_name for card_name, card_info in relevant_cards.items()
            if set(char[language] for char in card_info["characters"]).issubset(combined_set)
        }
        if len(activated_cards) > max_cards:
            max_cards = len(activated_cards)
            best_combination = list(combo)

    return best_combination

def activate_cards(data, selected_characters, language):
    """
    Aktiviert Karten basierend auf den ausgewählten Charakteren.

    Args:
        data (dict): Die Datenstruktur, die Karten und benötigte Charaktere beschreibt.
        selected_characters (list): Die aktuell ausgewählten Charaktere.
        language (str): Die aktuelle Sprache ("DE" oder "EN").

    Returns:
        list: Aktivierte Karten mit Zusatzinformationen.
    """
    activated_cards = []
    for card_name, card_info in data.items():
        # Extrahiere die Liste der Charaktere für die aktuelle Sprache
        required_characters = {char[language] for char in card_info["characters"]}
        
        # Prüfe, ob alle erforderlichen Charaktere in den ausgewählten vorhanden sind
        if required_characters.issubset(selected_characters):
            activated_cards.append({
                "name": card_info["name"],  # Vollständiges Name-Wörterbuch
                "type": card_info["type"]   # Vollständiges Typ-Wörterbuch
            })
    return activated_cards


