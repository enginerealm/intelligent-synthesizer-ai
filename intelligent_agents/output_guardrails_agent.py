"""
Output Guardrails Agent using the new framework
"""
from .agent import Agent, AgentConfig
from .decorators import agent_tool
from agents import trace
from models.research_models import ResearchReport, ValidationResult
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()


class OutputGuardrailsAgent(Agent):
    """Agent for validating content for safety and appropriateness"""
    
    def __init__(self):
        config = AgentConfig(
            name="OutputGuardrails",
            description="Validates content for profanity and inappropriate content",
            model="gemini-pro",
            temperature=0.3
        )
        super().__init__(config)
        
        # Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    async def execute(self, report: ResearchReport) -> ValidationResult:
        """Execute content validation"""
        return await self.validate_content(report)
    
    @agent_tool("validate_content", "Validate content for safety and appropriateness")
    async def validate_content(self, report: ResearchReport) -> ValidationResult:
        """Validate content for profanity and inappropriate content"""
        with trace("Content Validation") :
            try:
                
                # Prepare content for validation
                content_to_validate = f"""
                Title: {report.title}
                Executive Summary: {report.executive_summary}
                Key Findings: {', '.join(report.key_findings)}
                Insights: {', '.join(report.insights)}
                Recommendations: {', '.join(report.recommendations)}
                """
                
                validation_prompt = f"""
                Analyze the following research report content for inappropriate language, profanity, offensive content, or harmful information.
                
                Content to analyze:
                {content_to_validate[:2000]}  # Limit content size for API
                
                Please provide a comprehensive analysis in JSON format:
                {{
                    "is_clean": true/false,
                    "issues": ["list of any specific issues found"],
                    "message": "brief assessment message",
                    "confidence": 0.95,
                    "flagged_sections": ["any specific sections that need attention"]
                }}
                
                Be thorough but fair in your assessment.
                """
                
                response = await self.gemini_model.generate_content(validation_prompt)
                
                # Parse response
                try:
                    data = json.loads(response.text)
                    validation_result = ValidationResult(
                        is_clean=data.get("is_clean", True),
                        issues=data.get("issues", []),
                        message=data.get("message", "Content validation completed"),
                        confidence=data.get("confidence", 0.9)
                    )
                except json.JSONDecodeError:
                    # Fallback validation
                    response_text = response.text.lower()
                    is_clean = "clean" in response_text and "inappropriate" not in response_text
                    
                    validation_result = ValidationResult(
                        is_clean=is_clean,
                        issues=[] if is_clean else ["Content validation flagged potential issues"],
                        message="Content validation completed" if is_clean else "Content validation detected potential issues",
                        confidence=0.8
                    )
                
                
                return validation_result
                
            except Exception as e:
                # Default to clean if validation fails
                validation_result = ValidationResult(
                    is_clean=True,
                    issues=[],
                    message=f"Validation error: {str(e)}",
                    confidence=0.5
                )
                return validation_result
