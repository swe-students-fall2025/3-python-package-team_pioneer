from pypet import create_pet,status,play
import time

def main():
    pet = create_pet("Mochi", "capybara", mood="happy", hunger=20, energy=80)
    print(status(pet, color=True, verbose=True, ascii_art=True))  
    play(pet, "fetch", 10, True)
    time.sleep(3)
    pet = create_pet("Mochi", "capybara", mood="happy", hunger=20, energy=80)
    print(status(pet, color=True, verbose=True, ascii_art=True))  

if __name__=="__main__":
    main()
