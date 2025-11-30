"""
memory_agent.py

High-level memory interface for ECHOFORM.
This is the gateway between agents and the SQL memory system.
"""

from typing import Dict, List
from memory import repository


class MemoryAgent:
    """
    Abstraction layer for memory.
    Keeps agents independent from SQL implementation.
    """

    # --------------------------------------------------
    # SESSION
    # --------------------------------------------------

    def new_session(self) -> str:
        """
        Create a new cognitive session.
        """
        return repository.create_session()

    # --------------------------------------------------
    # DIALOGUE
    # --------------------------------------------------

    def save_user_message(self, session_id: str, content: str):
        """
        Store user message.
        """
        repository.save_message(session_id, "user", content)

    def save_assistant_message(self, session_id: str, content: str):
        """
        Store assistant response.
        """
        repository.save_message(session_id, "assistant", content)

    def load_context(self, session_id: str) -> List[Dict]:
        """
        Fetch last N messages as context.
        """
        return repository.get_recent_context(session_id)

    # --------------------------------------------------
    # REASONING
    # --------------------------------------------------

    def save_reasoning(
        self,
        session_id: str,
        raw: str,
        compressed: str,
        traits: Dict
    ):
        """
        Persist reasoning snapshot (raw + compressed).
        """
        repository.save_reasoning_snapshot(
            session_uuid=session_id,
            raw_reasoning=raw,
            compressed=compressed,
            traits=traits,
        )

    # --------------------------------------------------
    # EVALUATION
    # --------------------------------------------------

    def save_evaluation(self, session_id: str, scores: Dict):
        """
        Persist evaluation metrics.
        """
        repository.save_evaluation(session_id, scores)

    # --------------------------------------------------
    # TRAITS
    # --------------------------------------------------

    def load_traits(self, session_id: str) -> Dict:
        """
        Load personality profile.
        """
        return repository.get_traits(session_id)

    def update_traits(self, session_id: str, traits: Dict):
        """
        Save mutated personality traits.
        """
        repository.update_traits(session_id, traits)

    # --------------------------------------------------
    # MUTATION
    # --------------------------------------------------

    def increment_mutation(self, session_id: str):
        """
        Increment mutation counter.
        """
        repository.increment_mutation_level(session_id)

    def get_mutation_level(self, session_id: str) -> int:
        """
        Fetch current mutation level.
        """
        return repository.get_mutation_level(session_id)
