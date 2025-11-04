#!/usr/bin/env python3
"""
Interactive pyPet demo

Run:
  pipenv run python src/demo.py
"""

from __future__ import annotations

import time
from typing import Optional

from pypet import create_pet, play, status, feed, ALLOWED_SPECIES, ALLOWED_MOODS


def clear() -> None:
    print("\033[2J\033[H", end="")

def pause(msg: str = "Press Enter to continue...") -> None:
    try:
        input(msg)
    except EOFError:
        pass

def choose(prompt: str, choices: list[str], default: Optional[str] = None) -> str:
    """Simple numbered picker."""
    while True:
        print(prompt)
        for i, c in enumerate(choices, 1):
            print(f"  {i}. {c}")
        if default:
            print(f"[Enter for default: {default}]")
        sel = input("> ").strip()
        if not sel and default:
            return default
        if sel.isdigit() and 1 <= int(sel) <= len(choices):
            return choices[int(sel) - 1]
        print("Invalid choice. Try again.\n")

def spinner(text: str, seconds: float = 1.2) -> None:
    glyphs = "|/-\\"
    end = time.time() + seconds
    i = 0
    print(text, end=" ", flush=True)
    while time.time() < end:
        print(glyphs[i % len(glyphs)], end="\r", flush=True)
        time.sleep(0.08)
        i += 1
    print(" " * 20, end="\r")

def main() -> int:
    clear()
    print("🐾 Welcome to pyPet\n")

    name = input("Name your pet: ").strip() or "Mochi"
    species = choose("Pick a species:", sorted(ALLOWED_SPECIES), default="otter")
    mood = choose("Pick a starting mood:", sorted(ALLOWED_MOODS), default="neutral")

    pet = create_pet(name=name, species=species, mood=mood, hunger=40, energy=80)

    while True:
        clear()
        print("=== pyPet ===\n")
        print(status(pet, color=True, verbose=True, ascii_art=True))  # uses your package’s status()
        print("\nActions:")

        menu = [
            ("p", "Play"),
            ("f", "Feed"),
            ("r", "Rename pet"),
            ("m", "Change mood"),
            ("s", "Show status"),
            ("q", "Quit")
        ]

        print("  " + "  ".join(f"[{k}] {label}" for k, label in menu))
        choice = input("\n> ").strip().lower()

        if choice == "q":
            print("\nBye!")
            return 0

        elif choice == "s":
            print()
            print(status(pet, color=True, verbose=True, ascii_art=True))
            pause()
            continue

        elif choice == "r":
            new_name = input("New name: ").strip()
            if new_name:
                pet["name"] = new_name
            continue

        elif choice == "m":
            new_mood = choose("New mood:", sorted(ALLOWED_MOODS), default=pet.get("mood", "neutral"))
            pet["mood"] = new_mood

            pet["ascii_key"] = f"{pet['species']}:{pet['mood']}"
            continue

        elif choice == "p":
            game = choose("Game:", ["fetch", "tug", "chase", "hide-n-seek"], default="fetch")
            try:
                energy = int(input("How energetic is the play? (1–30, default 10): ").strip() or "10")
            except ValueError:
                energy = 10
            reward = input("Give a reward after? [y/N]: ").strip().lower().startswith("y")
            spinner("Playing...")
            play(pet, game, energy, reward)
            print("Done!")
            pause()
            continue

        elif choice == "f":
            food = choose("Food:", ["kibble", "fish", "berries", "treat"], default="kibble")
            try:
                portion = int(input("Portion size (1–30, default 8): ").strip() or "8")
            except ValueError:
                portion = 8
            treat = input("Is it a special treat? [y/N]: ").strip().lower().startswith("y")
            spinner("Feeding...")
            feed(pet, food, portion, treat)
            print("Yum!")
            pause()
            continue

        else:
            print("Unknown option.")
            time.sleep(0.6)

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted. See you next time! 🐾")
        raise SystemExit(130)

