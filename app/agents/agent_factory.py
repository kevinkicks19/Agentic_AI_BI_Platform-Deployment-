from typing import Dict, Any, List
import yaml
from app.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class AgentFactory:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.agents: Dict[str, BaseAgent] = {}
    
    def load_config(self) -> Dict[str, Any]:
        """Load agent configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Error loading agent config: {str(e)}")
            return {}
    
    def create_agents(self) -> Dict[str, BaseAgent]:
        """Create agents from configuration"""
        config = self.load_config()
        
        for agent_config in config.get('agents', []):
            try:
                name = agent_config['name']
                system_message = agent_config['system_message']
                
                logger.info(f"Creating agent: {name}")
                agent = BaseAgent(name, system_message)
                self.agents[name] = agent
                
            except Exception as e:
                logger.error(f"Error creating agent {name}: {str(e)}")
        
        return self.agents
    
    def get_agent(self, name: str) -> BaseAgent:
        """Get an agent by name"""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys()) 