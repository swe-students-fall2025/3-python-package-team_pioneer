from pypet import create_pet, status
import time

def main():
    pet = create_pet("Mochi", "capybara", mood="happy", hunger=20, energy=80)
    print(status(pet, color=True, verbose=True, ascii_art=True))  
 

if __name__=="__main__":
    main()
