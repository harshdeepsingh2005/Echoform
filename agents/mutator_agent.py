"""
mutator_agent.py

Behavior evolution engine.
Mutates personality traits based on evaluation results.
"""

from typing import Dict

from config import (
    MUTATION_DELTAS,
    SCORING_THRESHOLDS,
    TRAIT_MIN,
    TRAIT_MAX,
)


class MutatorAgent:
    """
    Evolves personality traits over time.
    """

    def run(self, traits: Dict, scores: Dict) -> Dict:
        new_traits = traits.copy()
        overall = scores.get("overall", 0.5)

        if overall >= SCORING_THRESHOLDS["high_score"]:
            self._upgrade(new_traits)
        elif overall <= SCORING_THRESHOLDS["low_score"]:
            self._downgrade(new_traits)
        else:
            self._stabilize(new_traits)

        return self._clamp(new_traits)

    # --------------------------------------------------

    def _upgrade(self, traits: Dict):
        """
        High score → encourage abstraction + creativity.
        """
        traits["creativity"] += MUTATION_DELTAS["creativity_up"]
        traits["abstraction"] += MUTATION_DELTAS["abstraction_up"]
        traits["verbosity"] += MUTATION_DELTAS["verbosity_up"]

    # --------------------------------------------------

    def _downgrade(self, traits: Dict):
        """
        Low score → simplify.
        """
        traits["creativity"] += MUTATION_DELTAS["creativity_down"]
        traits["abstraction"] += MUTATION_DELTAS["abstraction_down"]
        traits["verbosity"] += MUTATION_DELTAS["verbosity_down"]

    # --------------------------------------------------

    def _stabilize(self, traits: Dict):
        """
        Minor drift in formality to avoid stagnation.
        """
        traits["formality"] += MUTATION_DELTAS["formality_up"]

    # --------------------------------------------------

    def _clamp(self, traits: Dict) -> Dict:
        """
        Clamp all traits to [0,1].
        """
        for key, value in traits.items():
            traits[key] = max(TRAIT_MIN, min(TRAIT_MAX, value))
        return traits
