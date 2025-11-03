from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import TypedDict, Dict
from uuid import uuid4

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
    """
    Feed the pet to reduce hunger and improve happiness slightly.
    Also updates mood and timestamps.
    """
    if not isinstance(pet, dict):
        raise ValueError("pet must be a dict created by create_pet()")
    if "hunger" not in pet or "happiness" not in pet:
        raise ValueError("invalid pet schema")

    if not isinstance(food, str):
        raise ValueError("food must be a string")
    if not isinstance(portion, int) or not (0 <= portion <= 100):
        raise ValueError("portion must be between 0 and 100")

    # Time since last interaction
    pet = time_passes(pet, seconds=1800)  

    FOOD_EFFECTS = {
        "kibble": 15,
        "fish": 25,
        "carrot": 10,
        "steak": 30,
        "cookie": 20,
    }

    base_effect = FOOD_EFFECTS.get(food.lower(), 10)
    hunger_delta = base_effect * (portion / 100)
    if treat:
        hunger_delta += 5

    lo, hi = BOUNDS["hunger"]
    pet["hunger"] = clamp(pet["hunger"] - hunger_delta, lo, hi)

    # Increase happiness based on fullness
    fullness_bonus = (100 - pet["hunger"]) / 15
    pet["happiness"] = clamp(
        pet["happiness"] + fullness_bonus + (5 if treat else 0),
        *BOUNDS["happiness"],
    )

    # Update last interaction
    pet["last_interaction_at"] = time()

    # Recalculate mood 
    pet = update_mood(pet)

    return pet

def play(pet: dict, game: str, energy: int, reward: bool):
    # code
    return {}

def status(pet: dict, color: bool, verbose: bool, ascii_art: bool):
    # code
    return {}

def update_mood(pet: Pet) -> Pet:
    """Recalculate mood based on hunger, energy, and happiness."""
    hunger, energy, happiness = pet["hunger"], pet["energy"], pet["happiness"]

    if hunger > 80:
        pet["mood"] = "hungry"
    elif energy < 20:
        pet["mood"] = "sleepy"
    elif happiness > 70:
        pet["mood"] = "happy"
    elif happiness < 30:
        pet["mood"] = "sad"
    else:
        pet["mood"] = "neutral"

    pet["ascii_key"] = f"{pet['species']}:{pet['mood']}"
    return pet

def time_passes(pet: Pet, seconds: int = 3600) -> Pet:
    """Simulate time passing: hunger increases and happiness decreases."""
    decay_factor = seconds / 3600 
    pet["hunger"] = clamp(pet["hunger"] + 5 * decay_factor, *BOUNDS["hunger"])
    pet["happiness"] = clamp(pet["happiness"] - 3 * decay_factor, *BOUNDS["happiness"])
    pet["last_interaction_at"] = time()
    return update_mood(pet)

def describe_pet(pet: Pet) -> str:
    """Return a readable summary of the pet's state."""
    return (
        f"{pet['name']} the {pet['species']} looks {pet['mood']}! "
        f"Hunger: {pet['hunger']:.1f}/100, Energy: {pet['energy']}/100, "
        f"Happiness: {pet['happiness']:.1f}/100."
    )