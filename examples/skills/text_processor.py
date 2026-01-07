"""Text processing skill for string operations."""

from skill_library import BaseSkill, SkillParameter, SkillResult, SkillParameterType


class TextProcessorSkill(BaseSkill):
    """Skill for processing and manipulating text."""
    
    @property
    def name(self) -> str:
        return "text_processor"
    
    @property
    def description(self) -> str:
        return "Processes text with operations like uppercase, lowercase, reverse, count words"
    
    @property
    def parameters(self) -> list[SkillParameter]:
        return [
            SkillParameter(
                name="text",
                type=SkillParameterType.STRING,
                description="The text to process",
                required=True
            ),
            SkillParameter(
                name="operation",
                type=SkillParameterType.STRING,
                description="Operation: uppercase, lowercase, reverse, count_words, count_chars",
                required=True
            ),
        ]
    
    @property
    def category(self) -> str:
        return "text"
    
    @property
    def tags(self) -> list[str]:
        return ["text", "string", "processing"]
    
    def execute(self, **kwargs) -> SkillResult:
        """Execute text processing operation."""
        text = kwargs.get("text")
        operation = kwargs.get("operation")
        
        try:
            if operation == "uppercase":
                result = text.upper()
            elif operation == "lowercase":
                result = text.lower()
            elif operation == "reverse":
                result = text[::-1]
            elif operation == "count_words":
                result = len(text.split())
            elif operation == "count_chars":
                result = len(text)
            else:
                return SkillResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )
            
            return SkillResult(
                success=True,
                data=result,
                metadata={"operation": operation, "original_length": len(text)}
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Text processing error: {str(e)}"
            )
