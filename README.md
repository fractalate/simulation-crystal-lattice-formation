# Simulation of Crystal Lattice Formation

## Setup

```bash
# Set up a virtual env for dependencies.
python3 -m venv --prompt simclf .venv

# Activate the virtual env.
source .venv/bin/activate

# Install dependencies.
pip install --editable .
```

## Running Basic Simulation

```bash
python3 -m simclf.simulations.basic
```

This will output files in a directory roughly named like `out/{timestamp}_basic_{version}`.
