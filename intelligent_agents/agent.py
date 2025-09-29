"""
Base Agent class for the intelligent research system
"""
from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class AgentConfig(BaseModel):
    """Configuration for an agent"""
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    model: str = Field(default="gpt-4", description="Model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")
    timeout: int = Field(default=30, description="Timeout in seconds")


class Agent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Execute the agent's main functionality"""
        pass
    
    
    async def call_model(self, messages: list, **kwargs) -> str:
        """Call the OpenAI model with the agent's configuration"""
        model_kwargs = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
        }
        
        if self.config.max_tokens:
            model_kwargs["max_tokens"] = self.config.max_tokens
        
        # Override with any provided kwargs
        model_kwargs.update(kwargs)
        
        response = self.client.chat.completions.create(**model_kwargs)
        return response.choices[0].message.content
    
