![TitanWar Combo Helper](https://github.com/user-attachments/assets/fff5dfaf-9cc6-4c57-8b06-8be7a5decac7)
# TitanWar Combo Helper

A helpful tool to optimize team combinations and buff strategies in the game **TitanWar**. With this app, you can calculate the best character combinations for your teams and activate card buffs based on your preferences.

---

## Features

### 1. **Character Management**
- **Character Images:** Clear display of all characters with images.
- **Character Selection:** Select up to 6 characters simultaneously.
- **Exclusion:** Characters can be excluded or re-included. (with mouse right click)

### 2. **Buff Optimization**
- **Autofill:** Automatically calculates the best combinations based on:
  - Attack
  - Defense
  - Random Buffs
- **Buff Display:** Shows activated buffs and associated characters.

### 3. **Multilingual Support**
- Available in **German (DE)** and **English (EN)**.
- Dynamic language switching in the interface.

### 4. **Team Management**
- Save and load teams directly from the GUI.
- Manage up to 6 teams simultaneously.
- Full Reset of all set Teams.

---

## Installation

### Prerequisites
- **Python 3.11** or higher
- Libraries:
  - `Pillow`
  - `tkinter`

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/blobb999/TitanWar-Combo-Helper.git
   cd TitanWar-Combo-Helper
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   python TitanWar_Combo_Helper.py
   ```

### Build Binary
1. **compile:**
   ```bash
   pyinstaller --noconsole --onefile --add-data "data.json;." "TitanWar_Combo_Helper.py"
   ```
---

## Usage

1. **Character Selection:**
   - Select or deselect characters via left-click.
   - Right-click to exclude characters from calculations.

2. **Autofill Function:**
   - Choose a buff type (Attack, Defense, or Random).
   - Click **Autofill** to calculate the best combinations.

3. **Save/Load Teams:**
   - Select a team and save it.
   - Load saved teams using the buttons at the bottom.

4. **Change Language:**
   - Switch between German and English using the interface at the bottom right.

---

## Project Structure

```
TitanWar-Combo-Helper/
├── img/                # Directory for character and buff images
├── data.json           # Buff data structure
├── config.cfg          # User configuration
├── TitanWar_Combo_Helper.py  # Main program
├── utils.py            # Utility functions
├── character_utils.py  # Logic for combinations and buffs
├── gui_layout.py       # GUI layout
├── calc_feedback.py    # Infobox while Calculating
├── requirements.txt    # Dependencies
└── readme.md           # Project description
```

---

## Contributing

We welcome contributions! Here's how you can get involved:

1. **Fork:**
   Fork this repository.
2. **Make Changes:**
   Work on your feature or bug fix.
3. **Pull Request:**
   Submit a pull request with a description of your changes.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Contact

- **Author:** blobb999
- **GitHub:** [TitanWar-Combo-Helper](https://github.com/blobb999/TitanWar-Combo-Helper)

---

Enjoy using the TitanWar Combo Helper!