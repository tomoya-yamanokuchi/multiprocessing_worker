from typing import Any
import abc

class BaseWorker(abc.ABC):
    @abc.abstractmethod
    def execute(self, task: Any) -> Any:
        pass
