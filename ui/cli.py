"""
cli.py

Command-line interface for ECHOFORM.
Used for development, debugging, and terminal demos.
"""

from app import EchoformEngine
from config import APP_NAME, APP_TAGLINE


def run_cli():
    print("\n" + "=" * 60)
    print(APP_NAME)
    print(APP_TAGLINE)
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    engine = EchoformEngine()

    while True:
        user_input = input("You > ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("\n[ECHOFORM] Session terminated.")
            break

        result = engine.process_input(user_input)

        print("\nECHOFORM >")
        print(result["reply"])

        print("\n--- SCORES ---")
        for k, v in result["scores"].items():
            print(f"{k}: {v}")

        print("\n--- TRAITS ---")
        for k, v in result["traits"].items():
            print(f"{k}: {round(v, 2)}")

        print(f"\n[MUTATION LEVEL] {result['mutation_level']}\n")


if __name__ == "__main__":
    run_cli()
