from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):

    """Simple tool interface: return a (possible) updated dict for state merge"""
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        pass
