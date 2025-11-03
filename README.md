# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

Group Members

- [Connor Lee](https://github.com/Connorlee487)
- [Lanxi](https://github.com/player1notfound)
- [Alex](https://github.com/axie22)
- 4th ?

## `pyPet`

**Theme:** A tiny virtual pet in your terminal.

**Concept:**
`pyPet` creates a small, stateful pet that lives in your terminal. You can feed it, play with it, and check on its mood.

**Core Functions**

- `create_pet(name: str, species: str, mood: str, hunger: int)`
  - Initializes a new pet with starting attributes.
- `feed(pet: dict, food: str, portion: int, treat: bool)`
  - Reduces hunger, may improve mood based on treat type.
- `play(pet: dict, game: str, energy: int, reward: bool)`
  - Boosts happiness and decreases energy over time.
- `status(pet: dict, color: bool, verbose: bool, ascii_art: bool)`
  - Prints the current pet’s stats and ASCII representation.

### Instructions for Running & Testing

``` bash
pipenv install --dev
pipenv run pip install -e .
pipenv run pytest -q
```

Build

``` bash
pipenv run python -m build
pipenv run twine upload --repository testpypi dist/*
```
