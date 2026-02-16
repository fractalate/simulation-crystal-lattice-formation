import numpy as np
import matplotlib.pyplot as plt

from simclf.generators.uniform_points_3d import generate_uniform_points_3d
from simclf.physics.atom import calculate_equilibrium_spacing
from simclf.physics.energy import calculate_potential_energy_of_basic_system


# XXX these magic numbers give like a 3 angstrom equilibrium spacing which is in the ballpark for some atomic configurations.
ATTRACTIVE_FACTOR = 3.6e-28
REPULSIVE_FACTOR = 1.0e-95
REPULSIVE_POWER = 8.0

NUMBER_OF_ATOMS = 100

equilibrium_spacing = calculate_equilibrium_spacing(
    attractive_factor=ATTRACTIVE_FACTOR,
    repulsive_factor=REPULSIVE_FACTOR,
    repulsive_power=REPULSIVE_POWER,
)
print(f"{equilibrium_spacing=}")

# XXX math problem: given a XxYxZ space which we'll fill with uniformly sized spheres having radius r,
# what is that chance that uniformly adding N spheres to the space will produce a configuration with overlapping spheres?
# Or maybe it's more interesting to ask: given that space, how many overlapping spheres can we expect when adding N spheres?
# With this, I can generate N+fudge atoms for the simulation where fudge is this number.
# Then I can remove any overlapping and hopefully we're left with about N atoms.

# But for now we just put some atoms in for now and remove those which overlap.

# We'll simulate in a cube, so we roughly cube root N atoms along each axis.
# Scale with some fudge so it's less likely atoms will touch.
simulation_dimension = 1.75 * NUMBER_OF_ATOMS**(1/3) * (2 * equilibrium_spacing)

atom_positions = generate_uniform_points_3d(
    np.array([-simulation_dimension / 2.0, -simulation_dimension / 2.0, -simulation_dimension / 2.0]),
    np.array([ simulation_dimension / 2.0,  simulation_dimension / 2.0,  simulation_dimension / 2.0]),
    NUMBER_OF_ATOMS,
)

# XXX fuck I hate myself for this...
class DoItAgain(Exception):
    pass

while True:
    try:
        for i in range(atom_positions.shape[0] - 1):
            for j in range(i + 1, atom_positions.shape[0]):
                distance = np.linalg.norm(atom_positions[i] - atom_positions[j])
                if distance < equilibrium_spacing:
                    atom_positions[j] = atom_positions[atom_positions.shape[0] - 1]
                    atom_positions = atom_positions[:-1,]
                    raise DoItAgain()
        break
    except DoItAgain:
        pass

print(f"number_of_atoms={atom_positions.shape[0]}")

potential_energy_of_system = calculate_potential_energy_of_basic_system(
    atom_positions=atom_positions,
    attractive_factor=ATTRACTIVE_FACTOR,
    repulsive_factor=REPULSIVE_FACTOR,
    repulsive_power=REPULSIVE_POWER,
)

print(f"{potential_energy_of_system=}")

step_size = equilibrium_spacing / 20.0
gradient = np.zeros_like(atom_positions)
mask = np.zeros_like(atom_positions)

# TODO Is there something wrong with this gradient descent?
# It either converges so slowly it's useless or it's just wrong.
# I think maybe I could try to make sure each step of the simulation moves some minimum amount so that it forces faster convergence maybe?
for k in range(20):
    for i in range(atom_positions.shape[0]):
        for j in range(atom_positions.shape[1]):
            mask[i][j] = step_size
            temp = calculate_potential_energy_of_basic_system(
                atom_positions=atom_positions + mask,
                attractive_factor=ATTRACTIVE_FACTOR,
                repulsive_factor=REPULSIVE_FACTOR,
                repulsive_power=REPULSIVE_POWER,
            )
            gradient[i][j] = (temp - potential_energy_of_system) / step_size
            mask[i][j] = 0

    atom_positions = atom_positions - gradient * step_size

    potential_energy_of_system_next = calculate_potential_energy_of_basic_system(
        atom_positions=atom_positions,
        attractive_factor=ATTRACTIVE_FACTOR,
        repulsive_factor=REPULSIVE_FACTOR,
        repulsive_power=REPULSIVE_POWER,
    )

    print(f"{potential_energy_of_system_next=}")
    print(f"delta={potential_energy_of_system_next - potential_energy_of_system}")

    potential_energy_of_system = potential_energy_of_system_next

#print(atom_positions)

xs = atom_positions[:, 0]
ys = atom_positions[:, 1]
zs = atom_positions[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(xs, ys, zs)  # type: ignore

plt.show()
