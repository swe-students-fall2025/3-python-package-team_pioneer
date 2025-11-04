"""
pyPet

APIs:
- create_pet()
- feed(fill in args when done)
- play(fill in args when done)
- status(fill in args when done)
"""

from .pet import (
    create_pet,
    feed,
    play,
    status,
    ALLOWED_SPECIES,
    ALLOWED_MOODS,
    BOUNDS,
    Pet,
    update_mood,
    time_passes,
    describe_pet,
)

__all__ = [
    "create_pet",
    "feed",
    "play",
    "status",
    "ALLOWED_SPECIES",
    "ALLOWED_MOODS",
    "BOUNDS",
    "Pet",
    "update_mood",
    "time_passes",
    "describe_pet",
]

__version__ = "0.1.0"
