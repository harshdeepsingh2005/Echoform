"""
compressor_agent.py

Semantic compressor for ECHOFORM.
Reduces verbose reasoning into a compact cognitive fingerprint
for long-term storage and fast recall.
"""

from typing import Dict, List


class CompressorAgent:
    """
    Turns detailed reasoning into a condensed representation.
    """

    def run(self, reasoning: str, traits: Dict) -> str:
        """
        Main entry point for compression.
        Produces:
        - bullet-point summary
        - trait fingerprint
        - risk signal
        """
        key_points = self._extract_key_points(reasoning)
        fingerprint = self._build_fingerprint(traits)
        risk = traits.get("risk", "low")

        compressed = self._merge(key_points, fingerprint, risk)
        return compressed

    # --------------------------------------------------

    def _extract_key_points(self, text: str) -> List[str]:
        """
        Extract major reasoning steps.
        Lightweight unsupervised summarization via structure:
        - sentence boundaries
        - line heuristics
        """
        if not text.strip():
            return ["No reasoning provided."]

        # Split on lines if structured, else sentences
        if "\n" in text:
            lines = [l.strip() for l in text.split("\n") if l.strip()]
        else:
            lines = [s.strip() for s in text.split(".") if s.strip()]

        # Deduplicate overlapping points while preserving order
        seen = set()
        unique = []
        for l in lines:
            low = l.lower()
            if low not in seen:
                seen.add(low)
                unique.append(l)

        # Hard cap to prevent memory bloat
        return unique[:5]

    # --------------------------------------------------

    def _build_fingerprint(self, traits: Dict) -> str:
        """
        Convert observer traits into a compact string
        suitable for SQL storage & analysis.
        """
        tone = traits.get("tone", "unknown")
        bias = traits.get("bias", "none")
        depth = traits.get("depth", 0.0)
        abstraction = traits.get("abstraction", 0.0)

        return (
            f"tone={tone} | "
            f"bias={bias} | "
            f"depth={round(depth, 2)} | "
            f"abstraction={round(abstraction, 2)}"
        )

    # --------------------------------------------------

    def _merge(self, points: List[str], fingerprint: str, risk: str) -> str:
        """
        Merge bullet summary + fingerprint + risk tag.
        """
        bullets = " || ".join(points)
        return f"{bullets}  >>>  {fingerprint}  >>>  risk={risk}"
