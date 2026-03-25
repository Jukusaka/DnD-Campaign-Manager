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
    pass


class TestCharacterModel(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()