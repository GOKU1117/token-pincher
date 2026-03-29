import re
import requests
from token_pincher.optimizer.prompt_segmenter import PromptSegmenter

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"


class PromptOptimizer:
    """
    Two-stage compression:
      Stage 1 (coarse): rule-based, zero LLM calls
      Stage 2 (fine):   Llama3.2 via Ollama rewrites residual
    """

    WASTE_PATTERNS = [
        (r"you are a helpful assistant\.?\s*", ""),
        (r"you are an?\s+[\w\s]+?assistant\.?\s*", ""),
        (r"act as (?:a |an )?(?:professional |expert |senior )?[\w\s]+?\.\s*", ""),
        (r"(?:please |kindly )(?:help me |assist me )?", ""),
        (r"i (?:want|need) you to\s+", ""),
        (r"could you (?:please )?\s*", ""),
        (r"please carefully (?:analyze|read|consider|review|examine)\s*", ""),
        (r"\b(?:very |really |quite |extremely |absolutely )\b", ""),
        (r"\bin great detail\b", "in detail"),
        (r"\bstep[- ]by[- ]step\b", ""),
        (r"\bcarefully\b", ""),
        (r"\bthoroughly\b", ""),
        (r"\bcomprehensively\b", ""),
        (r"\bfully understand\b", "understand"),
        (r"\bplease and thank you\.?\s*$", ""),
        (r"\bthank you\.?\s*$", ""),
        (r"make sure (?:to |that )?", "ensure "),
        (r"analyze the following request and\s*", ""),
        (r"provide a detailed and comprehensive explanation\.?\s*", ""),
        (r"provide a (?:detailed|comprehensive|complete|full)\s+(?:and\s+\w+\s+)?(?:explanation|answer|response)\.?\s*", ""),
        (r"the following request", ""),
    ]

    def __init__(self):
        self.segmenter = PromptSegmenter()

   
    def _stage1(self, text: str) -> tuple[str, int]:
        result, count = text, 0
        for entry in self.WASTE_PATTERNS:
            pattern, repl = entry[0], entry[1]
            new = re.sub(pattern, repl, result, flags=re.IGNORECASE)
            if new != result:
                count += 1
            result = new
        result = re.sub(r"[ \t]{2,}", " ", result)
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result.strip(), count

   
    def _stage2(self, original: str, stage1: str, token_budget: int) -> str:
        prompt = (
            f"You are a prompt compression engine.\n"
            f"Rewrite the following prompt to be as short as possible "
            f"while preserving ALL semantic meaning.\n"
            f"Target: under {token_budget} tokens.\n"
            f"Output ONLY the rewritten prompt, no explanation.\n\n"
            f"Original:\n{original}\n\n"
            f"After rule-based compression:\n{stage1}\n\n"
            f"Final compressed prompt:"
        )
        try:
            res = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            }, timeout=60)
            res.raise_for_status()
            return res.json()["response"].strip()
        except Exception as e:
           
            print(f"[Stage 2 fallback] {e}")
            return stage1

 
    def optimize(self, prompt: str, token_budget: int | None = None) -> dict:
        segments = self.segmenter.segment(prompt)

        stage1_parts, total_rules = [], 0
        for seg in segments:
            compressed, rules = self._stage1(seg.content)
            if seg.type == "formatting" and len(compressed.split()) < 3:
                continue
            stage1_parts.append(compressed)
            total_rules += rules

        stage1_result = "\n".join(stage1_parts)

        final = stage1_result
        used_llm = False
        if token_budget is not None:
            estimated = int(len(stage1_result.split()) * 1.3)
            if estimated > token_budget:
                final = self._stage2(prompt, stage1_result, token_budget)
                used_llm = True

        orig_est = int(len(prompt.split()) * 1.3)
        final_est = int(len(final.split()) * 1.3)

        return {
            "stage1": stage1_result,
            "final": final,
            "used_llm": used_llm,
            "segments": [
                {"type": s.type, "content": s.content, "importance": s.importance}
                for s in segments
            ],
            "stats": {
                "original_tokens": orig_est,
                "optimized_tokens": final_est,
                "reduction_pct": round((1 - final_est / max(orig_est, 1)) * 100, 1),
                "rules_applied": total_rules,
            },
        }

    def suggest(self, prompt: str) -> list[dict]:
        suggestions = []
        segments = self.segmenter.segment(prompt)

        if any("helpful assistant" in s.content.lower() for s in segments):
            suggestions.append({
                "id": "remove_generic_role",
                "severity": "high",
                "description": "Generic role declaration — ~10 tokens, zero benefit",
                "fix": "Remove 'You are a helpful assistant'",
            })

        polite = len(re.findall(r"\b(please|kindly|could you)\b", prompt, re.I))
        if polite > 1:
            suggestions.append({
                "id": "remove_politeness",
                "severity": "medium",
                "description": f"{polite} politeness markers — LLMs don't respond to manners",
                "fix": "Replace 'Please help me write X' → 'Write X'",
            })

        if len(prompt.split()) > 200:
            suggestions.append({
                "id": "long_context",
                "severity": "medium",
                "description": "Context-heavy prompt — consider RAG or summarization",
                "fix": "Pre-summarize background before including it",
            })

        fmt_segs = [s for s in segments if s.type == "formatting"]
        if fmt_segs:
            suggestions.append({
                "id": "implicit_formatting",
                "severity": "low",
                "description": "Formatting instructions may be implicit from task type",
                "fix": "Use 'list X' instead of 'use bullet points to list X'",
            })

        return suggestions