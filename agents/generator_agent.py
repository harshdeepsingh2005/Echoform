"""
generator_agent.py

Primary intelligence engine for ECHOFORM using Google Gemini ADK.
Falls back to simulated cognition if Gemini is unavailable.
"""

import logging
import time
from typing import Dict, List, Tuple

from config import (
    GEMINI_API_KEY,
    DEFAULT_GEMINI_MODEL,
    GEMINI_MAX_RETRIES,
    GEMINI_STREAMING_ENABLED,
)

# Attempt Gemini import
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeneratorAgent:
    """
    Primary thinking agent.

    Uses Gemini via Google ADK when available.
    Otherwise, operates in offline simulation mode.
    """

    def __init__(self):
        self.use_gemini = bool(GEMINI_API_KEY) and GEMINI_AVAILABLE
        self.model_name = DEFAULT_GEMINI_MODEL
        self.model = None

        if self.use_gemini:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel(self.model_name)
                logging.info("[GENERATOR] Gemini model loaded: %s", self.model_name)
            except Exception as e:
                logging.error("[GENERATOR] Gemini init failed: %s", e)
                self.use_gemini = False

    # --------------------------------------------------

    def run(
        self,
        prompt: str,
        context: List[Dict[str, str]],
        traits: Dict[str, float],
    ) -> Tuple[str, str]:
        """
        Generate answer + reasoning.
        """
        if self.use_gemini and self.model:
            return self._run_gemini(prompt, context, traits)
        return self._run_simulated(prompt, traits)

    # --------------------------------------------------
    # GEMINI MODE
    # --------------------------------------------------

    def _run_gemini(self, prompt, context, traits):
        system_prompt = self._build_system_prompt(traits)
        memory_block = self._build_context(context)

        final_prompt = f"""
You are ECHOFORM — a reflective AI system.

SYSTEM CONFIGURATION:
{system_prompt}

CONVERSATION CONTEXT:
{memory_block}

USER PROMPT:
{prompt}

RESPONSE FORMAT (VERY IMPORTANT):
Write your answer in this exact structure:

MAIN ANSWER:
<your response for the user, clearly written>

REASONING TRACE:
<step-by-step explanation of how you arrived at the MAIN ANSWER, including how you used the traits, context and prompt>
"""

        last_error = None
        for i in range(GEMINI_MAX_RETRIES):
            try:
                logging.info("[GENERATOR] Gemini request attempt %s", i + 1)

                if GEMINI_STREAMING_ENABLED:
                    stream = self.model.generate_content(final_prompt, stream=True)
                    text = "".join(chunk.text for chunk in stream if getattr(chunk, "text", None))
                else:
                    response = self.model.generate_content(final_prompt)
                    text = response.text or ""

                text = text.strip()
                reasoning = self._extract_reasoning(text)
                final = self._remove_reasoning(text)
                return final, reasoning

            except Exception as e:
                logging.warning("[GENERATOR] Gemini attempt failed: %s", e)
                time.sleep(1.0)
                last_error = e

        logging.error("[GENERATOR] All Gemini attempts failed. Fallback engaged.")
        return self._run_simulated(prompt, traits)

    # --------------------------------------------------
    # FALLBACK MODE
    # --------------------------------------------------

    def _run_simulated(self, prompt, traits):
        abstraction = traits.get("abstraction", 0.5)
        creativity = traits.get("creativity", 0.5)

        reasoning = [
            f"Prompt interpreted: {prompt}",
            "Running in offline simulation mode (Gemini disabled)."
        ]

        if abstraction > 0.7:
            reasoning.append("High-level conceptual framing applied.")
        else:
            reasoning.append("Direct pragmatic interpretation applied.")

        if creativity > 0.7:
            reasoning.append("Creative deviation introduced.")
        else:
            reasoning.append("Standard response shaping applied.")

        reply = f"""
                    [SIMULATION MODE]

                    Your prompt was: {prompt}
                    This response was generated without Gemini.
                    """

        return reply.strip(), "\n".join(reasoning)

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def _build_system_prompt(self, traits):
        return f"""
                Creativity: {traits['creativity']}
                Abstraction: {traits['abstraction']}
                Verbosity: {traits['verbosity']}
                Formality: {traits['formality']}

                Use these to guide tone and complexity.
                """

    def _build_context(self, context):
        if not context:
            return "No previous context."

        return "\n".join(
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in context[-10:]
        )

    def _extract_reasoning(self, text: str) -> str:
        """
        Extract the internal reasoning from the model output.

        We expect the model to use the marker:

            REASONING TRACE:

        Anything after that is treated as reasoning.
        """
        marker = "REASONING TRACE:"
        if marker in text:
            return text.split(marker, 1)[1].strip()

        # Backwards compatibility (old format)
        if "[REASONING]" in text:
            return text.split("[REASONING]", 1)[1].strip()

        return "Gemini produced no explicit reasoning."



    def _remove_reasoning(self, text: str) -> str:
        """
        Strip the reasoning section and return only what should be shown to the user.

        We remove everything starting at REASONING TRACE: and also
        remove the leading 'MAIN ANSWER:' label if present.
        """
        marker = "REASONING TRACE:"
        if marker in text:
            main_part = text.split(marker, 1)[0]
        else:
            main_part = text

        # Drop the MAIN ANSWER label if it exists
        main_part = main_part.replace("MAIN ANSWER:", "").strip()
        return main_part

