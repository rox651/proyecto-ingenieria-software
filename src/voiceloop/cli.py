"""CLI entry point for running the voice pipeline locally."""

import argparse
import asyncio
import logging

from voiceloop.pipeline import VoicePipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="VoiceLoop — asyncio voice agent")
    parser.add_argument("--turns", type=int, default=1, help="Max conversational turns")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    pipeline = VoicePipeline()
    results = asyncio.run(pipeline.run(max_turns=args.turns))

    for i, turn in enumerate(results, 1):
        print(f"\n--- Turn {i} ---")
        print(f"User:      {turn.user_text}")
        print(f"Assistant: {turn.assistant_text}")
