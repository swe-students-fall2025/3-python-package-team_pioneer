from pypet import create_pet
from pypet import play

def test_play_basic_happy_path():
    """Test basic play functionality with reward"""
    pet = create_pet("Buddy", "dog", energy=80, hunger=20)
    initial_energy = pet["energy"]
    initial_happiness = pet["happiness"]
    
    updated_pet = play(pet, "fetch", energy=30, reward=True)
    
    # Check energy decreased by expected amount
    assert updated_pet["energy"] == initial_energy - 30
    assert updated_pet["energy"] == 50
    
    # Check happiness increased (base + reward + species bonus)
    # reward=True gives 10 base + 3 species bonus for dog+fetch = 13 total
    assert updated_pet["happiness"] > initial_happiness
    assert updated_pet["happiness"] == initial_happiness + 13
    
    # Check last_interaction_at was updated
    assert updated_pet["last_interaction_at"] > pet["last_interaction_at"]


def test_play_without_reward():
    """Test play without giving reward"""
    pet = create_pet("Whiskers", "cat", energy=60, hunger=30)
    initial_energy = pet["energy"]
    initial_happiness = pet["happiness"]
    
    updated_pet = play(pet, "laser pointer", energy=20, reward=False)
    
    # Check energy decreased
    assert updated_pet["energy"] == initial_energy - 20
    assert updated_pet["energy"] == 40
    
    # Check happiness increased (base + species bonus, no reward)
    assert updated_pet["happiness"] > initial_happiness
    assert updated_pet["happiness"] >= initial_happiness + 8  # 5 base + 3 species


def test_play_species_bonus_dog_fetch():
    """Test dog gets bonus for fetch game"""
    pet = create_pet("Max", "dog", energy=100, hunger=10)
    initial_happiness = pet["happiness"]
    
    updated_pet = play(pet, "Fetch the Ball", energy=10, reward=False)
    
    # Dog + fetch should give extra happiness
    assert updated_pet["happiness"] >= initial_happiness + 8  # 5 base + 3 species


def test_play_species_bonus_cat_laser():
    """Test cat gets bonus for laser/string games"""
    pet = create_pet("Shadow", "cat", energy=90, hunger=15)
    initial_happiness = pet["happiness"]
    
    updated_pet = play(pet, "laser tag", energy=15, reward=False)
    
    # Cat + laser should give extra happiness
    assert updated_pet["happiness"] >= initial_happiness + 8  # 5 base + 3 species


def test_play_species_bonus_otter_water():
    """Test otter gets bigger bonus for water games"""
    pet = create_pet("Splash", "otter", energy=85, hunger=20)
    initial_happiness = pet["happiness"]
    
    updated_pet = play(pet, "swim in pool", energy=25, reward=False)
    
    # Otter + water should give biggest bonus
    assert updated_pet["happiness"] >= initial_happiness + 9  # 5 base + 4 species


def test_play_insufficient_energy():
    """Test play when pet doesn't have enough energy"""
    pet = create_pet("Sleepy", "capybara", energy=10, hunger=40)
    initial_happiness = pet["happiness"]
    
    # Try to use more energy than available
    updated_pet = play(pet, "relax", energy=50, reward=True)
    
    # Energy should go to 0
    assert updated_pet["energy"] == 0
    
    # Happiness should decrease slightly
    assert updated_pet["happiness"] < initial_happiness
    assert updated_pet["happiness"] == initial_happiness - 2


def test_play_energy_clamping():
    """Test energy is clamped to 0-100"""
    pet = create_pet("Active", "duck", energy=5, hunger=25)
    
    updated_pet = play(pet, "water play", energy=10, reward=False)
    
    # Should not go below 0
    assert updated_pet["energy"] >= 0


def test_play_happiness_clamping():
    """Test happiness is clamped to 0-100"""
    pet = create_pet("Joy", "dog", energy=80, hunger=5)
    # Set very high happiness
    pet["happiness"] = 95
    
    updated_pet = play(pet, "fetch", energy=20, reward=True)
    
    # Should not exceed 100
    assert updated_pet["happiness"] <= 100


def test_play_mood_changes_to_happy():
    """Test mood changes to happy when happiness is high"""
    pet = create_pet("Cheerful", "cat", energy=90, hunger=10)
    pet["happiness"] = 75  # Start close to happy
    
    updated_pet = play(pet, "laser", energy=10, reward=True)
    
    # Should become happy
    assert updated_pet["mood"] == "happy"
    assert updated_pet["ascii_key"] == "cat:happy"


def test_play_mood_changes_to_sleepy():
    """Test mood changes to sleepy when energy is low"""
    pet = create_pet("Tired", "otter", energy=50, hunger=30)
    
    updated_pet = play(pet, "water games", energy=40, reward=False)
    
    # Should become sleepy
    assert updated_pet["mood"] == "sleepy"
    assert updated_pet["ascii_key"] == "otter:sleepy"


def test_play_mood_changes_to_sad():
    """Test mood changes to sad when happiness is low"""
    pet = create_pet("Down", "duck", energy=60, hunger=50)
    pet["happiness"] = 20  # Low happiness
    
    updated_pet = play(pet, "generic game", energy=10, reward=False)
    
    # Should become sad
    assert updated_pet["mood"] == "sad"
    assert updated_pet["ascii_key"] == "duck:sad"


def test_play_mood_changes_to_grumpy():
    """Test mood changes to grumpy when happiness is medium-low"""
    pet = create_pet("Grouchy", "capybara", energy=70, hunger=45)
    pet["happiness"] = 40  # Medium-low happiness
    
    updated_pet = play(pet, "relax", energy=30, reward=False)
    
    # Should become grumpy
    assert updated_pet["mood"] == "grumpy"
    assert updated_pet["ascii_key"] == "capybara:grumpy"


def test_play_invalid_energy():
    """Test play raises error for invalid energy values"""
    pet = create_pet("Test", "dog", energy=50, hunger=30)
    
    # Test negative energy
    try:
        play(pet, "fetch", energy=-10, reward=False)
        assert False, "expected ValueError for negative energy"
    except ValueError:
        pass
    
    # Test zero energy
    try:
        play(pet, "fetch", energy=0, reward=False)
        assert False, "expected ValueError for zero energy"
    except ValueError:
        pass
    
    # Test non-integer energy
    try:
        play(pet, "fetch", energy="ten", reward=False)
        assert False, "expected ValueError for non-integer energy"
    except ValueError:
        pass


def test_play_original_pet_not_modified():
    """Test that playing doesn't modify the original pet dict"""
    pet = create_pet("Original", "dog", energy=80, hunger=25)
    original_energy = pet["energy"]
    original_happiness = pet["happiness"]
    original_mood = pet["mood"]
    
    updated_pet = play(pet, "fetch", energy=30, reward=True)
    
    # Original pet should be unchanged
    assert pet["energy"] == original_energy
    assert pet["happiness"] == original_happiness
    assert pet["mood"] == original_mood
    
    # Updated pet should be different
    assert updated_pet["energy"] != pet["energy"]


def test_play_multiple_species_games():
    """Test all species with their preferred games"""
    species_games = [
        ("dog", "fetch", 10),
        ("cat", "string toy", 10),
        ("otter", "swimming", 10),
        ("duck", "water play", 10),
        ("capybara", "relaxing", 10),
    ]
    
    for species, game, expected_bonus in species_games:
        pet = create_pet(f"{species.capitalize()}Test", species, energy=70, hunger=30)
        initial_happiness = pet["happiness"]
        
        updated_pet = play(pet, game, energy=20, reward=False)
        
        # Each should get some bonus
        assert updated_pet["happiness"] > initial_happiness
        assert updated_pet["happiness"] >= initial_happiness + 5  # At least base boost

