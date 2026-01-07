"""Skill registry for managing and discovering skills."""

from typing import Dict, List, Optional, Type
from .base_skill import BaseSkill


class SkillRegistry:
    """
    Central registry for managing skills.
    
    Provides methods to register, unregister, discover, and retrieve skills.
    """
    
    def __init__(self):
        """Initialize the skill registry."""
        self._skills: Dict[str, BaseSkill] = {}
        self._skill_classes: Dict[str, Type[BaseSkill]] = {}
    
    def register(self, skill: BaseSkill) -> None:
        """
        Register a skill instance.
        
        Args:
            skill: The skill instance to register
            
        Raises:
            ValueError: If a skill with the same name is already registered
        """
        if skill.name in self._skills:
            raise ValueError(f"Skill '{skill.name}' is already registered")
        
        self._skills[skill.name] = skill
        self._skill_classes[skill.name] = type(skill)
    
    def register_class(self, skill_class: Type[BaseSkill]) -> None:
        """
        Register a skill class and instantiate it.
        
        Args:
            skill_class: The skill class to register
        """
        skill_instance = skill_class()
        self.register(skill_instance)
    
    def unregister(self, skill_name: str) -> None:
        """
        Unregister a skill.
        
        Args:
            skill_name: Name of the skill to unregister
            
        Raises:
            KeyError: If the skill is not registered
        """
        if skill_name not in self._skills:
            raise KeyError(f"Skill '{skill_name}' is not registered")
        
        del self._skills[skill_name]
        del self._skill_classes[skill_name]
    
    def get(self, skill_name: str) -> Optional[BaseSkill]:
        """
        Get a skill by name.
        
        Args:
            skill_name: Name of the skill to retrieve
            
        Returns:
            The skill instance or None if not found
        """
        return self._skills.get(skill_name)
    
    def list_skills(self) -> List[str]:
        """
        List all registered skill names.
        
        Returns:
            List of skill names
        """
        return list(self._skills.keys())
    
    def find_by_category(self, category: str) -> List[BaseSkill]:
        """
        Find skills by category.
        
        Args:
            category: Category to search for
            
        Returns:
            List of skills in the category
        """
        return [
            skill for skill in self._skills.values()
            if skill.category == category
        ]
    
    def find_by_tag(self, tag: str) -> List[BaseSkill]:
        """
        Find skills by tag.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of skills with the tag
        """
        return [
            skill for skill in self._skills.values()
            if tag in skill.tags
        ]
    
    def search(self, query: str) -> List[BaseSkill]:
        """
        Search for skills by name or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching skills
        """
        query_lower = query.lower()
        return [
            skill for skill in self._skills.values()
            if query_lower in skill.name.lower() 
            or query_lower in skill.description.lower()
        ]
    
    def get_all_metadata(self) -> List[Dict]:
        """
        Get metadata for all registered skills.
        
        Returns:
            List of skill metadata dictionaries
        """
        return [skill.get_metadata() for skill in self._skills.values()]
    
    def clear(self) -> None:
        """Clear all registered skills."""
        self._skills.clear()
        self._skill_classes.clear()
