import re
from dataclasses import dataclass


@dataclass
class PromptSegment:
    type: str        
    content: str
    importance: float  


class PromptSegmenter:
    """
    Decompose prompt into near-independent dimensions.
    Inspired by TurboQuant: each coordinate compressed independently.
    """

    INSTRUCTION_PATTERNS = [
        r"^(you are|act as|your role|as a|you must|you should)",
        r"^(please|kindly|could you|i want you to|i need you to)",
        r"\b(step by step|in detail|carefully|thoroughly|always|never)\b",
    ]

    FORMATTING_PATTERNS = [
        r"\b(respond in|format your|output should|use markdown|in json)\b",
        r"\b(bullet points?|numbered list|json format|table format)\b",
        r"\b(do not include|don't include|without preamble|no explanation)\b",
    ]

    EXAMPLE_PATTERNS = [
        r"^(example[:\-]|e\.g\.|for instance|input[:\-]|output[:\-])",
        r"^(here is an example|here's an example)",
    ]

    def segment(self, prompt: str) -> list[PromptSegment]:
        lines = [l.strip() for l in prompt.split("\n") if l.strip()]
        return [
            PromptSegment(
                type=(t := self._classify(l)),
                content=l,
                importance=self._score(l, t),
            )
            for l in lines
        ]

    def _classify(self, line: str) -> str:
        lo = line.lower()
        if any(re.search(p, lo) for p in self.EXAMPLE_PATTERNS):
            return "examples"
        if any(re.search(p, lo) for p in self.INSTRUCTION_PATTERNS):
            return "instruction"
        if any(re.search(p, lo) for p in self.FORMATTING_PATTERNS):
            return "formatting"
        return "context"

    def _score(self, line: str, seg_type: str) -> float:
        base = {"instruction": 0.85, "context": 0.6, "examples": 0.7, "formatting": 0.3}
        score = base.get(seg_type, 0.5)
        words = len(line.split())
        if words < 6:
            score += 0.1
        if words > 40:
            score -= 0.15
        return round(min(max(score, 0.0), 1.0), 2)