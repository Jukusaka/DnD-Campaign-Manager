from models.item import Item
from models.spell import Spell
from models.character import Character
from save import GameDataManager
from pydantic import ValidationError


manager = GameDataManager()
party: list[Character] = []


# ─── Display Helpers ──────────────────────────────────────────────────────────

def header(title: str):
    print(f"\n{'─'*42}")
    print(f"  {title}")
    print(f"{'─'*42}")

def pause():
    input("\n  Press Enter to continue...")

def print_character_sheet(character: Character):
    header(f"{character.name}  —  Level {character.level}")
    print(f"  HP:           {character.health_points}/{character.max_health_points}")
    print(f"  Strength:     {character.strength}")
    print(f"  Intelligence: {character.intelligence}")
    print(f"  Faith:        {character.faith}")
    print(f"  Vitality:     {character.vitality}")
    print(f"  Defence:      {character.defence}")

    if character.items:
        print(f"\n  Items:")
        for i, item in enumerate(character.items, 1):
            print(f"    {i}. {item.name} [{item.rarity}] — {item.value}g / {item.weight}lb")
            print(f"       {item.description}")
    else:
        print("\n  Items: none")

    if character.spells:
        print(f"\n  Spells:")
        for i, spell in enumerate(character.spells, 1):
            dice = f" | {spell.damage_dice}" if spell.damage_dice else ""
            print(f"    {i}. {spell.name} | {spell.range} | {spell.duration}{dice}")
            print(f"       {spell.description}")
    else:
        print("\n  Spells: none")

def print_party():
    if not party:
        print("  (party is empty)")
        return
    for i, c in enumerate(party, 1):
        print(f"  {i}. {c.name}  (Level {c.level})  —  HP: {c.health_points}/{c.max_health_points}")

def pick_character(prompt="  Select character number: ") -> Character | None:
    print_party()
    if not party:
        return None
    try:
        idx = int(input(prompt)) - 1
        if 0 <= idx < len(party):
            return party[idx]
        print("  Invalid selection.")
    except ValueError:
        print("  Please enter a number.")
    return None


# ─── Input Helpers ────────────────────────────────────────────────────────────

def prompt_int(label: str, default: int = None) -> int:
    while True:
        raw = input(f"  {label}{f' [{default}]' if default is not None else ''}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a whole number.")

def prompt_str(label: str, default: str = None) -> str:
    raw = input(f"  {label}{f' [{default}]' if default is not None else ''}: ").strip()
    return raw if raw else (default or "")

def prompt_float(label: str, default: float = 0.0) -> float:
    while True:
        raw = input(f"  {label} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a number.")


# ─── Character Actions ────────────────────────────────────────────────────────

def create_character():
    header("Create New Character")
    try:
        name    = prompt_str("Name")
        level   = prompt_int("Level", 1)
        str_    = prompt_int("Strength     (1-20)", 10)
        int_    = prompt_int("Intelligence (1-20)", 10)
        faith   = prompt_int("Faith        (1-20)", 10)
        vit     = prompt_int("Vitality     (1-20)", 10)
        def_    = prompt_int("Defence      (1-20)", 10)
        max_hp  = prompt_int("Max HP", 100)

        character = Character(
            name=name, level=level,
            strength=str_, intelligence=int_, faith=faith,
            vitality=vit, defence=def_,
            health_points=max_hp, max_health_points=max_hp
        )
        party.append(character)
        print(f"\n  ✓ {character.name} added to the party!")
    except ValidationError as e:
        print("\n  ✗ Could not create character:")
        for err in e.errors():
            print(f"    - {err['loc'][0]}: {err['msg']}")

def view_characters():
    header("View Character Sheet")
    character = pick_character()
    if character:
        print_character_sheet(character)

def remove_character():
    header("Remove Character")
    print_party()
    if not party:
        return
    try:
        idx = int(input("  Select character to remove: ")) - 1
        if 0 <= idx < len(party):
            removed = party.pop(idx)
            print(f"\n  ✓ {removed.name} removed from the party.")
        else:
            print("  Invalid selection.")
    except ValueError:
        print("  Please enter a number.")


# ─── Item Actions ─────────────────────────────────────────────────────────────

def add_item():
    header("Add Item to Character")
    character = pick_character()
    if not character:
        return
    print()
    try:
        name        = prompt_str("Item name")
        description = prompt_str("Description")
        rarity      = prompt_str("Rarity (common/uncommon/rare/very rare/legendary)", "common")
        weight      = prompt_float("Weight (lb)", 0.0)
        value       = prompt_int("Value (gold)", 0)

        item = Item(name=name, description=description, rarity=rarity, weight=weight, value=value)
        updated = character.copy(update={"items": character.items + [item]})
        party[party.index(character)] = updated
        print(f"\n  ✓ '{item.name}' added to {updated.name}.")
    except ValidationError as e:
        print("\n  ✗ Could not create item:")
        for err in e.errors():
            print(f"    - {err['loc'][0]}: {err['msg']}")

def remove_item():
    header("Remove Item from Character")
    character = pick_character()
    if not character:
        return
    if not character.items:
        print("  This character has no items.")
        return

    print(f"\n  Items of {character.name}:")
    for i, item in enumerate(character.items, 1):
        print(f"    {i}. {item.name}")

    try:
        idx = int(input("  Select item to remove: ")) - 1
        if 0 <= idx < len(character.items):
            new_items = [it for j, it in enumerate(character.items) if j != idx]
            updated = character.copy(update={"items": new_items})
            party[party.index(character)] = updated
            print(f"\n  ✓ Item removed.")
        else:
            print("  Invalid selection.")
    except ValueError:
        print("  Please enter a number.")


# ─── Spell Actions ────────────────────────────────────────────────────────────

def add_spell():
    header("Add Spell to Character")
    character = pick_character()
    if not character:
        return
    print()
    try:
        name         = prompt_str("Spell name")
        description  = prompt_str("Description")
        casting_time = prompt_str("Casting time", "1")
        range_       = prompt_str("Range", "Self")
        duration     = prompt_str("Duration", "Instantaneous")
        damage_dice  = prompt_str("Damage dice (e.g. 2d6, leave blank for none)", "")
        damage_dice  = damage_dice if damage_dice else None

        spell = Spell(
            name=name, description=description,
            casting_time=casting_time, range=range_,
            duration=duration, damage_dice=damage_dice
        )
        updated = character.copy(update={"spells": character.spells + [spell]})
        party[party.index(character)] = updated
        print(f"\n  ✓ '{spell.name}' added to {updated.name}.")
    except ValidationError as e:
        print("\n  ✗ Could not create spell:")
        for err in e.errors():
            print(f"    - {err['loc'][0]}: {err['msg']}")

def remove_spell():
    header("Remove Spell from Character")
    character = pick_character()
    if not character:
        return
    if not character.spells:
        print("  This character has no spells.")
        return

    print(f"\n  Spells of {character.name}:")
    for i, spell in enumerate(character.spells, 1):
        print(f"    {i}. {spell.name}")

    try:
        idx = int(input("  Select spell to remove: ")) - 1
        if 0 <= idx < len(character.spells):
            new_spells = [sp for j, sp in enumerate(character.spells) if j != idx]
            updated = character.copy(update={"spells": new_spells})
            party[party.index(character)] = updated
            print(f"\n  ✓ Spell removed.")
        else:
            print("  Invalid selection.")
    except ValueError:
        print("  Please enter a number.")
