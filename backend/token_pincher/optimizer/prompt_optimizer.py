class PromptOptimizer:

    RULES = [
        ("You are a helpful assistant", ""),
        ("Please carefully analyze", "Analyze"),
        ("Kindly", ""),
        ("Please", ""),
    ]

    def optimize(self, prompt: str) -> str:
        result = prompt
        for old, new in self.RULES:
            result = result.replace(old, new)
        return result.strip()

    def suggest(self, prompt: str) -> list[str]:
        suggestions = []

        if len(prompt) > 500:
            suggestions.append("reduce_prompt_length")

        if "You are a helpful assistant" in prompt:
            suggestions.append("remove_generic_instruction")

        if "Please" in prompt:
            suggestions.append("remove_politeness_words")

        return suggestions