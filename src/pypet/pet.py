from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from time import time
from typing import TypedDict, Dict
from uuid import uuid4

ANIMAL_ART = {
    "cat": r"""
 /\_/\ 
( o.o )
 > ^ <
""",
    "dog": r"""
  / \__
 (    @\___
 /         O
/   (_____/
/_____/   U
""",
    "otter": r"""
 (\_._/)
 ( o o )
  > ^ <
""",
    "capybara": r"""
  ( \_______/ )
  ( o   o )
   (  -  )
    """,
    "duck": r"""
<(o )___
 ( ._> /
  `---'
"""
}




ALLOWED_SPECIES = {"cat", "dog", "otter", "capybara", "duck"}
ALLOWED_MOODS = {"happy", "neutral", "grumpy", "sleepy", "hungry", "sad"}
BOUNDS: Dict[str, tuple[int, int]] = {
    "hunger": (0, 100),     # 0 = not hungry, 100 = hungry
    "energy": (0, 100),     # 0 = empty, 100 = full 
    "happiness": (0, 100),  # 0 = sad, 100 = happy
}


class Pet(TypedDict, total=False):
    """
    Schema for a pet instance.

    Keys:
        id: unique identifier 
        version: schema version
        name: non-empty name
        species: lowercase species key in ALLOWED_SPECIES
        mood: lowercase mood key in ALLOWED_MOODS
        hunger: 0-100 (int)
        energy: 0-100 (int)
        happiness: 0-100 (int)
        created_at: timestamp 
        last_interaction_at: timestamp
        ascii_key: f"{species}:{mood}"
    """
    id: str
    version: int
    name: str
    species: str
    mood: str
    hunger: int
    energy: int
    happiness: int
    created_at: float
    last_interaction_at: float
    ascii_key: str

def clamp(x: int, lo: int, hi: int) -> int:
    """Clamp integer x to [lo, hi]"""
    try:
        xi = int(x)
    except (TypeError, ValueError):
        raise ValueError(f"value {x!r} must be an integer")
    return max(lo, min(hi, xi))


def baseline_happiness(hunger: int) -> int:
    """
    Compute a baseline happiness from hunger
    happiness = clamp(80 - hunger // 2, 0, 100)
    """
    lo, hi = BOUNDS["happiness"]
    return clamp(80 - clamp(hunger, *BOUNDS["hunger"]) // 2, lo, hi)

def create_pet(
    name: str,
    species: str,
    mood: str = "neutral",
    hunger: int = 50,
    energy: int | None = None,
) -> Pet:
    """
    Create and return a new pet dict

    Args:
        name: Pet's display name. Must be a non-empty string after trimming.
        species: One of ALLOWED_SPECIES (normalized to lowercase).
        mood: One of ALLOWED_MOODS (normalized to lowercase). Default "neutral".
        hunger: Integer 0-100 (0=not hungry, 100=hungry)
        energy: Optional integer 0-100 (default 70 if omitted)

    Returns:
        Pet: a new pet object adhering to the schema defined by `Pet`.

    Raises:
        ValueError: on invalid name/species/mood types or unsupported values.
    """

    if not isinstance(name, str):
        raise ValueError("name must be a string")
    name = name.strip()
    if not name:
        raise ValueError("name must be non-empty")

    if not isinstance(species, str):
        raise ValueError("species must be a string")
    species = species.strip().lower()
    if species not in ALLOWED_SPECIES:
        raise ValueError(f"unsupported species: {species!r}. Allowed: {sorted(ALLOWED_SPECIES)}")

    if not isinstance(mood, str):
        raise ValueError("mood must be a string")
    mood = mood.strip().lower()
    if mood not in ALLOWED_MOODS:
        raise ValueError(f"unsupported mood: {mood!r}. Allowed: {sorted(ALLOWED_MOODS)}")


    hunger = clamp(hunger, *BOUNDS["hunger"])
    energy = clamp(energy if energy is not None else 70, *BOUNDS["energy"])
    happiness = baseline_happiness(hunger)

    pet: Pet = {
        "id": str(uuid4()),
        "version": 1,
        "name": name,
        "species": species,
        "mood": mood,
        "hunger": hunger,
        "energy": energy,
        "happiness": happiness,
        "created_at": time(),
        "last_interaction_at": time(),
        "ascii_key": f"{species}:{mood}"
    }
    return pet


def feed(pet: dict, food: str, portion: int, treat: bool):
    # code
    return {}

def play(pet: dict, game: str, energy: int, reward: bool):
    # code
    return {}

def status(pet: dict, color: bool = False, verbose: bool = False, ascii_art: bool = False):
    if not isinstance(pet, dict):
        raise ValueError("pet must be a dictionary")

    pet["last_interaction_at"] = time()

    name = pet.get("name", "Unknown")
    species = pet.get("species", "unknown")
    mood = pet.get("mood", "neutral")

    if color:
        colors = {
            "happy": "\033[92m",   # green
            "neutral": "\033[93m", # yellow
            "grumpy": "\033[91m",  # red
            "sleepy": "\033[94m",  # blue
            "hungry": "\033[95m",  # magenta
            "sad": "\033[90m",     # gray
        }
        end = "\033[0m"
        mood_text = f"{colors.get(mood, '')}{mood}{end}"
    else:
        mood_text = mood
    
    summary = "\n" + "-" * 40 + "\n"
    summary += f"{name} the {species} looks {mood_text}."

    if verbose:
        summary += "\n" + "-" * 40 + "\n"
        for key, value in pet.items():
            if key in {"name", "species", "mood"}:
                continue
            if key in {"created_at", "last_interaction_at"}:
                value = datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
                label = "Created at:" if key == "created_at" else "Last interaction:"
                summary += f"{label} {value}\n"
            else:
                summary += f"{key}: {value}\n"
        summary = summary.strip()
        summary += "\n" + "-" * 40

    if ascii_art:
        art = ANIMAL_ART.get(species, "(•ᴗ•)")
        summary += "\n" + art.strip()+"\n" 

    return summary