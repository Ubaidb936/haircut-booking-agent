from abc import ABC, abstractmethod
from typing import List

class BaseAgent(ABC):
    @abstractmethod
    def start(self, thread_id: str):
        """Greets the customer"""

    @abstractmethod
    def resume(self, thread_id: str, message: str):
        """Continues until the customer is done booking the hair cut appointment"""    


