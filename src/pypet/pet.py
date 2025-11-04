from __future__ import annotations
from datetime import datetime
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
    """
    Play a game with the pet, updating its energy and happiness.

    Args:
        pet: Pet dict to play with
        game: Name of the game being played
        energy: Amount of energy to deduct (must be positive)
        reward: Whether to give a treat/happy boost

    Returns:
        dict: Updated pet dict with modified energy, happiness, and last_interaction_at

    Raises:
        ValueError: if energy is not a positive integer
    """
    if not isinstance(energy, int) or energy <= 0:
        raise ValueError("energy must be a positive integer")
    
    # Get current stats
    current_energy = pet.get("energy", 0)
    current_happiness = pet.get("happiness", 0)
    species = pet.get("species", "").lower()
    
    # Check if pet has enough energy to play
    if current_energy < energy:
        # Not enough energy - small happiness penalty
        new_energy = 0
        new_happiness = clamp(current_happiness - 2, *BOUNDS["happiness"])
    else:
        # Deduct energy
        new_energy = clamp(current_energy - energy, *BOUNDS["energy"])
        
        # Base happiness boost
        happiness_boost = 10 if reward else 5
        
        # Species-specific multipliers for certain games
        species_boost = 0
        if species == "dog" and "fetch" in game.lower():
            species_boost = 3
        elif species == "cat" and ("laser" in game.lower() or "string" in game.lower()):
            species_boost = 3
        elif species == "duck" and ("water" in game.lower() or "swim" in game.lower()):
            species_boost = 3
        elif species == "otter" and ("water" in game.lower() or "swim" in game.lower()):
            species_boost = 4
        elif species == "capybara" and "relax" in game.lower():
            species_boost = 2
        
        new_happiness = clamp(current_happiness + happiness_boost + species_boost, *BOUNDS["happiness"])
    
    # Update mood based on new stats
    new_mood = pet.get("mood", "neutral")
    if new_energy < 20:
        new_mood = "sleepy"
    elif new_happiness >= 80:
        new_mood = "happy"
    elif new_happiness < 30:
        new_mood = "sad"
    elif new_happiness < 50:
        new_mood = "grumpy"
    else:
        new_mood = "neutral"

    pet["energy"] = new_energy
    pet["happiness"] = new_happiness
    pet["mood"] = new_mood
    pet['ascii_key'] = f"{species}:{new_mood}"
    pet["last_interaction_at"] = time()
    
    return pet

def status(pet: dict, color: bool = False, verbose: bool = False, ascii_art: bool = False):
    if not isinstance(pet, dict):
        raise ValueError("pet must be a dictionary")

    pet["last_interaction_at"] = time()

    name = pet.get("name", "Unknown")
    species = pet.get("species", "unknown")
    mood = pet.get("mood", "neutral")

    if color:
        colors = {
            "happy": "\033[92m",  # green
            "neutral": "\033[93m", # yellow
            "grumpy": "\033[91m", # red
            "sleepy": "\033[94m", # blue
            "hungry": "\033[95m", # magenta
            "sad": "\033[90m",  # gray
        }
        end = "\033[0m"
        mood_text = f"{colors.get(mood, '')}{mood}{end}"
    else:
        mood_text = mood
    
    summary = "\n" + "-" * 40 + "\n"
    summary += f"{name} the {species} looks {mood_text}.\n"
    summary += "-" * 40

    if verbose:
        summary += "\n"
        for key, value in pet.items():
            if key in {"name", "species", "mood"}:
                continue
        # Format timestamps
            if key in {"created_at", "last_interaction_at"}:
                value = datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
                label = "Created at:" if key == "created_at" else "Last interaction:"
            else:
            # Capitalize first letter for keys
                label = key.capitalize() + ":"
            summary += f"{label} {value}\n"
        summary = summary.strip()
        summary += "\n" + "-" * 40


    if ascii_art:
        art=ANIMAL_ART.get(species, "(•ᴗ•)")
        summary+= "\n"+art.strip()+"\n\n" 

    return summary

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
