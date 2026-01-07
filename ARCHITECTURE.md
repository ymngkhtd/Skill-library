# Agent Skill Library Architecture

A modular, extensible framework for defining, managing, and executing agent skills. This library provides a clean architecture for building AI agents with pluggable capabilities.

## 🏗️ Architecture Overview

The Agent Skill Library is built on three core components:

### 1. **BaseSkill** - Abstract Skill Interface
The foundation for all skills, defining:
- Skill metadata (name, description, version, category, tags)
- Parameter definitions with types and validation
- Execution contract
- Metadata introspection

### 2. **SkillRegistry** - Skill Management
Central registry providing:
- Skill registration and discovery
- Search and filtering (by name, category, tags)
- Metadata querying
- Skill lifecycle management

### 3. **SkillExecutor** - Execution Engine
Safe execution framework with:
- Parameter validation
- Error handling
- Logging
- Batch execution support

## 📦 Directory Structure

```
skill_library/
├── __init__.py              # Package exports
├── base_skill.py            # BaseSkill abstract class and data structures
├── skill_registry.py        # SkillRegistry for managing skills
└── skill_executor.py        # SkillExecutor for running skills

examples/
├── skills/                  # Example skill implementations
│   ├── __init__.py
│   ├── calculator.py        # Math operations skill
│   ├── text_processor.py    # Text manipulation skill
│   └── web_search.py        # Web search skill (simulated)
└── demo.py                  # Interactive demonstration
```

## 🚀 Quick Start

### 1. Create a Custom Skill

```python
from skill_library import BaseSkill, SkillParameter, SkillResult, SkillParameterType

class MySkill(BaseSkill):
    @property
    def name(self) -> str:
        return "my_skill"
    
    @property
    def description(self) -> str:
        return "Description of what my skill does"
    
    @property
    def parameters(self) -> list:
        return [
            SkillParameter(
                name="input",
                type=SkillParameterType.STRING,
                description="Input parameter",
                required=True
            )
        ]
    
    def execute(self, **kwargs) -> SkillResult:
        input_value = kwargs.get("input")
        # Your skill logic here
        return SkillResult(
            success=True,
            data=f"Processed: {input_value}"
        )
```

### 2. Register and Execute Skills

```python
from skill_library import SkillRegistry, SkillExecutor

# Create registry and executor
registry = SkillRegistry()
executor = SkillExecutor(registry)

# Register skills
registry.register(MySkill())

# Execute a skill
result = executor.execute("my_skill", {"input": "Hello World"})
print(result.data)  # Output: Processed: Hello World
```

### 3. Discover Skills

```python
# List all skills
all_skills = registry.list_skills()

# Search by keyword
results = registry.search("text")

# Find by category
math_skills = registry.find_by_category("math")

# Find by tag
tagged = registry.find_by_tag("processing")
```

## 🎯 Key Features

### Type-Safe Parameters
Skills define their parameters with strong typing:
- STRING, INTEGER, FLOAT, BOOLEAN, LIST, DICT, ANY
- Required/optional parameters
- Default values
- Automatic validation

### Flexible Discovery
Find skills using multiple methods:
- By name
- By category
- By tags
- By keyword search

### Error Handling
Robust error handling with:
- Parameter validation
- Execution error catching
- Structured error messages
- Success/failure status

### Metadata-Driven
All skills are self-describing:
- Name and description
- Version tracking
- Categorization
- Parameter schemas

### Batch Execution
Execute multiple skills in sequence:
```python
executions = [
    ("skill1", {"param": "value1"}),
    ("skill2", {"param": "value2"}),
]
results = executor.batch_execute(executions)
```

## 📚 Example Skills

The library includes three example skills:

### CalculatorSkill
Performs basic math operations: add, subtract, multiply, divide
- **Category**: math
- **Tags**: calculator, math, arithmetic

### TextProcessorSkill
Processes text: uppercase, lowercase, reverse, count words/chars
- **Category**: text
- **Tags**: text, string, processing

### WebSearchSkill
Simulates web search with mock results
- **Category**: search
- **Tags**: web, search, information

## 🔧 Running the Demo

```bash
python examples/demo.py
```

The demo showcases:
1. Skill registration
2. Metadata inspection
3. Skill execution
4. Parameter validation
5. Search and discovery
6. Batch execution

## 🌟 Design Principles

1. **Modularity**: Each skill is self-contained and independent
2. **Extensibility**: Easy to add new skills without modifying core code
3. **Type Safety**: Strong typing and validation for parameters
4. **Introspection**: Skills are fully self-describing
5. **Error Resilience**: Graceful error handling at all levels
6. **Developer Friendly**: Simple, intuitive API

## 🛠️ Extending the Library

To add a new skill:

1. Inherit from `BaseSkill`
2. Implement required properties (name, description, parameters)
3. Implement the `execute()` method
4. Optionally set category, tags, and version
5. Register with the registry

The architecture is designed to be extended with:
- Custom skill categories
- Async execution support
- Skill dependencies
- Permission systems
- Caching mechanisms
- Skill versioning and updates

## 📄 License

Open source - feel free to use and extend this architecture for your agent systems.

## 🤝 Contributing

This is a foundational architecture. Contributions welcome for:
- New example skills
- Additional features
- Documentation improvements
- Testing infrastructure
- Performance optimizations
