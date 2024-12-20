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
    short_mod_name: str
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
        blocked_names_path = os.path.join(os.path.dirname(__file__), '../data/blocked_short_mod_names.json')
        try:
            with open(blocked_names_path, 'r') as file:
                data = json.load(file)
                BLOCKED_SHORT_MOD_NAMES = data['BLOCKED_SHORT_MOD_NAMES']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Fallback to an empty list if file is not found or invalid
            BLOCKED_SHORT_MOD_NAMES = []

        # Comprehensive validation for short mod name
        if not self.short_mod_name:
            raise ValueError("Short mod name cannot be empty")

        if self.short_mod_name in BLOCKED_SHORT_MOD_NAMES:
            raise ValueError(f"The short mod name '{self.short_mod_name}' is already in use and cannot be used")

        # Check for valid characters (lowercase, numbers, underscores)
        if not re.match(r'^[a-z0-9_]+$', self.short_mod_name):
            raise ValueError("Short mod name must contain only lowercase letters, numbers, and underscores")

        # Length constraints
        if len(self.short_mod_name) < 3 or len(self.short_mod_name) > 30:
            raise ValueError("Short mod name must be between 3 and 30 characters long")