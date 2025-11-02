from pypet import create_pet, ALLOWED_SPECIES, ALLOWED_MOODS

def test_create_pet_happy_path():
    pet = create_pet("Mochi", "Otter", mood="Happy", hunger=10, energy=90)
    assert pet["name"] == "Mochi"
    assert pet["species"] == "otter"
    assert pet["mood"] == "happy"
    assert 0 <= pet["hunger"] <= 100
    assert 0 <= pet["energy"] <= 100
    assert 0 <= pet["happiness"] <= 100
    assert pet["ascii_key"] == "otter:happy"

def test_create_pet_validation_errors():
    for bad in ("", "   "):
        try:
            create_pet(bad, "cat")
            assert False, "expected ValueError for empty name"
        except ValueError:
            pass
    try:
        create_pet("Ok", "dragon")
        assert False, "expected ValueError for species"
    except ValueError:
        pass
    try:
        create_pet("Ok", "cat", mood="ecstatic")
        assert False, "expected ValueError for mood"
    except ValueError:
        pass

def test_defaults_and_normalization():
    pet = create_pet("  PIP  ", "DoG")
    assert pet["name"] == "PIP"
    assert pet["species"] == "dog"
    assert pet["mood"] == "neutral"
    assert pet["energy"] == 70  # default
