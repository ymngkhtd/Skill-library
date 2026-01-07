#!/usr/bin/env python3
"""
Demo script showing how to use the Agent Skill Library.

This script demonstrates:
1. Creating and registering skills
2. Executing skills with validation
3. Searching and discovering skills
4. Batch execution
"""

import sys
import os

# Add parent directory to path to import skill_library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skill_library import SkillRegistry, SkillExecutor
from examples.skills import CalculatorSkill, TextProcessorSkill, WebSearchSkill


def main():
    print("=" * 60)
    print("Agent Skill Library - Demo")
    print("=" * 60)
    print()
    
    # Step 1: Create registry and executor
    print("1. Creating skill registry and executor...")
    registry = SkillRegistry()
    executor = SkillExecutor(registry)
    print("   ✓ Registry and executor created")
    print()
    
    # Step 2: Register skills
    print("2. Registering example skills...")
    registry.register(CalculatorSkill())
    registry.register(TextProcessorSkill())
    registry.register(WebSearchSkill())
    print(f"   ✓ Registered {len(registry.list_skills())} skills")
    print(f"   Skills: {', '.join(registry.list_skills())}")
    print()
    
    # Step 3: List skill metadata
    print("3. Listing skill metadata...")
    for metadata in registry.get_all_metadata():
        print(f"   - {metadata['name']}: {metadata['description']}")
        print(f"     Category: {metadata['category']}, Tags: {metadata['tags']}")
    print()
    
    # Step 4: Execute calculator skill
    print("4. Executing calculator skill (10 + 5)...")
    result = executor.execute("calculator", {
        "operation": "add",
        "a": 10,
        "b": 5
    })
    print(f"   Result: {result.data}")
    print(f"   Success: {result.success}")
    print()
    
    # Step 5: Execute text processor skill
    print("5. Executing text processor skill (uppercase)...")
    result = executor.execute("text_processor", {
        "text": "Hello, Agent Skill Library!",
        "operation": "uppercase"
    })
    print(f"   Result: {result.data}")
    print(f"   Success: {result.success}")
    print()
    
    # Step 6: Execute web search skill
    print("6. Executing web search skill...")
    result = executor.execute("web_search", {
        "query": "artificial intelligence",
        "max_results": 3
    })
    print(f"   Found {len(result.data)} results:")
    for i, item in enumerate(result.data, 1):
        print(f"   {i}. {item['title']}")
    print()
    
    # Step 7: Demonstrate parameter validation
    print("7. Demonstrating parameter validation...")
    result = executor.execute("calculator", {
        "operation": "divide",
        "a": 10
        # Missing 'b' parameter
    })
    print(f"   Success: {result.success}")
    print(f"   Error: {result.error}")
    print()
    
    # Step 8: Search for skills
    print("8. Searching for skills with 'text' keyword...")
    found_skills = registry.search("text")
    print(f"   Found {len(found_skills)} skills:")
    for skill in found_skills:
        print(f"   - {skill.name}")
    print()
    
    # Step 9: Find skills by category
    print("9. Finding skills by category 'math'...")
    math_skills = registry.find_by_category("math")
    print(f"   Found {len(math_skills)} skills:")
    for skill in math_skills:
        print(f"   - {skill.name}")
    print()
    
    # Step 10: Batch execution
    print("10. Batch execution example...")
    executions = [
        ("calculator", {"operation": "multiply", "a": 7, "b": 8}),
        ("text_processor", {"text": "batch", "operation": "uppercase"}),
    ]
    results = executor.batch_execute(executions)
    print(f"   Executed {len(results)} skills:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. Success: {result.success}, Data: {result.data}")
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
