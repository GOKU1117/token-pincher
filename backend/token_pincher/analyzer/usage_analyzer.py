from token_pincher.core.models import TokenUsage

class UsageAnalyzer:

    THRESHOLDS = {
        "system_prompt_bloat": 500,   
        "high_total": 3000,
        "low_total": 20,
        "context_ratio": 0.7, 
    }

    def analyze(self, usage: TokenUsage, segments: list[dict] | None = None) -> list[dict]:
        warnings = []

        if usage.total_tokens > self.THRESHOLDS["high_total"]:
            warnings.append({
                "id": "high_token_usage",
                "severity": "high",
                "message": f"Total tokens ({usage.total_tokens}) exceeds 3k — consider splitting the task",
            })

        if usage.total_tokens < self.THRESHOLDS["low_total"]:
            warnings.append({
                "id": "prompt_too_short",
                "severity": "info",
                "message": "Prompt is very short — may produce vague output",
            })

        if segments:
            context_tokens = sum(
                len(s["content"].split()) * 1.3 
                for s in segments if s["type"] == "context"
            )
            if context_tokens / max(usage.input_tokens, 1) > self.THRESHOLDS["context_ratio"]:
                warnings.append({
                    "id": "context_dominated",
                    "severity": "medium",
                    "message": "Context is >70% of prompt — consider RAG or summarization",
                })

        return warnings