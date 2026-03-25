from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional
import re

class Spell(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Spell name")
    casting_time: str = Field(default="1", description="Time to cast")
    range: str = Field(default="Self", description="Spell range")
    duration: str = Field(default="Instantaneous", description="Spell duration")
    description: str = Field(..., description="Spell description")
    damage_dice: Optional[str] = Field(None, description="Damage dice if applicable (e.g., '2d6')")

    @validator("name", "description")
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError("Spell fields cannot be empty")
        return v.strip()

    @validator("name")
    def validate_name_format(cls, v):
        """Ensure name contains only letters, numbers, spaces, and hyphens"""
        if not re.match(r"^[a-zA-Z0-9\s\-']+$", v):
            raise ValueError("Spell name can only contain letters, numbers, spaces, hyphens, and apostrophes")
        return v

    @validator("damage_dice")
    def validate_damage_dice(cls, v):
        """Validate damage dice format (e.g., '2d6', '3d8+2', '1d4')"""
        if v is None:
            return v
        
        # Pattern: XdY or XdY+Z (e.g., 2d6, 3d8+5, 1d4+2)
        if not re.match(r"^\d+d\d+(\+\d+)?$", v.lower()):
            raise ValueError(
                "Damage dice must be in format like '2d6', '3d8+2', or '1d4'"
            )
        
        # Validate reasonable dice values
        match = re.match(r"^(\d+)d(\d+)(\+\d+)?$", v.lower())
        if match:
            num_dice, dice_size = int(match.group(1)), int(match.group(2))
            
            if num_dice < 1 or num_dice > 100:
                raise ValueError("Number of dice must be between 1 and 100")
            
            if dice_size not in [1, 2, 3, 4, 6, 8, 10, 12, 20, 100]:
                raise ValueError("Dice size must be a standard die type (d4, d6, d8, d10, d12, d20, etc.)")
        
        return v.lower()