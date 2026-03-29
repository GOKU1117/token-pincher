from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str


@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass
class AnalysisResult:
    tokens: int
    cost: float
    warnings: list[str]