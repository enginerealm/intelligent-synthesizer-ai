"""
Decorators for agent functions
"""
from functools import wraps
from typing import Callable, Any, Dict
import asyncio
from agents import trace


def function_tool(name: str = None, description: str = None):
    """
    Decorator to mark a function as a function tool for agents
    
    Usage:
        @function_tool("search_web", "Search the web for information")
        async def search_web(query: str) -> str:
            # Implementation
    """
    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with trace(tool_name):
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    
                    return result
                    
                except Exception as e:
                    raise
        
        # Add metadata to the function
        wrapper._is_function_tool = True
        wrapper._tool_name = tool_name
        wrapper._tool_description = description or func.__doc__ or f"Tool: {tool_name}"
        
        return wrapper
    return decorator


def agent_tool(name: str = None, description: str = None):
    """
    Decorator to mark a method as an agent tool
    
    Usage:
        @agent_tool("plan_queries", "Plan search queries")
        async def plan_queries(self, query: str) -> List[SearchQuery]:
            # Implementation
    """
    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            with trace(tool_name):
                try:
                    result = await func(self, *args, **kwargs)
                    return result
                    
                except Exception as e:
                    raise
        
        # Add metadata to the function
        wrapper._is_agent_tool = True
        wrapper._tool_name = tool_name
        wrapper._tool_description = description or func.__doc__ or f"Agent tool: {tool_name}"
        
        return wrapper
    return decorator
