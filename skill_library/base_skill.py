"""Base skill interface and data structures."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class SkillParameterType(Enum):
    """Types of skill parameters."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    ANY = "any"


@dataclass
class SkillParameter:
    """Definition of a skill parameter."""
    name: str
    type: SkillParameterType
    description: str
    required: bool = True
    default: Any = None


@dataclass
class SkillResult:
    """Result of a skill execution."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseSkill(ABC):
    """
    Abstract base class for all skills.
    
    Skills are self-contained capabilities that agents can execute.
    Each skill must implement the execute method and define its metadata.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self._validate_metadata()
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the skill."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the skill does."""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> list[SkillParameter]:
        """Return the list of parameters this skill accepts."""
        pass
    
    @property
    def version(self) -> str:
        """Return the version of the skill."""
        return "1.0.0"
    
    @property
    def category(self) -> str:
        """Return the category of the skill."""
        return "general"
    
    @property
    def tags(self) -> list[str]:
        """Return tags associated with the skill."""
        return []
    
    @abstractmethod
    def execute(self, **kwargs) -> SkillResult:
        """
        Execute the skill with the given parameters.
        
        Args:
            **kwargs: Parameters for the skill execution
            
        Returns:
            SkillResult: The result of the skill execution
        """
        pass
    
    def validate_parameters(self, **kwargs) -> tuple[bool, Optional[str]]:
        """
        Validate the provided parameters against the skill's parameter definitions.
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        param_dict = {p.name: p for p in self.parameters}
        
        # Check required parameters
        for param in self.parameters:
            if param.required and param.name not in kwargs:
                if param.default is None:
                    return False, f"Missing required parameter: {param.name}"
        
        # Check for unknown parameters
        for key in kwargs:
            if key not in param_dict:
                return False, f"Unknown parameter: {key}"
        
        return True, None
    
    def _validate_metadata(self):
        """Validate that required metadata is properly defined."""
        if not self.name:
            raise ValueError("Skill name cannot be empty")
        if not self.description:
            raise ValueError("Skill description cannot be empty")
    
    def get_metadata(self) -> dict[str, Any]:
        """Return all metadata about the skill."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "tags": self.tags,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type.value,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                }
                for p in self.parameters
            ],
        }
