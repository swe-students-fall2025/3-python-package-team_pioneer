from pypet import create_pet, status
import time

def main():
    pet = create_pet("Mochi", "capybara", mood="happy", hunger=20, energy=80)
    print(status(pet, color=True, verbose=True, ascii_art=True))  
    time.sleep(1)

    pet["hunger"]+= 15
    pet["energy"]-= 10
    pet["happiness"]-= 5
    pet["last_interaction_at"]=time.time()  

    print(status(pet, color=True, verbose=True, ascii_art=False)) 

if __name__=="__main__":
    main()
