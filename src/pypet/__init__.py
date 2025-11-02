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
    ALLOWED_SPECIES,
    ALLOWED_MOODS,
    BOUNDS,
    Pet,
)

__all__ = [
    "create_pet",
    "ALLOWED_SPECIES",
    "ALLOWED_MOODS",
    "BOUNDS",
    "Pet",
]

__version__ = "0.1.0"
