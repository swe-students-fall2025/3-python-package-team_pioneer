from pypet.pet import create_pet, feed, update_mood, time_passes, describe_pet


def test_feed_reduces_hunger():

    pet = create_pet("Mochi", "otter", "neutral", hunger=80)
    updated_pet = feed(pet, "fish", 30, treat=False)

    assert 0 <= updated_pet["hunger"] < 80, "Hunger did not decrease as expected"
    assert isinstance(updated_pet["hunger"], (int, float))


def test_feed_increases_happiness():

    pet = create_pet("Mochi", "otter", "neutral", hunger=70)
    before = pet["happiness"]
    updated_pet = feed(pet, "fish", 40, treat=False)

    assert updated_pet["happiness"] >= before, "Happiness should not decrease after feeding"
    assert updated_pet["happiness"] <= 100, "Happiness should not exceed 100"


def test_feed_treat_makes_pet_happy():

    pet = create_pet("Mochi", "otter", "neutral", hunger=60)
    before_happiness = pet["happiness"]

    updated_pet = feed(pet, "fish", 20, treat=True)

    assert updated_pet["happiness"] > before_happiness, "Treat should boost happiness"

    assert updated_pet["mood"] in {"happy", "content", "neutral"}, (
        f"Mood after treat should be positive, got {updated_pet['mood']}"
    )



def test_update_mood_adjusts_based_on_hunger_energy_happiness():

    pet = {
        "name": "Mochi",
        "species": "otter",
        "mood": "neutral",
        "hunger": 90,
        "energy": 50,
        "happiness": 50,
    }
    pet = update_mood(pet)

    assert pet["mood"] in {"hungry", "sleepy", "happy", "sad", "neutral"}, "Invalid mood after update"
    assert "ascii_key" in pet, "ascii_key not updated"


def test_time_passes_increases_hunger_and_updates_mood():

    pet = create_pet("Mochi", "otter", "neutral", hunger=30)
    before_hunger = pet["hunger"]
    updated_pet = time_passes(pet, seconds=7200)  # 2 hours later

    assert updated_pet["hunger"] > before_hunger, "Hunger should increase over time"
    assert updated_pet["mood"] in {"hungry", "neutral", "sleepy", "sad", "happy"}


def test_describe_pet_returns_readable_summary():

    pet = create_pet("Mochi", "otter", "neutral", hunger=40)
    desc = describe_pet(pet)

    assert isinstance(desc, str), "Description should be a string"
    assert "Mochi" in desc and "otter" in desc, "Missing pet info in description"
    assert any(word in desc for word in ["happy", "neutral", "hungry", "sleepy", "sad"]), "Mood not in description"


def test_feed_does_not_exceed_bounds():

    pet = create_pet("Mochi", "otter", "neutral", hunger=5)
    updated_pet = feed(pet, "steak", 80, treat=True)

    assert 0 <= updated_pet["hunger"] <= 100, "Hunger out of bounds"
    assert 0 <= updated_pet["happiness"] <= 100, "Happiness out of bounds"


def test_multiple_interactions_keep_state_consistent():

    pet = create_pet("Mochi", "otter", "neutral", hunger=70)
    pet = feed(pet, "fish", 30, treat=False)
    pet = time_passes(pet, seconds=3600)
    pet = feed(pet, "cookie", 50, treat=True)

    assert 0 <= pet["hunger"] <= 100
    assert 0 <= pet["energy"] <= 100
    assert 0 <= pet["happiness"] <= 100
    assert isinstance(pet["mood"], str)
