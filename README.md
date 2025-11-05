[![CI / CD](https://github.com/swe-students-fall2025/3-python-package-team_pioneer/actions/workflows/ci.yml/badge.svg)](https://github.com/swe-students-fall2025/3-python-package-team_pioneer/actions/workflows/ci.yml)

# pyPet 🐾

**A tiny virtual pet that lives in your terminal**

pyPet is a delightful Python package that lets you create and care for a virtual pet right in your terminal. Feed your pet, play games with them, and watch their mood change based on how well you care for them. Perfect for developers who want a little companionship while coding!

📦 **[View on PyPI](https://pypi.org/project/pypet/)**

---

## 👥 Team Members

- [Connor Lee](https://github.com/Connorlee487)
- [Lanxi](https://github.com/player1notfound)
- [Alex](https://github.com/axie22)
- [Matthew](https://github.com/mzhou3299)
- [Andrew Liu](https://github.com/aklLiu5062)
---

## 🚀 Quick Start

### Installation

Install pyPet from PyPI:

```bash
pip install pypet
```

Or install from TestPyPI:

```bash
pip install -i https://test.pypi.org/simple/ pypet==0.1.2
```

### Basic Usage

```python
from pypet import create_pet, feed, play, status

# Create a new pet
pet = create_pet("Mochi", "otter", mood="happy", hunger=25, energy=85)

# Feed your pet
feed(pet, "fish", portion=20, treat=False)

# Play with your pet
play(pet, "fetch", energy=10, reward=True)

# Check on your pet
print(status(pet, color=True, verbose=True, ascii_art=True))
```

---

## 📚 Function Documentation

### `create_pet(name: str, species: str, mood: str = "neutral", hunger: int = 50, energy: int | None = None)`

Creates and returns a new virtual pet with the specified attributes.

**Parameters:**
- `name` (str): The pet's display name. Must be a non-empty string after trimming.
- `species` (str): The pet's species. Must be one of: `cat`, `dog`, `otter`, `capybara`, or `duck` (case-insensitive).
- `mood` (str, optional): The pet's initial mood. Must be one of: `happy`, `neutral`, `grumpy`, `sleepy`, `hungry`, or `sad`. Defaults to `"neutral"`.
- `hunger` (int, optional): Initial hunger level (0-100, where 0 = not hungry, 100 = very hungry). Defaults to `50`.
- `energy` (int, optional): Initial energy level (0-100, where 0 = exhausted, 100 = full energy). If not provided, defaults to `70`.

**Returns:**
- `Pet`: A dictionary representing the pet with the following keys:
  - `id`: Unique identifier (UUID)
  - `name`: Pet's name
  - `species`: Pet's species
  - `mood`: Current mood
  - `hunger`: Current hunger level (0-100)
  - `energy`: Current energy level (0-100)
  - `happiness`: Current happiness level (0-100, automatically calculated)
  - `created_at`: Timestamp of creation
  - `last_interaction_at`: Timestamp of last interaction
  - `ascii_key`: Key for ASCII art representation

**Raises:**
- `ValueError`: If name, species, or mood are invalid types or contain unsupported values.

**Example:**
```python
from pypet import create_pet

pet = create_pet("Fluffy", "cat", mood="happy", hunger=30, energy=90)
print(f"Created {pet['name']} the {pet['species']}")
```

---

### `feed(pet: dict, food: str, portion: int, treat: bool)`

Feeds your pet, reducing their hunger and potentially improving their mood. The function also simulates time passing (30 minutes) and updates the pet's mood based on their new hunger and happiness levels.

**Parameters:**
- `pet` (dict): A pet dictionary created by `create_pet()`.
- `food` (str): Type of food to give. Supported foods include: `kibble`, `fish`, `carrot`, `steak`, `cookie`. Each food has different hunger-reduction effects.
- `portion` (int): Portion size (0-100). Larger portions reduce more hunger.
- `treat` (bool): Whether the food is a special treat. If `True`, provides an additional hunger reduction and happiness boost.

**Returns:**
- `dict`: The updated pet dictionary with modified hunger, happiness, mood, and `last_interaction_at` timestamp.

**Raises:**
- `ValueError`: If pet is not a valid dictionary, food is not a string, or portion is not an integer between 0 and 100.

**Example:**
```python
from pypet import create_pet, feed

pet = create_pet("Buddy", "dog", hunger=80)
pet = feed(pet, "steak", portion=25, treat=True)
print(f"Hunger after feeding: {pet['hunger']}")
```

---

### `play(pet: dict, game: str, energy: int, reward: bool)`

Plays a game with your pet, which increases happiness but consumes energy. Different games may provide bonus happiness for certain species (e.g., dogs love "fetch", cats enjoy "laser" or "string" games).

**Parameters:**
- `pet` (dict): A pet dictionary created by `create_pet()`.
- `game` (str): Name of the game to play (e.g., `"fetch"`, `"tug"`, `"chase"`, `"hide-n-seek"`, `"laser"`, `"string"`, `"swim"`, `"relax"`).
- `energy` (int): Amount of energy to consume (must be a positive integer). If the pet doesn't have enough energy, they won't be able to play fully and may receive a small happiness penalty.
- `reward` (bool): Whether to give a reward after playing. If `True`, provides an additional happiness boost.

**Returns:**
- `dict`: The updated pet dictionary with modified energy, happiness, mood, and `last_interaction_at` timestamp.

**Raises:**
- `ValueError`: If energy is not a positive integer.

**Example:**
```python
from pypet import create_pet, play

pet = create_pet("Max", "dog", energy=50)
pet = play(pet, "fetch", energy=15, reward=True)
print(f"Energy after playing: {pet['energy']}, Happiness: {pet['happiness']}")
```

---

### `status(pet: dict, color: bool = False, verbose: bool = False, ascii_art: bool = False)`

Returns a formatted string displaying your pet's current status and mood.

**Parameters:**
- `pet` (dict): A pet dictionary created by `create_pet()`.
- `color` (bool, optional): If `True`, the mood will be displayed in color (green for happy, yellow for neutral, red for grumpy, blue for sleepy, magenta for hungry, gray for sad). Defaults to `False`.
- `verbose` (bool, optional): If `True`, displays detailed information including all pet attributes (id, version, hunger, energy, happiness, timestamps, etc.). Defaults to `False`.
- `ascii_art` (bool, optional): If `True`, displays ASCII art representing the pet's species. Defaults to `False`.

**Returns:**
- `str`: A formatted string showing the pet's status.

**Raises:**
- `ValueError`: If pet is not a dictionary.

**Example:**
```python
from pypet import create_pet, status

pet = create_pet("Mochi", "otter", mood="happy")
print(status(pet, color=True, verbose=True, ascii_art=True))
```

---

## 💡 Example Program

We've included an interactive demo program that showcases all the functions. After installing pyPet, you can run it with:

```bash
pypet-demo
```

Or run it directly:

```bash
python -m pypet.examples.demo
```

The demo program allows you to:
- Create a custom pet with your choice of name, species, and starting mood
- Feed your pet with different foods
- Play various games with your pet
- Check your pet's status with colorful, detailed output
- Rename your pet or change their mood

**View the full example code:** [`src/pypet/examples/demo.py`](src/pypet/examples/demo.py)

---

## 🛠️ For Contributors

Interested in contributing to pyPet? Here's how to set up your development environment:

### Prerequisites

- Python 3.8 or higher
- pipenv (for dependency management)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/swe-students-fall2025/3-python-package-team_pioneer.git
   cd 3-python-package-team_pioneer
   ```

2. **Set up a virtual environment and install dependencies:**
   ```bash
   pipenv install --dev
   ```

3. **Install the package in editable mode:**
   ```bash
   pipenv run pip install -e .
   ```

4. **Run the tests:**
   ```bash
   pipenv run pytest -q
   ```

   To run tests with more verbose output:
   ```bash
   pipenv run pytest -v
   ```

5. **Build the package:**
   ```bash
   pipenv run python -m build
   ```
   
   This creates distribution files in the `dist/` directory.

6. **Test the build locally:**
   ```bash
   pipenv run pip install dist/pypet-*.whl
   ```

### Running Tests

The test suite uses pytest and includes tests for all core functions. Run all tests with:

```bash
pipenv run pytest -q
```

Or run specific test files:

```bash
pipenv run pytest tests/test_create_pet.py
pipenv run pytest tests/test_feed_helper.py
pipenv run pytest tests/test_play.py
pipenv run pytest tests/test_status.py
```

### Project Structure

```
3-python-package-team_pioneer/
├── src/
│   └── pypet/
│       ├── __init__.py      # Package exports
│       ├── pet.py           # Core pet functions
│       ├── main.py          # Entry point
│       └── examples/
│           └── demo.py      # Interactive demo
├── tests/                   # Test suite
│   ├── test_create_pet.py
│   ├── test_feed_helper.py
│   ├── test_play.py
│   └── test_status.py
├── pyproject.toml           # Package configuration
├── Pipfile                  # Dependency management
└── README.md               # This file
```

### Uploading to PyPI (for maintainers)

To upload a new version to TestPyPI:

```bash
pipenv run twine upload --repository testpypi dist/*
```

To upload to production PyPI:

```bash
pipenv run twine upload dist/*
```

---

## 📄 License

This project is licensed under the GNU General Public License v3 (GPLv3). See the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **PyPI Package:** https://pypi.org/project/pypet/
- **GitHub Repository:** https://github.com/swe-students-fall2025/3-python-package-team_pioneer
- **Issue Tracker:** https://github.com/swe-students-fall2025/3-python-package-team_pioneer/issues

---

## 🙏 Acknowledgments

Thanks for using pyPet! We hope your virtual pet brings a smile to your terminal. 🐾
