from token_pincher.core.models import TokenUsage


class UsageAnalyzer:

    def analyze(self, usage: TokenUsage) -> list[str]:
        warnings = []

        if usage.total_tokens > 3000:
            warnings.append("high_token_usage")

        if usage.total_tokens < 20:
            warnings.append("prompt_too_short")

        return warnings