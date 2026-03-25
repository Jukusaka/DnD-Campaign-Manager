# D&D Campaign Manager

## Kamil Rochala | Igor Mankiewicz

## DnD Campaign Manager

This project is a **Pydantic-powered DnD Campaign Manager**. It provides a robust backend framework for creating, validating, and persisting tabletop-style characters, items, and spells.

## About the Project

The system acts as a "source of truth" for game data, ensuring that every character created follows strict DnD rules through automated validation.

- **Character Creation:** Define heroes with stats (Strength, Intelligence, etc.) capped between 1 and 20.
    
- **Inventory & Magic:** Equip characters with items (with weight and rarity) and spells (validated against standard dice notation like `2d6` or `1d10`).
    
- **Data Persistence:** A `GameDataManager` handles saving and loading your party to/from JSON files, allowing you to resume your adventure later.
    
- **Reliability:** Includes a comprehensive suite of unit tests to ensure no "illegal" characters (like a Level 99 warrior or a negative-weight sword) can enter your game world.
    

---

## Getting Started

#### Prerequisites

- **Python 3.8+**
    
- **pip** (Python package installer)
    

#### 1. Set up a Virtual Environment (venv)

It is highly recommended to use a virtual environment to keep your global Python installation clean.

**On Windows:**

Bash

```
python -m venv venv
.\venv\Scripts\activate
```

**On macOS/Linux:**

Bash

```
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install Dependencies

Once your virtual environment is active, install the required Pydantic library:

Bash

```
pip install -r requirements.txt
```

---

## How to Run

#### Run the Main Demo

The `main.py` script demonstrates creating a party (Thorin the Warrior, Elara the Wizard, and Brother Aldric), saving them to the disk, and reloading them.

Bash

```
python main.py
```

#### Run the Test Suite

To verify that the validation logic is working correctly and see how the system handles invalid data:

Bash

```
python tests.py
```

---

## Project Structure

- `models/`: Contains the Pydantic schemas for `Character`, `Item`, and `Spell`.
    
- `save.py`: Logic for JSON serialization and file management.
    
- `main.py`: The entry point and demonstration script.
    
- `tests.py`: Unit tests for model validation.
    
