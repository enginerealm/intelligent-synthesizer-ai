"""
Orchestrator - Manages function tool flow using Runner pattern
"""
from typing import AsyncGenerator
from models.research_models import ResearchRequest
from .runner import Runner
from .function_tools import (
    QueryPlanningInput, WebSearchInput, 
    SynthesisInput, ValidationInput
)


class Orchestrator:
    def __init__(self):
        self.runner = Runner()

    async def run_research(self, user_query: str) -> AsyncGenerator[str, None]:
        """
        Main orchestration method using Runner pattern with function tools
        """
        try:
            # Initialize request
            request = ResearchRequest(query=user_query)

            yield "🚀 Starting intelligent research orchestration...\n"

            # Step 1: Plan search queries using function tool
            yield "📋 Planning intelligent search strategy...\n"
            planning_input = QueryPlanningInput(user_query=user_query)
            planning_result = await self.runner.run("plan_search_queries", planning_input)
            
            for query in planning_result.queries:
                yield f"✅ Planned query: {query.query[:50]}...\n"

            # Step 2: Perform web searches using function tools
            yield "🌐 Performing intelligent web searches...\n"
            search_results = []
            
            for i, search_query in enumerate(planning_result.queries, 1):
                yield f"🔍 Search {i}/{len(planning_result.queries)}: {search_query.query[:50]}...\n"
                
                search_input = WebSearchInput(search_query=search_query)
                search_result = await self.runner.run("perform_web_search", search_input)
                search_results.append(search_result.search_result)
                
                yield f"✅ Search completed: {search_result.search_result.status}\n"

            # Step 3: Synthesize results using function tool
            yield "📝 Synthesizing research findings...\n"
            synthesis_input = SynthesisInput(
                search_results=search_results,
                user_query=user_query
            )
            synthesis_result = await self.runner.run("synthesize_results", synthesis_input)
            yield f"✅ Report generated: {synthesis_result.research_report.title}\n"

            # Step 4: Validate content using function tool
            yield "🔍 Validating content for safety...\n"
            validation_input = ValidationInput(research_report=synthesis_result.research_report)
            validation_result = await self.runner.run("validate_content", validation_input)
            yield f"✅ Validation completed: {'Clean' if validation_result.validation_result.is_clean else 'Issues detected'}\n"

            # Step 5: Format final response
            yield "📄 Compiling final report...\n"
            final_response = self._format_final_report(
                synthesis_result.research_report, 
                validation_result.validation_result, 
                request
            )
            yield final_response

        except Exception as e:
            yield f"❌ Error in research orchestration: {str(e)}\n"
            raise

    def _format_final_report(self, report, validation_result, request) -> str:
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