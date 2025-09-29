"""
Synthesis Agent using the new framework
"""
from typing import List
from .agent import Agent, AgentConfig
from .decorators import agent_tool
from agents import trace
from models.research_models import SearchResult, ResearchReport
import json


class SynthesisAgent(Agent):
    """Agent for synthesizing search results into comprehensive reports"""
    
    def __init__(self):
        config = AgentConfig(
            name="SynthesisAgent",
            description="Synthesizes search results into comprehensive reports",
            model="gpt-4",
            temperature=0.3
        )
        super().__init__(config)
    
    async def execute(self, input_data) -> ResearchReport:
        """Execute synthesis"""
        if isinstance(input_data, dict):
            search_results = input_data.get("search_results", [])
            user_query = input_data.get("user_query", "")
        else:
            # Handle case where input_data is a list of SearchResult objects
            search_results = input_data
            user_query = "Research synthesis"
        
        return await self.synthesize_results(search_results, user_query)
    
    @agent_tool("synthesize_results", "Synthesize search results into a comprehensive report")
    async def synthesize_results(self, search_results: List[SearchResult], user_query: str) -> ResearchReport:
        """Synthesize search results into a comprehensive report"""
        with trace("Synthesis") :
            try:
                
                # Combine all results
                combined_results = "\n\n".join([
                    f"Query: {result.query}\nResults: {result.results}\nStatus: {result.status}"
                    for result in search_results
                ])
                
                synthesis_prompt = f"""
                You are an expert research analyst. Create a comprehensive research report based on the following search results.
                
                Original Query: {user_query}
                
                Search Results:
                {combined_results}
                
                Create a well-structured report in JSON format with the following structure:
                {{
                    "title": "Report title based on the query",
                    "executive_summary": "2-3 paragraph executive summary",
                    "key_findings": ["finding 1", "finding 2", "finding 3"],
                    "insights": ["insight 1", "insight 2", "insight 3"],
                    "recommendations": ["recommendation 1", "recommendation 2"],
                    "sources": ["source 1", "source 2"],
                    "confidence_score": 0.85
                }}
                
                Make the report comprehensive, well-structured, and actionable.
                """
                
                response = await self.call_model([
                    {"role": "system", "content": "You are an expert research analyst who creates comprehensive, well-structured reports. Always respond with valid JSON."},
                    {"role": "user", "content": synthesis_prompt}
                ])
                
                # Parse the response
                try:
                    data = json.loads(response)
                    
                    report = ResearchReport(
                        title=data.get("title", f"Research Report: {user_query}"),
                        executive_summary=data.get("executive_summary", ""),
                        key_findings=data.get("key_findings", []),
                        insights=data.get("insights", []),
                        recommendations=data.get("recommendations", []),
                        sources=data.get("sources", []),
                        confidence_score=data.get("confidence_score", 0.8)
                    )
                    
                    
                    return report
                    
                except json.JSONDecodeError:
                    # Fallback report
                    report = ResearchReport(
                        title=f"Research Report: {user_query}",
                        executive_summary="Comprehensive analysis based on web search results.",
                        key_findings=["Multiple perspectives analyzed", "Recent developments identified"],
                        insights=["Key insights from search results"],
                        recommendations=["Further research recommended"],
                        sources=["Web search results"],
                        confidence_score=0.7
                    )
                    return report
                    
            except Exception as e:
                raise
