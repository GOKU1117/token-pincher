class ClaudePricing:

    TABLE = {
        "sonnet": {"input": 3.0, "output": 15.0},
        "opus": {"input": 15.0, "output": 75.0},
    }

    def estimate(self, usage, model="sonnet"):
        price = self.TABLE[model]
        input_cost = usage.input_tokens / 1_000_000 * price["input"]
        output_cost = usage.output_tokens / 1_000_000 * price["output"]
        return round(input_cost + output_cost, 6)