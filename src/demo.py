from pypet import create_pet
from pypet.pet import play

pet = create_pet("Mochi", "otter")
play(pet, "fetch", 10, True)