from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from token_pincher.providers.claude.tokenizer import ClaudeTokenizer
from token_pincher.providers.claude.pricing import ClaudePricing
from token_pincher.analyzer.usage_analyzer import UsageAnalyzer
from token_pincher.optimizer.prompt_optimizer import PromptOptimizer

app = FastAPI(title="TokenPincher API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = ClaudeTokenizer()
pricing   = ClaudePricing()
analyzer  = UsageAnalyzer()
optimizer = PromptOptimizer()


class AnalyzeRequest(BaseModel):
    messages: list[dict]


class OptimizeRequest(BaseModel):
    prompt: str
    token_budget: int | None = None


@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    try:
        usage = tokenizer.count_tokens(data.messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    cost = pricing.estimate(usage)
    content = " ".join(m.get("content", "") for m in data.messages)
    opt = optimizer.optimize(content)
    warnings = analyzer.analyze(usage, opt["segments"])

    return {
        "tokens": usage.total_tokens,
        "input_tokens": usage.input_tokens,
        "cost": cost,
        "warnings": warnings,
        "segments": opt["segments"],
    }


@app.post("/optimize")
def optimize(data: OptimizeRequest):
    try:
        result = optimizer.optimize(data.prompt, token_budget=data.token_budget)
        suggestions = optimizer.suggest(data.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "original": data.prompt,
        "optimized": result["final"],
        "stage1": result["stage1"],
        "used_llm": result["used_llm"],
        "segments": result["segments"],
        "suggestions": suggestions,
        "stats": result["stats"],
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}