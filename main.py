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
