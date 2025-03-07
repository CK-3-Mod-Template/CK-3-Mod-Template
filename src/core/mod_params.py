import os
import json
import re
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class ModCreationParams:
    """
    Dataclass to validate and store mod creation parameters.
    """
    mod_name: str
    abbreviation: str
    tags: List[str]
    supported_version: Optional[str] = None

    def __post_init__(self):
        """
        Validate mod creation parameters.
        """
        # Validate mod name
        if not self.mod_name or len(self.mod_name) < 3:
            raise ValueError("Mod name must be at least 3 characters long")
        
        # Load blocked names from JSON
        blocked_names_path = os.path.join(os.path.dirname(__file__), '../data/blocked_abbreviations.json')
        try:
            with open(blocked_names_path, 'r') as file:
                data = json.load(file)
                BLOCKED_ABBREVIATIONS = data['BLOCKED_ABBREVIATIONS']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Fallback to an empty list if file is not found or invalid
            BLOCKED_ABBREVIATIONS = []

        # Comprehensive validation for abbreviation
        if not self.abbreviation:
            raise ValueError("Abbreviation cannot be empty")

        if self.abbreviation.lower() in [name.lower() for name in BLOCKED_ABBREVIATIONS]:
            raise ValueError(f"The abbreviation '{self.abbreviation}' is already in use and cannot be used")

        # Check for valid characters (lowercase, numbers, underscores)
        if not re.match(r'^[a-z0-9_]+$', self.abbreviation):
            raise ValueError("Abbreviation must contain only lowercase letters, numbers, and underscores")

        # Length constraints
        if len(self.abbreviation) < 3 or len(self.abbreviation) > 30:
            raise ValueError("Abbreviation must be between 3 and 30 characters long")