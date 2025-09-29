"""
WebSearchTool for performing web searches
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from openai import OpenAI
import os
from dotenv import load_dotenv
from agents import trace

load_dotenv()


class SearchRequest(BaseModel):
    """Request model for web search"""
    query: str = Field(..., description="Search query")
    max_results: int = Field(default=10, description="Maximum number of results")
    language: str = Field(default="en", description="Search language")
    region: str = Field(default="us", description="Search region")


class SearchResult(BaseModel):
    """Result model for web search"""
    title: str = Field(..., description="Result title")
    url: str = Field(..., description="Result URL")
    snippet: str = Field(..., description="Result snippet")
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Relevance score")


class WebSearchTool:
    """Tool for performing web searches using OpenAI's WebSearchTool"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tool_name = "WebSearchTool"
    
    async def search(self, request: SearchRequest) -> List[SearchResult]:
        """
        Perform a web search
        
        Args:
            request: Search request parameters
            
        Returns:
            List of search results
        """
        with trace("Web Search"):
            try:
                
                # Note: This is a placeholder for the actual WebSearchTool implementation
                # In practice, you would use OpenAI's WebSearchTool here
                search_prompt = f"""
                Search the web for: {request.query}
                
                Provide comprehensive information including:
                - Key findings and insights
                - Recent developments
                - Expert opinions
                - Statistical data if available
                - Multiple perspectives on the topic
                
                Format your response as a detailed research summary.
                """
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a web search expert. Provide comprehensive search results."},
                        {"role": "user", "content": search_prompt}
                    ],
                    temperature=0.3
                )
                
                # Simulate search results (in practice, you'd parse actual web search results)
                results = [
                    SearchResult(
                        title=f"Search Result 1 for {request.query}",
                        url="https://example.com/result1",
                        snippet=response.choices[0].message.content[:200] + "...",
                        relevance_score=0.9
                    ),
                    SearchResult(
                        title=f"Search Result 2 for {request.query}",
                        url="https://example.com/result2", 
                        snippet=response.choices[0].message.content[200:400] + "...",
                        relevance_score=0.8
                    )
                ]
                
                return results
                
            except Exception as e:
                raise
    
    async def search_multiple(self, queries: List[str]) -> Dict[str, List[SearchResult]]:
        """
        Perform multiple web searches
        
        Args:
            queries: List of search queries
            
        Returns:
            Dictionary mapping queries to their results
        """
        with trace("Multiple Web Searches"):
            try:
                results = {}
                for query in queries:
                    request = SearchRequest(query=query)
                    results[query] = await self.search(request)
                
                return results
                
            except Exception as e:
                raise
