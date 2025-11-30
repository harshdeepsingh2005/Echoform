"""
observer_agent.py

Meta-cognition engine.
Analyzes reasoning produced by Gemini or simulation.
Extracts:
- tone
- cognitive depth
- abstraction level
- bias risk
- hallucination risk
"""

from typing import Dict


class ObserverAgent:
    """
    Inspects the reasoning text and produces cognitive traits.
    """

    def run(self, reasoning: str) -> Dict:
        """
        Analyze the reasoning trace and return cognitive traits.
        """

        tone = self._detect_tone(reasoning)
        bias = self._detect_bias(reasoning)
        depth = self._estimate_depth(reasoning)
        abstraction = self._estimate_abstraction(reasoning)
        risk = self._estimate_risk(reasoning)

        return {
            "tone": tone,
            "bias": bias,
            "depth": round(depth, 2),
            "abstraction": round(abstraction, 2),
            "risk": risk,
        }

    # --------------------------------------------------

    def _detect_tone(self, text: str) -> str:
        """
        Heuristic tone detection.
        """
        t = text.lower()

        if any(k in t for k in ["theory", "concept", "paradigm", "abstract"]):
            return "philosophical"
        if any(k in t for k in ["example", "practical", "step", "implementation"]):
            return "practical"
        if any(k in t for k in ["analyze", "reason", "evaluate", "logic"]):
            return "analytical"
        if any(k in t for k in ["creative", "imagine", "novel", "unconventional"]):
            return "creative"
        return "neutral"

    # --------------------------------------------------

    def _detect_bias(self, text: str) -> str:
        """
        Rough bias signal detection.
        """
        t = text.lower()

        if "always" in t or "never" in t:
            return "overgeneralization"
        if "obviously" in t:
            return "confidence bias"
        if "best" in t or "worst" in t:
            return "extremism"
        return "none"

    # --------------------------------------------------

    def _estimate_depth(self, text: str) -> float:
        """
        Estimate cognitive depth from structure.
        """
        lines = [l for l in text.split("\n") if l.strip()]
        length_factor = min(1.0, len(lines) / 10)

        conjunctions = sum(
            1 for k in ["because", "therefore", "however", "thus"]
            if k in text.lower()
        )

        structure_factor = min(1.0, conjunctions * 0.2)
        return min(1.0, 0.3 + length_factor * 0.4 + structure_factor)

    # --------------------------------------------------

    def _estimate_abstraction(self, text: str) -> float:
        """
        Estimate abstract thinking.
        """
        keywords = [
            "concept", "model", "system", "framework",
            "abstraction", "layer", "architecture", "theory",
        ]

        hits = sum(1 for k in keywords if k in text.lower())
        return min(1.0, 0.4 + hits * 0.1)

    # --------------------------------------------------

    def _estimate_risk(self, text: str) -> str:
        """
        Detect hallucination or risk signals.
        """
        t = text.lower()

        if "i am not sure" in t or "unclear" in t:
            return "uncertain"
        if "guess" in t or "probably" in t:
            return "speculative"
        if "factually" in t and "source" not in t:
            return "hallucination-risk"
        return "low"
