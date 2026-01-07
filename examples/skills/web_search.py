"""Web search skill (simulated) for searching information."""

from typing import List
from skill_library import BaseSkill, SkillParameter, SkillResult, SkillParameterType


class WebSearchSkill(BaseSkill):
    """Skill for simulating web search operations."""
    
    @property
    def name(self) -> str:
        return "web_search"
    
    @property
    def description(self) -> str:
        return "Simulates web search functionality (returns mock results)"
    
    @property
    def parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(
                name="query",
                type=SkillParameterType.STRING,
                description="The search query",
                required=True
            ),
            SkillParameter(
                name="max_results",
                type=SkillParameterType.INTEGER,
                description="Maximum number of results to return",
                required=False,
                default=5
            ),
        ]
    
    @property
    def category(self) -> str:
        return "search"
    
    @property
    def tags(self) -> List[str]:
        return ["web", "search", "information"]
    
    def execute(self, **kwargs) -> SkillResult:
        """Execute web search (simulated)."""
        query = kwargs.get("query")
        max_results = kwargs.get("max_results", 5)
        
        try:
            # Simulate search results
            mock_results = [
                {
                    "title": f"Result {i+1} for '{query}'",
                    "url": f"https://example.com/result{i+1}",
                    "snippet": f"This is a mock search result snippet for query: {query}"
                }
                for i in range(min(int(max_results), 10))
            ]
            
            return SkillResult(
                success=True,
                data=mock_results,
                metadata={
                    "query": query,
                    "result_count": len(mock_results),
                    "simulated": True
                }
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Search error: {str(e)}"
            )
