from pydantic import BaseModel, Field, validator, root_validator
import re
from item import *
from spell import *
from typing import List


class Character(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Character name")
    level: int = Field(default=1, description="Character level")

    strength: int = Field(default=10, description="Strength stat (1-20)")
    intelligence: int = Field(default=10, description="Intelligence stat (1-20)")
    faith: int = Field(default=10, description="Faith stat (1-20)")
    vitality: int = Field(default=10, description="Vitality stat (1-20)")
    defence: int = Field(default=10, description="Defence stat (1-20)")
    
    health_points: int = Field(default=100, description="Current health points")
    max_health_points: int = Field(default=100, description="Maximum health points")

    items: List['Item'] = Field(default=[], description="All the item that the player posseses")
    spells : List['Spell'] = Field(default=[], description="All the spells that the player poses")

    @validator("name")
    def validate_name_format(cls, v):
        """Ensure name contains only letters, numbers, spaces, hyphens, and apostrophes"""
        if not re.match(r"^[a-zA-Z0-9\s\-']+$", v):
            raise ValueError("Character name can only contain letters, numbers, spaces, hyphens, and apostrophes")
        return v.strip()

    @validator("strength", "intelligence", "faith", "vitality", "defence", pre=True)
    def validate_stats_in_range(cls, v):
        """Ensure all stats are between 1 and 20"""
        try:
            stat_value = int(v)
        except (ValueError, TypeError):
            raise ValueError("Stat must be an integer")
        
        if stat_value < 1 or stat_value > 20:
            raise ValueError("All stats (Strength, Intelligence, Faith, Vitality, Defence) must be between 1 and 20")
        return stat_value

    @validator("level")
    def validate_level_range(cls, v):
        """Ensure level is between 1 and 20"""
        if v < 1 or v > 20:
            raise ValueError("Character level must be between 1 and 20")
        return v

    @validator("health_points")
    def validate_health_points(cls, v):
        """Ensure health points are positive"""
        if v < 0:
            raise ValueError("Health points cannot be negative")
        return v

    @validator("max_health_points")
    def validate_max_health_points(cls, v):
        """Ensure max health points are positive and reasonable"""
        if v <= 0:
            raise ValueError("Max health points must be greater than 0")
        if v > 9999:
            raise ValueError("Max health points cannot exceed 9999")
        return v