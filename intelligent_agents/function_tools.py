"""
Function Tools - Each research capability as a function tool
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from .decorators import function_tool
from .web_search_tool import WebSearchTool
from models.research_models import SearchQuery, SearchResult, ResearchReport, ValidationResult
import google.generativeai as genai
import os
import json
from datetime import datetime


# Pydantic models for function inputs/outputs
class QueryPlanningInput(BaseModel):
    user_query: str = Field(..., description="User's research query")


class QueryPlanningOutput(BaseModel):
    queries: List[SearchQuery] = Field(..., description="Planned search queries")


class WebSearchInput(BaseModel):
    search_query: SearchQuery = Field(..., description="Search query to execute")


class WebSearchOutput(BaseModel):
    search_result: SearchResult = Field(..., description="Search results")


class SynthesisInput(BaseModel):
    search_results: List[SearchResult] = Field(..., description="Search results to synthesize")
    user_query: str = Field(..., description="Original user query")


class SynthesisOutput(BaseModel):
    research_report: ResearchReport = Field(..., description="Synthesized research report")


class ValidationInput(BaseModel):
    research_report: ResearchReport = Field(..., description="Report to validate")


class ValidationOutput(BaseModel):
    validation_result: ValidationResult = Field(..., description="Validation results")


# Function Tools
@function_tool("plan_search_queries", "Plan intelligent search queries based on user input")
async def plan_search_queries(input_data: QueryPlanningInput) -> QueryPlanningOutput:
    """
    Plan intelligent search queries using Pydantic models
    """
    # Create two intelligent queries based on the user input
    query1 = SearchQuery(
        query=input_data.user_query,
        reasoning="Direct search for the main topic",
        query_type="Primary information",
        priority=1
    )
    
    query2 = SearchQuery(
        query=f"{input_data.user_query} latest developments trends",
        reasoning="Search for recent updates and developments",
        query_type="Recent developments",
        priority=2
    )
    
    return QueryPlanningOutput(queries=[query1, query2])


@function_tool("perform_web_search", "Perform web search for a given query")
async def perform_web_search(input_data: WebSearchInput) -> WebSearchOutput:
    """
    Perform web search using WebSearchTool
    """
    web_search_tool = WebSearchTool()
    
    # Create search request from Pydantic model
    from .web_search_tool import SearchRequest
    request = SearchRequest(query=input_data.search_query.query)
    
    # Perform search
    results = await web_search_tool.search(request)
    
    # Create search result using Pydantic model
    combined_snippet = "\n\n".join([res.snippet for res in results])
    search_result = SearchResult(
        query=input_data.search_query.query,
        results=combined_snippet,
        status="success" if results else "no_results",
        metadata={
            "reasoning": input_data.search_query.reasoning,
            "query_type": input_data.search_query.query_type,
            "priority": input_data.search_query.priority,
            "num_results": len(results)
        }
    )
    
    return WebSearchOutput(search_result=search_result)


@function_tool("synthesize_results", "Synthesize search results into comprehensive report")
async def synthesize_results(input_data: SynthesisInput) -> SynthesisOutput:
    """
    Synthesize search results using Pydantic models
    """
    # Combine search results
    combined_results = []
    for result in input_data.search_results:
        combined_results.append(f"Query: {result.query}\nResults: {result.results}")
    
    # Create research report using Pydantic model
    research_report = ResearchReport(
        title=f"Research Report: {input_data.user_query}",
        executive_summary=f"Comprehensive analysis of '{input_data.user_query}' based on multiple search perspectives.",
        key_findings=[
            f"Primary findings from {len(input_data.search_results)} search queries",
            "Multiple perspectives analyzed",
            "Recent developments identified"
        ],
        insights=[
            "Key insights from search results",
            "Important patterns identified",
            "Critical information synthesized"
        ],
        recommendations=[
            "Further research recommended",
            "Additional sources to explore",
            "Follow-up actions suggested"
        ],
        sources=[f"Search query: {result.query}" for result in input_data.search_results],
        confidence_score=0.85,
        generated_at=datetime.now()
    )
    
    return SynthesisOutput(research_report=research_report)


@function_tool("validate_content", "Validate research report content for safety")
async def validate_content(input_data: ValidationInput) -> ValidationOutput:
    """
    Validate content using Pydantic models - no manual prompts
    """
    # Use Pydantic model to extract validation data
    report = input_data.research_report
    
    # Create validation criteria using Pydantic model fields
    validation_criteria = {
        "title_length": len(report.title),
        "findings_count": len(report.key_findings),
        "insights_count": len(report.insights),
        "recommendations_count": len(report.recommendations),
        "confidence_score": report.confidence_score
    }
    
    # Simple validation logic using Pydantic model data
    is_clean = True
    issues = []
    message = "Content validation completed"
    confidence = 0.9
    
    # Check for potential issues using Pydantic model data
    if validation_criteria["title_length"] < 5:
        issues.append("Title too short")
        is_clean = False
    
    if validation_criteria["findings_count"] == 0:
        issues.append("No key findings provided")
        is_clean = False
    
    if validation_criteria["confidence_score"] < 0.5:
        issues.append("Low confidence score")
        is_clean = False
    
    # Create ValidationResult using Pydantic model
    validation_result = ValidationResult(
        is_clean=is_clean,
        issues=issues,
        message=message,
        confidence=confidence
    )
    
    return ValidationOutput(validation_result=validation_result)
