"""
Query Planner Agent using the new framework
"""
from typing import List, AsyncGenerator
from pydantic import BaseModel, Field
from .agent import Agent, AgentConfig
from .decorators import agent_tool
from agents import trace
from models.research_models import SearchQuery
import json


class QueryPlannerAgent(Agent):
    """Agent for planning intelligent search queries"""
    
    def __init__(self):
        config = AgentConfig(
            name="QueryPlanner",
            description="Plans intelligent search queries with reasoning",
            model="gpt-4",
            temperature=0.7
        )
        super().__init__(config)
    
    async def execute(self, user_query: str) -> List[SearchQuery]:
        """Execute query planning"""
        return await self.plan_queries(user_query)
    
    @agent_tool("plan_queries", "Plan intelligent search queries with reasoning")
    async def plan_queries(self, user_query: str) -> List[SearchQuery]:
        """Plan intelligent search queries"""
        with trace("Query Planning"):
            try:
                
                planning_prompt = f"""
                You are an expert research strategist. Given the user query: "{user_query}"
                
                Plan exactly 2 intelligent web search queries that will provide comprehensive coverage of this topic.
                For each query, provide:
                1. The search query text
                2. Reasoning for why this query is important
                3. What type of information it will likely uncover
                4. Priority (1 or 2)
                
                Respond in JSON format:
                {{
                    "queries": [
                        {{
                            "query": "search text",
                            "reasoning": "why this query is important",
                            "query_type": "type of information",
                            "priority": 1
                        }},
                        {{
                            "query": "search text",
                            "reasoning": "why this query is important", 
                            "query_type": "type of information",
                            "priority": 2
                        }}
                    ]
                }}
                """
                
                response = await self.call_model([
                    {"role": "system", "content": "You are an expert research strategist who plans comprehensive search strategies. Always respond with valid JSON."},
                    {"role": "user", "content": planning_prompt}
                ])
                
                # Parse the response
                try:
                    data = json.loads(response)
                    queries_data = data.get("queries", [])
                    
                    queries = []
                    for i, query_data in enumerate(queries_data):
                        search_query = SearchQuery(
                            query=query_data["query"],
                            reasoning=query_data["reasoning"],
                            query_type=query_data["query_type"],
                            priority=query_data.get("priority", i + 1)
                        )
                        queries.append(search_query)
                    
                    return queries
                    
                except json.JSONDecodeError:
                    # Fallback to simple queries
                    fallback_queries = [
                        SearchQuery(
                            query=user_query,
                            reasoning="Direct search for the main topic",
                            query_type="Primary information",
                            priority=1
                        ),
                        SearchQuery(
                            query=f"{user_query} latest developments",
                            reasoning="Search for recent updates and developments",
                            query_type="Recent developments",
                            priority=2
                        )
                    ]
                    return fallback_queries
                    
            except Exception as e:
                raise
