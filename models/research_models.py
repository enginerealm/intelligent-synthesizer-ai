"""
Pydantic models for the Intelligent Research Synthesizer
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from enum import Enum


class SearchQuery(BaseModel):
    """Model for a single search query with reasoning"""
    query: str = Field(..., description="The search query text")
    reasoning: str = Field(..., description="Why this query is important")
    query_type: str = Field(..., description="Type of information this query will uncover")
    priority: int = Field(default=1, ge=1, le=2, description="Priority of the query (1-2)")


class SearchResult(BaseModel):
    """Model for a single search result"""
    query: str = Field(..., description="The original search query")
    results: str = Field(..., description="The search results content")
    status: Literal["success", "error"] = Field(..., description="Status of the search")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the search was performed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ValidationResult(BaseModel):
    """Model for content validation results"""
    is_clean: bool = Field(..., description="Whether the content is clean")
    issues: List[str] = Field(default_factory=list, description="List of issues found")
    message: str = Field(..., description="Validation message")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    timestamp: datetime = Field(default_factory=datetime.now, description="When validation was performed")


class ResearchReport(BaseModel):
    """Model for the final research report"""
    title: str = Field(..., description="Report title")
    executive_summary: str = Field(..., description="Executive summary")
    key_findings: List[str] = Field(default_factory=list, description="Key findings")
    insights: List[str] = Field(default_factory=list, description="Important insights")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    sources: List[str] = Field(default_factory=list, description="Source references")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall confidence score")
    generated_at: datetime = Field(default_factory=datetime.now, description="When the report was generated")
    validation_result: Optional[ValidationResult] = Field(None, description="Content validation results")


class AgentStatus(BaseModel):
    """Model for agent status and progress"""
    agent_name: str = Field(..., description="Name of the agent")
    status: Literal["idle", "running", "completed", "error"] = Field(..., description="Current status")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Progress percentage")
    message: str = Field(default="", description="Status message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")


class ResearchRequest(BaseModel):
    """Model for a research request"""
    query: str = Field(..., description="The user's research query")
    user_id: Optional[str] = Field(None, description="User identifier")
    max_searches: int = Field(default=2, ge=1, le=5, description="Maximum number of searches")
    include_validation: bool = Field(default=True, description="Whether to include content validation")
    created_at: datetime = Field(default_factory=datetime.now, description="When the request was created")


class ResearchResponse(BaseModel):
    """Model for the research response"""
    request: ResearchRequest = Field(..., description="The original request")
    report: ResearchReport = Field(..., description="The generated report")
    agent_statuses: List[AgentStatus] = Field(default_factory=list, description="Status of all agents")
    total_processing_time: float = Field(default=0.0, description="Total processing time in seconds")
    success: bool = Field(..., description="Whether the research was successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class AgentTool(BaseModel):
    """Model for agent tools"""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    input_schema: Dict[str, Any] = Field(..., description="Input schema for the tool")
    output_schema: Dict[str, Any] = Field(..., description="Output schema for the tool")
    is_async: bool = Field(default=True, description="Whether the tool is async")


class TraceEvent(BaseModel):
    """Model for OpenAI tracing events"""
    event_type: str = Field(..., description="Type of trace event")
    agent_name: str = Field(..., description="Name of the agent")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    duration: Optional[float] = Field(None, description="Event duration in seconds")
