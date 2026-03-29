from typing import List
from token_pincher.core.models import Message, TokenUsage


class ClaudeTokenizer:

    def count_tokens(self, messages: List[Message]) -> TokenUsage:
        total_chars = sum(len(m.get("content", "")) for m in messages)
        tokens = int(total_chars / 2)
        return TokenUsage(tokens, 0, tokens)