import json
from pathlib import Path
from typing import List
from datetime import datetime
from models.item import *
from models.spell import *
from models.character import *


class GameDataManager:
    """Manages saving and loading game data to/from JSON files"""
    
    def __init__(self, save_directory: str = "./saves"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
    
    def save_character(self, character: Character, filename: str = None) -> str:
        """
        Save a single character to JSON
        
        Args:
            character: Character object to save
            filename: Optional custom filename (without .json)
        
        Returns:
            Path to the saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{character.name}_{timestamp}"
        
        filepath = self.save_directory / f"{filename}.json"
        
        character_data = character.dict()
        
        with open(filepath, 'w') as f:
            json.dump(character_data, f, indent=2, default=str)
        
        print(f"✓ Character saved to: {filepath}")
        return str(filepath)
    
    def save_all_data(self, characters: List[Character], filename: str = "game_data") -> str:
        """
        Save all characters and their data to a single JSON file
        
        Args:
            characters: List of Character objects to save
            filename: Custom filename (without .json)
        
        Returns:
            Path to the saved file
        """
        filepath = self.save_directory / f"{filename}.json"
        
        # Convert all characters to dictionaries
        game_data = {
            "save_date": datetime.now().isoformat(),
            "characters": [char.dict() for char in characters],
            "total_characters": len(characters)
        }
        
        with open(filepath, 'w') as f:
            json.dump(game_data, f, indent=2, default=str)
        
        print(f"✓ All game data saved to: {filepath}")
        return str(filepath)
    
    def load_character(self, filepath: str) -> Character:
        """
        Load a character from JSON file
        
        Args:
            filepath: Path to the JSON file
        
        Returns:
            Character object
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        character = Character(**data)
        print(f"✓ Character loaded from: {filepath}")
        return character
    
    def load_all_data(self, filepath: str) -> List[Character]:
        """
        Load all characters from JSON file
        
        Args:
            filepath: Path to the JSON file
        
        Returns:
            List of Character objects
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        characters = [Character(**char_data) for char_data in data.get("characters", [])]
        print(f"✓ Loaded {len(characters)} characters from: {filepath}")
        return characters
