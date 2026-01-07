"""Calculator skill for mathematical operations."""

from skill_library import BaseSkill, SkillParameter, SkillResult, SkillParameterType


class CalculatorSkill(BaseSkill):
    """Skill for performing basic mathematical calculations."""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Performs basic mathematical operations: add, subtract, multiply, divide"
    
    @property
    def parameters(self) -> list[SkillParameter]:
        return [
            SkillParameter(
                name="operation",
                type=SkillParameterType.STRING,
                description="Operation to perform: add, subtract, multiply, divide",
                required=True
            ),
            SkillParameter(
                name="a",
                type=SkillParameterType.FLOAT,
                description="First operand",
                required=True
            ),
            SkillParameter(
                name="b",
                type=SkillParameterType.FLOAT,
                description="Second operand",
                required=True
            ),
        ]
    
    @property
    def category(self) -> str:
        return "math"
    
    @property
    def tags(self) -> list[str]:
        return ["calculator", "math", "arithmetic"]
    
    def execute(self, **kwargs) -> SkillResult:
        """Execute the calculation."""
        operation = kwargs.get("operation")
        a = float(kwargs.get("a"))
        b = float(kwargs.get("b"))
        
        try:
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                if b == 0:
                    return SkillResult(
                        success=False,
                        error="Division by zero is not allowed"
                    )
                result = a / b
            else:
                return SkillResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )
            
            return SkillResult(
                success=True,
                data=result,
                metadata={"operation": operation, "a": a, "b": b}
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Calculation error: {str(e)}"
            )
