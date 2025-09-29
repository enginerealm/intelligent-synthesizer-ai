"""
Runner class for orchestrating agent execution
"""
from typing import Any, Dict, List, Optional, AsyncGenerator
from .agent import Agent
from agents import trace


class Runner:
    """Orchestrates the execution of multiple agents"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.execution_history: List[Dict[str, Any]] = []
    
    def register_agent(self, name: str, agent: Agent):
        """Register an agent with the runner"""
        self.agents[name] = agent
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(name)
    
    async def run(self, agent_name: str, input_data: Any) -> Any:
        """
        Run a specific agent with input data
        
        Args:
            agent_name: Name of the agent to run
            input_data: Input data for the agent
            
        Returns:
            Result from the agent execution
        """
        with trace(f"Run Agent: {agent_name}"):
            try:
                if agent_name not in self.agents:
                    raise ValueError(f"Agent '{agent_name}' not found")
                
                agent = self.agents[agent_name]
                result = await agent.execute(input_data)
                
                # Record execution
                execution_record = {
                    "agent_name": agent_name,
                    "input_data": str(input_data)[:500],
                    "result": str(result)[:500],
                    "status": "success"
                }
                self.execution_history.append(execution_record)
                
                return result
                
            except Exception as e:
                # Record failed execution
                execution_record = {
                    "agent_name": agent_name,
                    "input_data": str(input_data)[:500],
                    "error": str(e),
                    "status": "error"
                }
                self.execution_history.append(execution_record)
                raise
    
    async def run_sequence(self, sequence: List[Dict[str, Any]]) -> List[Any]:
        """
        Run a sequence of agents
        
        Args:
            sequence: List of dictionaries with 'agent' and 'input' keys
            
        Returns:
            List of results from each agent execution
        """
        with trace("Run Sequence"):
            try:
                results = []
                for i, step in enumerate(sequence):
                    agent_name = step["agent"]
                    input_data = step.get("input")
                    
                    result = await self.run(agent_name, input_data)
                    results.append(result)
                
                return results
                
            except Exception as e:
                raise
    
    async def run_parallel(self, tasks: List[Dict[str, Any]]) -> List[Any]:
        """
        Run multiple agents in parallel
        
        Args:
            tasks: List of dictionaries with 'agent' and 'input' keys
            
        Returns:
            List of results from each agent execution
        """
        import asyncio
        
        with trace("Run Parallel"):
            try:
                async def run_task(task):
                    agent_name = task["agent"]
                    input_data = task.get("input")
                    return await self.run(agent_name, input_data)
                
                results = await asyncio.gather(*[run_task(task) for task in tasks])
                return results
                
            except Exception as e:
                raise
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history"""
        return self.execution_history.copy()
    
    def clear_history(self):
        """Clear the execution history"""
        self.execution_history.clear()
