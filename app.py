"""
app.py

Main execution engine for ECHOFORM.
Coordinates all agents in a cognition loop using Google Gemini ADK.
"""

import logging
import sys
from typing import Dict

from config import (
    ensure_directories,
    LOG_FILE_PATH,
    DEBUG,
    APP_NAME,
    APP_TAGLINE,
    LOG_TO_CONSOLE,
    gemini_enabled,
)
from memory.db import initialize_database
from agents.generator_agent import GeneratorAgent
from agents.observer_agent import ObserverAgent
from agents.compressor_agent import CompressorAgent
from agents.memory_agent import MemoryAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.mutator_agent import MutatorAgent


# ==================================================
# LOGGING
# ==================================================

def configure_logging():
    handlers = [logging.FileHandler(str(LOG_FILE_PATH), mode="a")]

    if LOG_TO_CONSOLE:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        handlers=handlers,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ==================================================
# ECHOFORM ENGINE
# ==================================================

class EchoformEngine:
    """
    Central intelligence orchestrator.

    Routes cognition via:
    Generator → Observer → Compressor → Memory → Evaluator → Mutator
    """

    def __init__(self):
        self.memory = MemoryAgent()
        self.generator = GeneratorAgent()
        self.observer = ObserverAgent()
        self.compressor = CompressorAgent()
        self.evaluator = EvaluatorAgent()
        self.mutator = MutatorAgent()

        self.session_id = self.memory.new_session()

        logging.info("[SYSTEM] ECHOFORM ENGINE STARTED")
        logging.info("[SYSTEM] Session ID: %s", self.session_id)
        logging.info("[SYSTEM] Gemini Enabled: %s", gemini_enabled())

    # ------------------------------------------------------

    def process_input(self, user_input: str) -> Dict:
        """
        One full cognition cycle.
        """

        # --------------------------------------------------
        # SAVE USER INPUT
        # --------------------------------------------------

        logging.info("[USER] %s", user_input)
        self.memory.save_user_message(self.session_id, user_input)

        # --------------------------------------------------
        # CONTEXT + TRAITS
        # --------------------------------------------------

        context = self.memory.load_context(self.session_id)
        traits = self.memory.load_traits(self.session_id)

        # --------------------------------------------------
        # GENERATE RESPONSE
        # --------------------------------------------------

        logging.info("[AGENT] Generator invoked")
        reply, reasoning = self.generator.run(
            user_input,
            context=context,
            traits=traits,
        )

        # --------------------------------------------------
        # OBSERVE REASONING
        # --------------------------------------------------

        logging.info("[AGENT] Observer invoked")
        analysis = self.observer.run(reasoning)

        # --------------------------------------------------
        # COMPRESS COGNITION
        # --------------------------------------------------

        logging.info("[AGENT] Compressor invoked")
        compressed = self.compressor.run(reasoning, analysis)

        # --------------------------------------------------
        # MEMORY WRITE
        # --------------------------------------------------

        self.memory.save_reasoning(
            session_id=self.session_id,
            raw=reasoning,
            compressed=compressed,
            traits=analysis,
        )

        # --------------------------------------------------
        # EVALUATION
        # --------------------------------------------------

        logging.info("[AGENT] Evaluator invoked")
        scores = self.evaluator.run(reply, analysis)

        self.memory.save_evaluation(
            session_id=self.session_id,
            scores=scores,
        )

        # --------------------------------------------------
        # MUTATION
        # --------------------------------------------------

        logging.info("[AGENT] Mutator invoked")
        new_traits = self.mutator.run(traits, scores)

        self.memory.update_traits(
            session_id=self.session_id,
            traits=new_traits,
        )

        self.memory.increment_mutation(self.session_id)

        # --------------------------------------------------
        # SAVE FINAL RESPONSE
        # --------------------------------------------------

        self.memory.save_assistant_message(self.session_id, reply)

        # --------------------------------------------------
        # LOG OUTPUT
        # --------------------------------------------------

        logging.info("[EVAL] %s", scores)
        logging.info("[MUTATION] %s", new_traits)

        # --------------------------------------------------
        # RETURN PACKAGE
        # --------------------------------------------------

        return {
            "reply": reply,
            "raw_reasoning": reasoning,
            "analysis": analysis,
            "compressed": compressed,
            "scores": scores,
            "mutation_level": self.memory.get_mutation_level(self.session_id),
            "traits": new_traits,
            "session_id": self.session_id,
            "gemini_enabled": gemini_enabled(),
        }


# ==================================================
# CLI ENTRYPOINT
# ==================================================

def main():
    ensure_directories()
    configure_logging()
    initialize_database()

    print("\n" + APP_NAME)
    print(APP_TAGLINE)
    print("=" * 60)
    print("Gemini Enabled:", gemini_enabled())
    print("Type 'exit' to quit.\n")

    engine = EchoformEngine()

    while True:
        user_input = input("You > ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("\n[ECHOFORM] Session closed.")
            break

        out = engine.process_input(user_input)

        print("\nECHOFORM >")
        print(out["reply"])

        print("\n--- SCORES ---")
        for k, v in out["scores"].items():
            print(f"{k}: {v}")

        print("\n--- TRAITS ---")
        for k, v in out["traits"].items():
            print(f"{k}: {round(v, 2)}")

        print(f"\n[MUTATION] Level: {out['mutation_level']}")
        print(f"[SESSION] {out['session_id']}")
        print(f"[GEMINI] {out['gemini_enabled']}")
        print("\n[REASONING]")
        print(out["raw_reasoning"])


if __name__ == "__main__":
    main()
