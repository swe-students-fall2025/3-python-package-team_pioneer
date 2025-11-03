from pypet import create_pet,status,play
import time


pet = create_pet("Mochi", "otter")
play(pet, "fetch", 10, True)
print(status(pet, color=True, verbose=False, ascii_art=True))

pet = create_pet("Mochi", "otter")
play(pet, "fetch", 10, True)
print(status(pet, color=True, verbose=False, ascii_art=True)) 





