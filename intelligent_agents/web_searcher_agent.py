"""
Web Searcher Agent using the new framework
"""
from typing import List, AsyncGenerator
from .agent import Agent, AgentConfig
from .decorators import agent_tool
from .web_search_tool import WebSearchTool, SearchRequest
from agents import trace
from models.research_models import SearchQuery, SearchResult


class WebSearcherAgent(Agent):
    """Agent for performing web searches"""
    
    def __init__(self):
        config = AgentConfig(
            name="WebSearcher",
            description="Performs intelligent web searches",
            model="gpt-4",
            temperature=0.3
        )
        super().__init__(config)
        self.web_search_tool = WebSearchTool()
    
    async def execute(self, search_query: SearchQuery) -> SearchResult:
        """Execute web search"""
        return await self.search_web(search_query)
    
    @agent_tool("search_web", "Perform web search for a query")
    async def search_web(self, search_query: SearchQuery) -> SearchResult:
        """Perform web search"""
        with trace("Web Search") :
            try:
                
                # Use the WebSearchTool
                request = SearchRequest(
                    query=search_query.query,
                    max_results=10
                )
                
                results = await self.web_search_tool.search(request)
                
                # Combine results into a single SearchResult
                combined_content = "\n\n".join([
                    f"Title: {result.title}\nURL: {result.url}\nSnippet: {result.snippet}"
                    for result in results
                ])
                
                search_result = SearchResult(
                    query=search_query.query,
                    results=combined_content,
                    status="success",
                    metadata={
                        "reasoning": search_query.reasoning,
                        "query_type": search_query.query_type,
                        "priority": search_query.priority,
                        "result_count": len(results)
                    }
                )
                
                
                return search_result
                
            except Exception as e:
                error_result = SearchResult(
                    query=search_query.query,
                    results=f"Error performing search: {str(e)}",
                    status="error",
                    metadata={"error": str(e)}
                )
                return error_result
