# Agent Skill Library

A modular, extensible framework for building AI agent capabilities. Define, register, and execute skills with a clean, type-safe architecture.

## 🎯 Overview

The Agent Skill Library provides a robust foundation for building AI agents with pluggable skills. Each skill is a self-contained unit of functionality that can be easily registered, discovered, and executed.

## ✨ Features

- **🔌 Pluggable Architecture**: Easy to add new skills without modifying core code
- **🔍 Smart Discovery**: Find skills by name, category, tags, or keyword search
- **✅ Type-Safe**: Strong parameter typing with automatic validation
- **📊 Self-Describing**: All skills expose their metadata and capabilities
- **🛡️ Error Resilient**: Comprehensive error handling and validation
- **⚡ Batch Execution**: Run multiple skills in sequence
- **📚 Well Documented**: Complete architecture documentation and examples

## 🚀 Quick Start

```python
from skill_library import SkillRegistry, SkillExecutor
from examples.skills import CalculatorSkill

# Create registry and executor
registry = SkillRegistry()
executor = SkillExecutor(registry)

# Register a skill
registry.register(CalculatorSkill())

# Execute the skill
result = executor.execute("calculator", {
    "operation": "add",
    "a": 10,
    "b": 5
})

print(f"Result: {result.data}")  # Output: Result: 15.0
```

## 📖 Documentation

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation on:
- Architecture overview
- Core components
- Creating custom skills
- API reference
- Design principles
- Extension guidelines

## 🎮 Try the Demo

Run the interactive demo to see the library in action:

```bash
python examples/demo.py
```

The demo showcases:
- Skill registration and discovery
- Parameter validation
- Multiple skill executions
- Search and filtering
- Batch operations

## 🏗️ Architecture

The library consists of three core components:

1. **BaseSkill**: Abstract base class for all skills
2. **SkillRegistry**: Central registry for skill management
3. **SkillExecutor**: Safe execution engine with validation

See the full architecture documentation in [ARCHITECTURE.md](ARCHITECTURE.md).

## 📦 Example Skills

The library includes example implementations:

- **CalculatorSkill**: Basic math operations (add, subtract, multiply, divide)
- **TextProcessorSkill**: Text manipulation (uppercase, lowercase, reverse, counting)
- **WebSearchSkill**: Simulated web search functionality

## 🔧 Creating a Custom Skill

```python
from skill_library import BaseSkill, SkillParameter, SkillResult, SkillParameterType

class MyCustomSkill(BaseSkill):
    @property
    def name(self) -> str:
        return "my_custom_skill"
    
    @property
    def description(self) -> str:
        return "Does something awesome"
    
    @property
    def parameters(self) -> list:
        return [
            SkillParameter(
                name="input",
                type=SkillParameterType.STRING,
                description="Input data",
                required=True
            )
        ]
    
    def execute(self, **kwargs) -> SkillResult:
        # Your skill logic here
        return SkillResult(success=True, data="result")
```

## 🛠️ Requirements

- Python 3.9+

No external dependencies required for the core library!

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional example skills
- Async execution support
- Skill dependency management
- Caching mechanisms
- Testing infrastructure

## 📄 License

Open source - free to use and extend.

## 🔗 Project Structure

```
.
├── skill_library/           # Core library
│   ├── __init__.py
│   ├── base_skill.py       # Base skill interface
│   ├── skill_registry.py   # Skill management
│   └── skill_executor.py   # Execution engine
├── examples/               # Example implementations
│   ├── skills/            # Example skills
│   │   ├── calculator.py
│   │   ├── text_processor.py
│   │   └── web_search.py
│   └── demo.py            # Interactive demo
├── ARCHITECTURE.md         # Detailed documentation
└── README.md              # This file
```