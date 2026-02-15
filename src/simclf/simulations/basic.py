import numpy as np

from simclf.generators.uniform_points_3d import generate_uniform_points_3d
from simclf.physics.atom import calculate_equilibrium_spacing


ATTRACTIVE_FACTOR = 2
REPULSIVE_FACTOR = 4
REPULSIVE_POWER = 8

NUMBER_OF_ATOMS = 100

atom_positions = generate_uniform_points_3d(
    np.array([0.0, 0.0, 0.0]),
    np.array([1.0, 1.0, 1.0]),
    NUMBER_OF_ATOMS,
)

equilibrium_spacing = calculate_equilibrium_spacing(
    attractive_factor=ATTRACTIVE_FACTOR,
    repulsive_factor=REPULSIVE_FACTOR,
    repulsive_power=REPULSIVE_POWER,
)

# XXX math problem: given a XxYxZ space which we'll fill with uniformly sized spheres having radius r, what is that chance that uniformly adding N spheres to the space will produce a configuration with overlapping spheres?
# or maybe it's more interesting to ask: given that space, how many overlapping spheres can we expect when adding N spheres?
# with this, I can generate N+fudge atoms for the simulation where fudge is this number. then I can remove any overlapping and hopefully we're left with about N atoms
