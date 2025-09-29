"""
Orchestrator - Manages agent flow using Runner pattern
"""
from typing import AsyncGenerator, List
from models.research_models import (
    ResearchRequest, ResearchReport, 
    SearchQuery, SearchResult, ValidationResult
)
from .runner import Runner
from .query_planner_agent import QueryPlannerAgent
from .web_searcher_agent import WebSearcherAgent
from .synthesis_agent import SynthesisAgent
from .output_guardrails_agent import OutputGuardrailsAgent
from agents import trace


class Orchestrator:
    def __init__(self):
        self.runner = Runner()
        self._setup_agents()
    
    def _setup_agents(self):
        """Setup all agents with the runner"""
        self.runner.register_agent("query_planner", QueryPlannerAgent())
        self.runner.register_agent("web_searcher", WebSearcherAgent())
        self.runner.register_agent("synthesis", SynthesisAgent())
        self.runner.register_agent("output_guardrails", OutputGuardrailsAgent())
    
    async def run_research(self, user_query: str) -> AsyncGenerator[str, None]:
        """
        Main orchestration method using Runner pattern
        """
        with trace("Research Orchestration"):
            try:
                # Initialize request
                request = ResearchRequest(query=user_query)
                
                yield "🚀 Starting intelligent research orchestration...\n"
                
                # Step 1: Plan search queries
                yield "📋 Planning intelligent search strategy...\n"
                search_queries = await self.runner.run("query_planner", user_query)
                
                for query in search_queries:
                    yield f"✅ Planned query: {query.query[:50]}...\n"
                
                # Step 2: Perform web searches
                yield "🌐 Performing intelligent web searches...\n"
                search_results = []
                for i, search_query in enumerate(search_queries, 1):
                    yield f"🔍 Search {i}/{len(search_queries)}: {search_query.query[:50]}...\n"
                    
                    result = await self.runner.run("web_searcher", search_query)
                    search_results.append(result)
                    yield f"✅ Search completed: {result.status}\n"
                
                # Step 3: Synthesize results
                yield "📝 Synthesizing research findings...\n"
                synthesis_input = {"search_results": search_results, "user_query": user_query}
                final_report = await self.runner.run("synthesis", synthesis_input)
                yield f"✅ Report generated: {final_report.title}\n"
                
                # Step 4: Validate content
                yield "🔍 Validating content for safety...\n"
                validation_result = await self.runner.run("output_guardrails", final_report)
                yield f"✅ Validation completed: {'Clean' if validation_result.is_clean else 'Issues detected'}\n"
                
                # Step 5: Format final response
                yield "📄 Compiling final report...\n"
                final_response = self._format_final_report(final_report, validation_result, request)
                yield final_response
                
            except Exception as e:
                yield f"❌ Error in research orchestration: {str(e)}\n"
                raise
    
    def _format_final_report(self, report: ResearchReport, validation_result: ValidationResult, request: ResearchRequest) -> str:
        """
        Format the final report with all components
        """
        header = f"""
# 🔍 Intelligent Research Report
**Query**: {request.query}
**Generated**: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}
---
"""
        
        # Executive Summary
        executive_summary = f"""
## 📋 Executive Summary
{report.executive_summary}
"""
        
        # Key Findings
        key_findings = ""
        if report.key_findings:
            key_findings = f"""
## 🔍 Key Findings
{chr(10).join(f"• {finding}" for finding in report.key_findings)}
"""
        
        # Insights
        insights = ""
        if report.insights:
            insights = f"""
## 💡 Important Insights
{chr(10).join(f"• {insight}" for insight in report.insights)}
"""
        
        # Recommendations
        recommendations = ""
        if report.recommendations:
            recommendations = f"""
## 🎯 Recommendations
{chr(10).join(f"• {rec}" for rec in report.recommendations)}
"""
        
        # Sources
        sources = ""
        if report.sources:
            sources = f"""
## 📚 Sources
{chr(10).join(f"• {source}" for source in report.sources)}
"""
        
        # Validation section
        validation_section = ""
        if validation_result:
            status_icon = "✅" if validation_result.is_clean else "⚠️"
            validation_section = f"""
---
## 🛡️ Content Validation
{status_icon} **Status**: {'Clean' if validation_result.is_clean else 'Issues Detected'}
**Confidence**: {validation_result.confidence:.2f}
**Message**: {validation_result.message}
"""
            if validation_result.issues:
                validation_section += f"**Issues**: {', '.join(validation_result.issues)}\n"
        
        # Footer
        footer = f"""
---
## 📊 Report Metadata
- **Confidence Score**: {report.confidence_score:.2f}
- **Generated by**: Intelligent Research Synthesizer
- **Validation Model**: Gemini Pro
- **Processing Time**: {request.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return header + executive_summary + key_findings + insights + recommendations + sources + validation_section + footer
