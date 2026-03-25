from pydantic import BaseModel, Field, validator, root_validator

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str = Field(..., description="Item description")
    rarity: str = Field(default="common", description="Item rarity (common, uncommon, rare, legendary)")
    weight: float = Field(default=0.0, description="Item weight in pounds")
    value: int = Field(default=0, description="Item value in gold")

    @validator("rarity")
    def validate_rarity(cls, v):
        """Ensure rarity is one of the valid types"""
        valid_rarities = ["common", "uncommon", "rare", "very rare", "legendary"]
        if v.lower() not in valid_rarities:
            raise ValueError(f"Rarity must be one of: {', '.join(valid_rarities)}")
        return v.lower()

    @validator("weight")
    def validate_weight(cls, v):
        """Ensure weight is non-negative"""
        if v < 0:
            raise ValueError("Item weight cannot be negative")
        return v

    @validator("value")
    def validate_value(cls, v):
        """Ensure value is non-negative"""
        if v < 0:
            raise ValueError("Item value cannot be negative")
        return v