from models.item import Item
from models.spell import Spell
from models.character import Character
from save import GameDataManager


def print_character(character: Character):
    print(f"\n{'='*40}")
    print(f"  {character.name}  (Level {character.level})")
    print(f"{'='*40}")
    print(f"  HP:           {character.health_points}/{character.max_health_points}")
    print(f"  Strength:     {character.strength}")
    print(f"  Intelligence: {character.intelligence}")
    print(f"  Faith:        {character.faith}")
    print(f"  Vitality:     {character.vitality}")
    print(f"  Defence:      {character.defence}")

    if character.items:
        print(f"\n  Items ({len(character.items)}):")
        for item in character.items:
            print(f"    - {item.name} [{item.rarity}] | {item.value}g | {item.weight}lb")
            print(f"      {item.description}")

    if character.spells:
        print(f"\n  Spells ({len(character.spells)}):")
        for spell in character.spells:
            dice_info = f" | Damage: {spell.damage_dice}" if spell.damage_dice else ""
            print(f"    - {spell.name} | Range: {spell.range} | Duration: {spell.duration}{dice_info}")
            print(f"      {spell.description}")

    print(f"{'='*40}\n")


def main():
    manager = GameDataManager()

    # --- Create some items ---
    print("Creating items...")
    sword = Item(
        name="Iron Sword",
        description="A reliable iron sword, worn but sturdy.",
        rarity="common",
        weight=4.5,
        value=15
    )
    staff = Item(
        name="Arcane Staff",
        description="A gnarled staff crackling with magical energy.",
        rarity="rare",
        weight=3.0,
        value=250
    )
    holy_symbol = Item(
        name="Golden Holy Symbol",
        description="A golden symbol radiating divine warmth.",
        rarity="uncommon",
        weight=0.5,
        value=80
    )

    # --- Create some spells ---
    print("Creating spells...")
    fireball = Spell(
        name="Fireball",
        description="Hurls a blazing ball of fire at the target.",
        casting_time="1",
        range="120ft",
        duration="Instantaneous",
        damage_dice="3d6"
    )
    heal = Spell(
        name="Cure Wounds",
        description="Channels divine energy to restore the target's health.",
        casting_time="1",
        range="Touch",
        duration="Instantaneous",
        damage_dice=None
    )
    magic_missile = Spell(
        name="Magic Missile",
        description="Fires three darts of magical force, each dealing damage.",
        casting_time="1",
        range="120ft",
        duration="Instantaneous",
        damage_dice="1d4"
    )

    # --- Create characters ---
    print("Creating characters...")
    warrior = Character(
        name="Thorin",
        level=5,
        strength=18,
        intelligence=8,
        faith=10,
        vitality=15,
        defence=16,
        health_points=180,
        max_health_points=180,
        items=[sword],
        spells=[]
    )

    wizard = Character(
        name="Elara",
        level=7,
        strength=6,
        intelligence=20,
        faith=10,
        vitality=8,
        defence=8,
        health_points=90,
        max_health_points=90,
        items=[staff],
        spells=[fireball, magic_missile]
    )

    cleric = Character(
        name="Brother Aldric",
        level=4,
        strength=12,
        intelligence=12,
        faith=18,
        vitality=14,
        defence=14,
        health_points=130,
        max_health_points=130,
        items=[holy_symbol],
        spells=[heal]
    )

    # --- Print all characters ---
    print_character(warrior)
    print_character(wizard)
    print_character(cleric)

    # --- Save individual character ---
    print("Saving Thorin individually...")
    manager.save_character(warrior, filename="thorin_save")

    # --- Save all characters together ---
    print("Saving all characters...")
    all_save_path = manager.save_all_data([warrior, wizard, cleric], filename="party_save")

    # --- Load individual character ---
    print("\nLoading Thorin from file...")
    loaded_warrior = manager.load_character("saves/thorin_save.json")
    print(f"Loaded character: {loaded_warrior.name}, Level {loaded_warrior.level}")

    # --- Load all characters ---
    print("\nLoading entire party from file...")
    party = manager.load_all_data(all_save_path)
    print(f"Party members: {', '.join(c.name for c in party)}")


if __name__ == "__main__":
    main()