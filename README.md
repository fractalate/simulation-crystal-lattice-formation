# Simulation of Crystal Lattice Formation

## Thoughts

*February 12, 2026*

I want to make this simulation and in a conversation with ChatGPT about my troubles with naive simulations using a more classical approach, it recommended me to use an approach which attempts to minimize the potential in the group of atoms. I think I can give this an honest shot, I just need to take inventory of some things I understand:

* For some parameters $A$, $B$, and $n$ related to the ionic system and $r$ being the distance from the atom, we have
* Attractive energy $E_A = - \frac{A}{r}$.
* Repulsive energy $E_R = \frac{B}{r^n}$.
* Values for $n$ are around $8$.
* Source: Callister and Rethwish - Material Science and Engineering: An Introduction - 8e - Chapter 2.6

My initial thoughts on an approach is to randomly place some atoms in space, then consider the gradient of the potential field at each atom to determine which direction it needs to move to lower its potential.

## Setup

```
# Set up a virtual env for dependencies.
python3 -m venv --prompt simclf .venv

# Activate the virtual env.
source .venv/bin/activate

# Install dependencies.
pip install --editable .
```
