#gui_layout.py:

from tkinter import Frame, Canvas, Scrollbar, Label, Button, StringVar, OptionMenu, Radiobutton

def setup_gui_layout(app):
    """
    Baut das Hauptlayout der GUI auf.
    """
    # Setze die Standardgröße des Fensters
    app.root.geometry("1200x900")

    # Oberer Bereich: Charaktere
    app.top_frame = Frame(app.root)
    app.top_frame.pack(side="top", fill="both", expand=True)

    app.character_canvas = Canvas(app.top_frame)
    app.character_canvas.pack(side="left", fill="both", expand=True)

    app.scrollbar = Scrollbar(app.top_frame, command=app.character_canvas.yview)
    app.scrollbar.pack(side="right", fill="y")
    app.character_canvas.configure(yscrollcommand=app.scrollbar.set)

    app.inner_frame = Frame(app.character_canvas)
    app.character_canvas.create_window((0, 0), window=app.inner_frame, anchor="nw")
    app.inner_frame.bind(
        "<Configure>", lambda e: app.character_canvas.configure(scrollregion=app.character_canvas.bbox("all"))
    )

    # Unterer Bereich: Ausgewählte Charaktere und aktivierte Karten
    app.bottom_frame = Frame(app.root)
    app.bottom_frame.pack(side="bottom", fill="x")

    app.selected_label = Label(app.bottom_frame, text="Ausgewählte Charaktere:")
    app.selected_label.pack()
    app.selected_characters_frame = Frame(app.bottom_frame)
    app.selected_characters_frame.pack()

    app.cards_label = Label(app.bottom_frame, text="Aktivierte Karten:")
    app.cards_label.pack()
    app.activated_cards_frame = Frame(app.bottom_frame)
    app.activated_cards_frame.pack()

    # Steuerungs-Buttons
    controls_frame = Frame(app.bottom_frame)
    controls_frame.pack(pady=10)

    # Pulldown-Menü-Optionen basierend auf Sprache
    app.filter_var = StringVar(value="Zufällig")
    app.filter_options = {"DE": ["Zufällig", "Verteidigung", "Angriff"], "EN": ["Random", "Defense", "Attack"]}
    app.filter_menu = OptionMenu(controls_frame, app.filter_var, *app.filter_options[app.language])
    app.filter_menu.pack(side="left", padx=5)

    # Autofill-Button
    app.autofill_button = Button(controls_frame, text="Autofill", command=app.autofill_characters)
    app.autofill_button.pack(side="left", padx=5)

    # Team-Buttons
    app.team_var = StringVar(value="Team 1")
    app.team_buttons = {}
    for team_name in ["Team 1", "Team 2", "Team 3"]:
        btn = Button(
            controls_frame,
            text=team_name,
            command=lambda t=team_name: app.select_team(t)
        )
        btn.pack(side="left", padx=5)
        app.team_buttons[team_name] = btn

    # Set-Button
    Button(controls_frame, text="Set", command=app.save_team).pack(side="left", padx=5)

    # Info-Text für aktuelles Team
    app.info_label = Label(app.bottom_frame, text="Aktuelles Team: Team 1", font=("Arial", 10, "italic"))
    app.info_label.pack(pady=5)

    # Spracheinstellungen unten rechts
    app.language_var = StringVar(value=app.language)
    Radiobutton(
        app.bottom_frame, text="EN", variable=app.language_var, value="EN",
        command=app.change_language
    ).pack(side="right", padx=5, pady=5)
    Radiobutton(
        app.bottom_frame, text="DE", variable=app.language_var, value="DE",
        command=app.change_language
    ).pack(side="right", padx=5, pady=5)

