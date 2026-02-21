# Simulation of Crystal Lattice Formation

![Example Animation of Atoms Arranging into a Regular Structure](./assets/example.gif)


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

<!--

## TODO

* Make some tools for analyzing the resulting crystal structure to see how "regular" it is I guess.
* Make some tools for loading Writer outputs.
* Rebuild the basic simulation as a class. Make it so the simulation can be continued.

-->
