"""
evaluator_agent.py

Performance evaluator for ECHOFORM.
Scores the output across multiple dimensions.
"""

from typing import Dict
from config import EVALUATION_WEIGHTS


class EvaluatorAgent:
    """
    Evaluates response quality and reasoning signatures.
    """

    def run(self, reply: str, traits: Dict) -> Dict[str, float]:
        accuracy = self._score_accuracy(reply)
        clarity = self._score_clarity(reply)
        depth = self._score_depth(traits)
        originality = self._score_originality(traits)

        overall = self._weighted_score(
            accuracy=accuracy,
            clarity=clarity,
            depth=depth,
            originality=originality,
        )

        return {
            "accuracy": round(accuracy, 2),
            "clarity": round(clarity, 2),
            "depth": round(depth, 2),
            "originality": round(originality, 2),
            "overall": round(overall, 2),
        }

    # --------------------------------------------------

    def _score_accuracy(self, reply: str) -> float:
        """
        Heuristic proxy for correctness.
        """
        if not reply.strip():
            return 0.2
        if "error" in reply.lower():
            return 0.4
        return 0.85

    # --------------------------------------------------

    def _score_clarity(self, reply: str) -> float:
        """
        Penalize extreme verbosity or emptiness.
        """
        words = len(reply.split())

        if words < 20:
            return 0.6
        if words > 350:
            return 0.7
        return 0.9

    # --------------------------------------------------

    def _score_depth(self, traits: Dict) -> float:
        """
        Observer depth score becomes the depth metric.
        """
        return float(traits.get("depth", 0.5))

    # --------------------------------------------------

    def _score_originality(self, traits: Dict) -> float:
        """
        Use abstraction level as novelty proxy.
        """
        abstraction = traits.get("abstraction", 0.5)
        creativity = traits.get("tone", "") == "creative"

        base = 0.5 + abstraction * 0.4
        if creativity:
            base += 0.1

        return min(1.0, base)

    # --------------------------------------------------

    def _weighted_score(self, **scores):
        """
        Combine all scores into a single metric.
        """
        total = 0.0
        for metric, weight in EVALUATION_WEIGHTS.items():
            total += scores.get(metric, 0.0) * weight
        return total
