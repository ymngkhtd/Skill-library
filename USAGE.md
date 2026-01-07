# Usage Guide - Agent Skill Library

This guide provides detailed examples and best practices for using the Agent Skill Library.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Creating Custom Skills](#creating-custom-skills)
4. [Advanced Features](#advanced-features)
5. [Best Practices](#best-practices)

## Installation

Since the library has no external dependencies, you can use it by simply cloning the repository:

```bash
git clone https://github.com/ymngkhtd/Skill-library.git
cd Skill-library
```

Or install it as a package:

```bash
pip install -e .
```

## Basic Usage

### 1. Setting Up Registry and Executor

```python
from skill_library import SkillRegistry, SkillExecutor

# Initialize
registry = SkillRegistry()
executor = SkillExecutor(registry)
```

### 2. Registering Skills

You can register skills in two ways:

**Method 1: Register an instance**
```python
from examples.skills import CalculatorSkill

skill = CalculatorSkill()
registry.register(skill)
```

**Method 2: Register a class**
```python
registry.register_class(CalculatorSkill)
```

### 3. Executing Skills

```python
# Execute with parameters
result = executor.execute("calculator", {
    "operation": "multiply",
    "a": 6,
    "b": 7
})

if result.success:
    print(f"Result: {result.data}")
else:
    print(f"Error: {result.error}")
```

### 4. Discovering Skills

```python
# List all skills
skills = registry.list_skills()
print(f"Available skills: {skills}")

# Search by keyword
text_skills = registry.search("text")

# Find by category
math_skills = registry.find_by_category("math")

# Find by tag
processing_skills = registry.find_by_tag("processing")

# Get detailed metadata
metadata = registry.get_all_metadata()
for skill_meta in metadata:
    print(f"{skill_meta['name']}: {skill_meta['description']}")
```

## Creating Custom Skills

### Basic Skill Template

```python
from typing import List
from skill_library import (
    BaseSkill, 
    SkillParameter, 
    SkillResult, 
    SkillParameterType
)

class MyCustomSkill(BaseSkill):
    """A custom skill that does something useful."""
    
    @property
    def name(self) -> str:
        """Unique identifier for the skill."""
        return "my_custom_skill"
    
    @property
    def description(self) -> str:
        """Human-readable description."""
        return "A skill that demonstrates custom functionality"
    
    @property
    def parameters(self) -> List[SkillParameter]:
        """Define what inputs the skill accepts."""
        return [
            SkillParameter(
                name="input_text",
                type=SkillParameterType.STRING,
                description="The text to process",
                required=True
            ),
            SkillParameter(
                name="count",
                type=SkillParameterType.INTEGER,
                description="Number of times to process",
                required=False,
                default=1
            ),
        ]
    
    @property
    def category(self) -> str:
        """Category for grouping skills."""
        return "custom"
    
    @property
    def tags(self) -> List[str]:
        """Tags for easy discovery."""
        return ["custom", "example"]
    
    @property
    def version(self) -> str:
        """Version of the skill."""
        return "1.0.0"
    
    def execute(self, **kwargs) -> SkillResult:
        """
        Main execution logic.
        
        Args:
            **kwargs: Parameters defined in self.parameters
            
        Returns:
            SkillResult with success status and data
        """
        input_text = kwargs.get("input_text")
        count = kwargs.get("count", 1)
        
        try:
            # Your skill logic here
            result_data = input_text * count
            
            return SkillResult(
                success=True,
                data=result_data,
                metadata={
                    "input_length": len(input_text),
                    "count": count
                }
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Execution failed: {str(e)}"
            )
```

### Advanced Skill Example: File Operations

```python
from pathlib import Path
from skill_library import BaseSkill, SkillParameter, SkillResult, SkillParameterType

class FileReaderSkill(BaseSkill):
    """Skill for reading file contents."""
    
    @property
    def name(self) -> str:
        return "file_reader"
    
    @property
    def description(self) -> str:
        return "Reads and returns the contents of a file"
    
    @property
    def parameters(self) -> list:
        return [
            SkillParameter(
                name="filepath",
                type=SkillParameterType.STRING,
                description="Path to the file to read",
                required=True
            ),
            SkillParameter(
                name="encoding",
                type=SkillParameterType.STRING,
                description="File encoding",
                required=False,
                default="utf-8"
            ),
        ]
    
    @property
    def category(self) -> str:
        return "io"
    
    @property
    def tags(self) -> list:
        return ["file", "io", "read"]
    
    def execute(self, **kwargs) -> SkillResult:
        filepath = kwargs.get("filepath")
        encoding = kwargs.get("encoding", "utf-8")
        
        try:
            path = Path(filepath)
            if not path.exists():
                return SkillResult(
                    success=False,
                    error=f"File not found: {filepath}"
                )
            
            content = path.read_text(encoding=encoding)
            
            return SkillResult(
                success=True,
                data=content,
                metadata={
                    "filepath": str(path),
                    "size_bytes": path.stat().st_size,
                    "encoding": encoding
                }
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Failed to read file: {str(e)}"
            )
```

## Advanced Features

### Batch Execution

Execute multiple skills in one go:

```python
executions = [
    ("calculator", {"operation": "add", "a": 10, "b": 20}),
    ("calculator", {"operation": "multiply", "a": 5, "b": 6}),
    ("text_processor", {"text": "Hello", "operation": "uppercase"}),
]

results = executor.batch_execute(executions)

for i, result in enumerate(results):
    print(f"Execution {i+1}: {result.data if result.success else result.error}")
```

### Parameter Validation

The executor automatically validates parameters, but you can also validate manually:

```python
skill = registry.get("calculator")
is_valid, error = skill.validate_parameters(
    operation="add",
    a=10,
    b=20
)

if not is_valid:
    print(f"Validation error: {error}")
```

### Disabling Validation

For performance-critical applications:

```python
result = executor.execute(
    "calculator",
    {"operation": "add", "a": 10, "b": 20},
    validate=False  # Skip parameter validation
)
```

### Skill Metadata Introspection

```python
skill = registry.get("calculator")

# Get all metadata
metadata = skill.get_metadata()
print(f"Name: {metadata['name']}")
print(f"Version: {metadata['version']}")
print(f"Category: {metadata['category']}")
print(f"Parameters:")
for param in metadata['parameters']:
    print(f"  - {param['name']}: {param['type']} ({'required' if param['required'] else 'optional'})")
```

## Best Practices

### 1. Skill Design

- **Single Responsibility**: Each skill should do one thing well
- **Clear Naming**: Use descriptive names that indicate what the skill does
- **Comprehensive Documentation**: Write clear descriptions for skills and parameters
- **Error Handling**: Always return SkillResult with appropriate error messages
- **Metadata**: Use categories and tags for better discoverability

### 2. Parameter Definition

- Use appropriate parameter types
- Provide clear descriptions
- Set sensible defaults for optional parameters
- Validate inputs within execute() if needed

### 3. Error Handling

```python
def execute(self, **kwargs) -> SkillResult:
    try:
        # Your code here
        return SkillResult(success=True, data=result)
    except SpecificException as e:
        return SkillResult(
            success=False,
            error=f"Specific error: {str(e)}"
        )
    except Exception as e:
        return SkillResult(
            success=False,
            error=f"Unexpected error: {str(e)}"
        )
```

### 4. Testing Skills

```python
# Test your skill
skill = MyCustomSkill()

# Test successful execution
result = skill.execute(input_text="test")
assert result.success
assert result.data is not None

# Test error handling
result = skill.execute()  # Missing required parameter
assert not result.success
assert result.error is not None
```

### 5. Registry Management

```python
# Clear registry when needed
registry.clear()

# Unregister specific skills
registry.unregister("skill_name")

# Check if skill exists before using
if registry.get("skill_name"):
    result = executor.execute("skill_name", params)
```

### 6. Organizing Skills

For larger projects, organize skills by category:

```
skills/
├── __init__.py
├── math/
│   ├── __init__.py
│   ├── calculator.py
│   └── statistics.py
├── text/
│   ├── __init__.py
│   ├── processor.py
│   └── analyzer.py
└── io/
    ├── __init__.py
    ├── file_reader.py
    └── file_writer.py
```

### 7. Logging

The SkillExecutor uses Python's logging module:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Now executor operations will be logged
result = executor.execute("skill_name", params)
```

## Next Steps

- Explore the example skills in `examples/skills/`
- Run the demo: `python examples/demo.py`
- Read the full architecture documentation in `ARCHITECTURE.md`
- Create your own custom skills for your use case

## Support

For issues, questions, or contributions, please visit the GitHub repository.
