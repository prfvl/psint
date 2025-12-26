# modules/base_module.py
from abc import ABC, abstractmethod

class BaseModule(ABC):
    """Abstract Base Class that all OSINT modules must inherit from."""
    
    def __init__(self):
        self.name = "Base Module"
        self.description = "Generic module description"

    @abstractmethod
    async def run(self, target: str):
        """
        Main execution method for the module.
        Every child class MUST implement this method.
        """
        pass