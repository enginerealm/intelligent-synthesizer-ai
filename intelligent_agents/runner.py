"""
Runner class for orchestrating function tool execution
"""
from typing import Any, Dict, List, Optional, Callable
from .function_tools import (
    plan_search_queries, perform_web_search, 
    synthesize_results, validate_content,
    QueryPlanningInput, WebSearchInput, 
    SynthesisInput, ValidationInput
)


class Runner:
    """Orchestrates the execution of function tools"""

    def __init__(self):
        self.function_tools: Dict[str, Callable] = {
            "plan_search_queries": plan_search_queries,
            "perform_web_search": perform_web_search,
            "synthesize_results": synthesize_results,
            "validate_content": validate_content
        }
        self.execution_history: List[Dict[str, Any]] = []

    def register_tool(self, name: str, tool_function: Callable):
        """Register a function tool with the runner"""
        self.function_tools[name] = tool_function

    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a function tool by name"""
        return self.function_tools.get(name)

    async def run(self, tool_name: str, input_data: Any) -> Any:
        """
        Run a specific function tool with input data

        Args:
            tool_name: Name of the function tool to run
            input_data: Input data for the tool

        Returns:
            Result from the function tool execution
        """
        try:
            if tool_name not in self.function_tools:
                raise ValueError(f"Function tool '{tool_name}' not found")

            tool_function = self.function_tools[tool_name]
            result = await tool_function(input_data)

            # Record execution
            execution_record = {
                "tool_name": tool_name,
                "input_data": str(input_data)[:500],
                "result": str(result)[:500],
                "status": "success"
            }
            self.execution_history.append(execution_record)

            return result

        except Exception as e:
            # Record failed execution
            execution_record = {
                "tool_name": tool_name,
                "input_data": str(input_data)[:500],
                "error": str(e),
                "status": "error"
            }
            self.execution_history.append(execution_record)
            raise

    async def run_sequence(self, sequence: List[Dict[str, Any]]) -> List[Any]:
        """
        Run a sequence of function tools

        Args:
            sequence: List of dictionaries with 'tool' and 'input' keys

        Returns:
            List of results from each tool execution
        """
        try:
            results = []
            for i, step in enumerate(sequence):
                tool_name = step["tool"]
                input_data = step.get("input")

                result = await self.run(tool_name, input_data)
                results.append(result)

            return results

        except Exception as e:
            raise

    async def run_parallel(self, tasks: List[Dict[str, Any]]) -> List[Any]:
        """
        Run multiple function tools in parallel

        Args:
            tasks: List of dictionaries with 'tool' and 'input' keys

        Returns:
            List of results from each tool execution
        """
        import asyncio

        try:
            async def run_task(task):
                tool_name = task["tool"]
                input_data = task.get("input")
                return await self.run(tool_name, input_data)

            results = await asyncio.gather(*[run_task(task) for task in tasks])
            return results

        except Exception as e:
            raise

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history"""
        return self.execution_history.copy()