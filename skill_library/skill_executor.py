"""Skill execution framework."""

import logging
from typing import Any, Dict, Optional
from .base_skill import BaseSkill, SkillResult
from .skill_registry import SkillRegistry


logger = logging.getLogger(__name__)


class SkillExecutor:
    """
    Executor for running skills with proper validation and error handling.
    """
    
    def __init__(self, registry: SkillRegistry):
        """
        Initialize the skill executor.
        
        Args:
            registry: The skill registry to use
        """
        self.registry = registry
    
    def execute(
        self,
        skill_name: str,
        parameters: Optional[Dict[str, Any]] = None,
        validate: bool = True
    ) -> SkillResult:
        """
        Execute a skill by name.
        
        Args:
            skill_name: Name of the skill to execute
            parameters: Parameters to pass to the skill
            validate: Whether to validate parameters before execution
            
        Returns:
            SkillResult: The result of the skill execution
        """
        if parameters is None:
            parameters = {}
        
        # Get the skill
        skill = self.registry.get(skill_name)
        if skill is None:
            return SkillResult(
                success=False,
                error=f"Skill '{skill_name}' not found in registry"
            )
        
        # Validate parameters if requested
        if validate:
            is_valid, error_msg = skill.validate_parameters(**parameters)
            if not is_valid:
                return SkillResult(
                    success=False,
                    error=f"Parameter validation failed: {error_msg}"
                )
        
        # Execute the skill
        try:
            logger.info(f"Executing skill: {skill_name}")
            result = skill.execute(**parameters)
            logger.info(f"Skill '{skill_name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing skill '{skill_name}': {str(e)}")
            return SkillResult(
                success=False,
                error=f"Execution error: {str(e)}"
            )
    
    def batch_execute(
        self,
        executions: list[tuple[str, Dict[str, Any]]]
    ) -> list[SkillResult]:
        """
        Execute multiple skills in sequence.
        
        Args:
            executions: List of (skill_name, parameters) tuples
            
        Returns:
            List of SkillResults
        """
        results = []
        for skill_name, parameters in executions:
            result = self.execute(skill_name, parameters)
            results.append(result)
        return results
