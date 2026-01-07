"""
Agent Skill Library - A modular framework for agent skills.

This library provides a flexible architecture for defining, registering,
and executing skills that can be used by AI agents.
"""

from .base_skill import BaseSkill, SkillParameter, SkillResult, SkillParameterType
from .skill_registry import SkillRegistry
from .skill_executor import SkillExecutor

__version__ = "0.1.0"
__all__ = [
    "BaseSkill",
    "SkillParameter",
    "SkillParameterType",
    "SkillResult",
    "SkillRegistry",
    "SkillExecutor",
]
