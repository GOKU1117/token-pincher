from abc import ABC, abstractmethod
from typing import List
from token_pincher.core.models import Message, TokenUsage


class BaseProvider(ABC):

    @abstractmethod
    def count_tokens(self, messages: List[Message]) -> TokenUsage:
        raise NotImplementedError