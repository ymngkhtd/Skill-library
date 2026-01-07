"""
Basic tests for Agent Skill Library.

These tests verify core functionality of the library architecture.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skill_library import (
    BaseSkill, 
    SkillParameter, 
    SkillResult, 
    SkillParameterType,
    SkillRegistry,
    SkillExecutor
)


class TestSkill(BaseSkill):
    """A simple test skill."""
    
    @property
    def name(self) -> str:
        return "test_skill"
    
    @property
    def description(self) -> str:
        return "A test skill"
    
    @property
    def parameters(self) -> list:
        return [
            SkillParameter(
                name="value",
                type=SkillParameterType.STRING,
                description="Test value",
                required=True
            )
        ]
    
    def execute(self, **kwargs) -> SkillResult:
        value = kwargs.get("value")
        return SkillResult(success=True, data=f"Processed: {value}")


def test_skill_creation():
    """Test creating a skill."""
    print("Testing skill creation...")
    skill = TestSkill()
    assert skill.name == "test_skill"
    assert skill.description == "A test skill"
    assert len(skill.parameters) == 1
    print("✓ Skill creation test passed")


def test_skill_execution():
    """Test executing a skill."""
    print("Testing skill execution...")
    skill = TestSkill()
    result = skill.execute(value="test")
    assert result.success
    assert result.data == "Processed: test"
    print("✓ Skill execution test passed")


def test_registry():
    """Test skill registry."""
    print("Testing skill registry...")
    registry = SkillRegistry()
    skill = TestSkill()
    
    # Register skill
    registry.register(skill)
    assert "test_skill" in registry.list_skills()
    
    # Get skill
    retrieved = registry.get("test_skill")
    assert retrieved is not None
    assert retrieved.name == "test_skill"
    
    # Search
    found = registry.search("test")
    assert len(found) == 1
    
    print("✓ Registry test passed")


def test_executor():
    """Test skill executor."""
    print("Testing skill executor...")
    registry = SkillRegistry()
    executor = SkillExecutor(registry)
    
    # Register skill
    registry.register(TestSkill())
    
    # Execute with valid parameters
    result = executor.execute("test_skill", {"value": "hello"})
    assert result.success
    assert "hello" in result.data
    
    # Execute with missing parameters
    result = executor.execute("test_skill", {})
    assert not result.success
    assert "Missing required parameter" in result.error
    
    # Execute non-existent skill
    result = executor.execute("nonexistent", {})
    assert not result.success
    assert "not found" in result.error
    
    print("✓ Executor test passed")


def test_parameter_validation():
    """Test parameter validation."""
    print("Testing parameter validation...")
    skill = TestSkill()
    
    # Valid parameters
    is_valid, error = skill.validate_parameters(value="test")
    assert is_valid
    assert error is None
    
    # Missing required parameter
    is_valid, error = skill.validate_parameters()
    assert not is_valid
    assert "Missing required parameter" in error
    
    print("✓ Parameter validation test passed")


def test_batch_execution():
    """Test batch execution."""
    print("Testing batch execution...")
    registry = SkillRegistry()
    executor = SkillExecutor(registry)
    registry.register(TestSkill())
    
    executions = [
        ("test_skill", {"value": "first"}),
        ("test_skill", {"value": "second"}),
    ]
    
    results = executor.batch_execute(executions)
    assert len(results) == 2
    assert all(r.success for r in results)
    
    print("✓ Batch execution test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Agent Skill Library Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_skill_creation,
        test_skill_execution,
        test_registry,
        test_executor,
        test_parameter_validation,
        test_batch_execution,
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            return False
        except Exception as e:
            print(f"✗ {test.__name__} errored: {e}")
            return False
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
