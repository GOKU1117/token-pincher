from fastapi import FastAPI
from token_pincher.providers.claude.tokenizer import ClaudeTokenizer
from token_pincher.providers.claude.pricing import ClaudePricing
from token_pincher.analyzer.usage_analyzer import UsageAnalyzer
from token_pincher.optimizer.prompt_optimizer import PromptOptimizer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = ClaudeTokenizer()
pricing = ClaudePricing()
analyzer = UsageAnalyzer()
optimizer = PromptOptimizer()


@app.post("/analyze")
def analyze(data: dict):
    messages = data["messages"]
    usage = tokenizer.count_tokens(messages)
    cost = pricing.estimate(usage)
    warnings = analyzer.analyze(usage)

    return {
        "tokens": usage.total_tokens,
        "cost": cost,
        "warnings": warnings
    }


@app.post("/optimize")
def optimize(data: dict):
    prompt = data["prompt"]
    optimized = optimizer.optimize(prompt)
    suggestions = optimizer.suggest(prompt)

    return {
        "optimized": optimized,
        "suggestions": suggestions
    }