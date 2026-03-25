import unittest
from pydantic import ValidationError
from models.item import Item
from models.spell import Spell
from models.character import Character


class TestItemModel(unittest.TestCase):

    def test_valid_item_creation(self):
        item = Item(
            name="Iron Sword",
            description="A sturdy iron sword",
            rarity="common",
            weight=5.0,
            value=10
        )
        self.assertEqual(item.name, "Iron Sword")
        self.assertEqual(item.rarity, "common")

    def test_item_invalid_rarity(self):
        with self.assertRaises(ValidationError):
            Item(
                name="Magic Staff",
                description="A glowing staff",
                rarity="mythic"  # Not a valid rarity
            )

    def test_item_negative_weight(self):
        with self.assertRaises(ValidationError):
            Item(
                name="Feather",
                description="A light feather",
                weight=-1.0  # Cannot be negative
            )

    def test_item_negative_value(self):
        with self.assertRaises(ValidationError):
            Item(
                name="Broken Shield",
                description="A cracked shield",
                value=-5  # Cannot be negative
            )

    def test_item_name_too_long(self):
        with self.assertRaises(ValidationError):
            Item(
                name="A" * 101,  # Exceeds max_length of 100
                description="Some item"
            )


class TestSpellModel(unittest.TestCase):

    def test_valid_spell_creation(self):
        spell = Spell(
            name="Fireball",
            description="Hurls a ball of fire at the target",
            damage_dice="2d6"
        )
        self.assertEqual(spell.name, "Fireball")
        self.assertEqual(spell.damage_dice, "2d6")

    def test_spell_invalid_damage_dice_format(self):
        with self.assertRaises(ValidationError):
            Spell(
                name="Lightning Bolt",
                description="Strikes with lightning",
                damage_dice="roll5"  # Invalid format
            )

    def test_spell_invalid_dice_size(self):
        with self.assertRaises(ValidationError):
            Spell(
                name="Odd Strike",
                description="A strange attack",
                damage_dice="2d7"  # d7 is not a standard die
            )

    def test_spell_invalid_name_characters(self):
        with self.assertRaises(ValidationError):
            Spell(
                name="Fire@Ball!",  # Special characters not allowed
                description="Burns everything"
            )

    def test_spell_empty_description(self):
        with self.assertRaises(ValidationError):
            Spell(
                name="Void",
                description="   "  # Blank description
            )


class TestCharacterModel(unittest.TestCase):

    def test_valid_character_creation(self):
        character = Character(
            name="Aragorn",
            level=5,
            strength=15,
            intelligence=10,
            faith=8,
            vitality=12,
            defence=14,
            health_points=120,
            max_health_points=120
        )
        self.assertEqual(character.name, "Aragorn")
        self.assertEqual(character.level, 5)

    def test_character_invalid_name_characters(self):
        with self.assertRaises(ValidationError):
            Character(name="Aragon@#!")  # Special characters not allowed

    def test_character_level_too_high(self):
        with self.assertRaises(ValidationError):
            Character(name="Gandalf", level=21)  # Max level is 20

    def test_character_level_too_low(self):
        with self.assertRaises(ValidationError):
            Character(name="Gandalf", level=0)  # Min level is 1

    def test_character_stat_out_of_range(self):
        with self.assertRaises(ValidationError):
            Character(name="Legolas", strength=25)  # Max stat is 20

    def test_character_negative_health(self):
        with self.assertRaises(ValidationError):
            Character(name="Boromir", health_points=-10)  # Cannot be negative

    def test_character_max_health_exceeded(self):
        with self.assertRaises(ValidationError):
            Character(name="Sauron", max_health_points=10000)  # Max is 9999

    def test_character_with_items_and_spells(self):
        item = Item(name="Shield", description="A wooden shield")
        spell = Spell(name="Heal", description="Restores health")
        character = Character(
            name="Cleric",
            items=[item],
            spells=[spell]
        )
        self.assertEqual(len(character.items), 1)
        self.assertEqual(len(character.spells), 1)


if __name__ == '__main__':
    unittest.main()