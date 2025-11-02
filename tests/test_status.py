from pypet import create_pet, status

def test_status_basic_output():
    pet = create_pet("Mochi", "otter", mood="happy")
    s = status(pet)
    assert "Mochi" in s
    assert "otter" in s
    assert "happy" in s

def test_status_verbose():
    pet = create_pet("Pip", "cat")
    s = status(pet, verbose=True)
    assert "Hunger" in s
    assert "Energy" in s
    assert "Happiness" in s

def test_status_ascii_art():
    animals = ["cat", "dog", "otter", "capybara", "duck"]
    for species in animals:
        pet = create_pet("Test", species)
        s = status(pet, ascii_art=True)

        assert "(" in s or "\\" in s or "_" in s

def test_status_color():
    pet = create_pet("Mochi", "otter", mood="happy")
    s = status(pet, color=True)
    assert "\033[" in s
