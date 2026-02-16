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

simulation_dimension = 1.0 * NUMBER_OF_ATOMS**(1/3) * (2 * equilibrium_spacing) * .2

# force the atoms into a planar arrangement
atom_positions = generate_uniform_points_3d(
    np.array([-simulation_dimension / 2.0, -simulation_dimension / 2.0, 0]),
    np.array([ simulation_dimension / 2.0,  simulation_dimension / 2.0, 0]),
    NUMBER_OF_ATOMS,
)

# XXX fuck I hate myself for this...
class DoItAgain(Exception):
    pass

# Detect atoms which overlap too much. Atoms are allowed to overlap considerably, but not
# too much. This allows for some portion of the points to spread out, rather than contract,
# which numerically helps reach a solution faster as the gradient when atoms are overlapping
# is much steeper than when the yare spaced apart.
while True:
    try:
        for i in range(atom_positions.shape[0] - 1):
            for j in range(i + 1, atom_positions.shape[0]):
                distance = np.linalg.norm(atom_positions[i] - atom_positions[j])
                if distance < equilibrium_spacing / 5.0:
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

for k in range(40):
    for i in range(atom_positions.shape[0]):
        for j in range(atom_positions.shape[1]):
            mask[i][j] = step_size
            temp = calculate_potential_energy_of_basic_system(
                atom_positions=atom_positions + mask,
                attractive_factor=ATTRACTIVE_FACTOR,
                repulsive_factor=REPULSIVE_FACTOR,
                repulsive_power=REPULSIVE_POWER,
            )
            gradient[i][j] = temp - potential_energy_of_system
            mask[i][j] = 0

    # Don't accept movement along the Z axis.
    gradient[:,2] = 0

    scale_factor = np.linalg.norm(gradient.flatten())
    if scale_factor > 0.0:
        perturbation = - gradient / scale_factor * equilibrium_spacing / (k + 5)

        attempt = 0
        while True:
            # March ahead while there are gains.
            attempt += 1
            atom_positions_next = atom_positions + perturbation
            potential_energy_of_system_next = calculate_potential_energy_of_basic_system(
                atom_positions=atom_positions_next,
                attractive_factor=ATTRACTIVE_FACTOR,
                repulsive_factor=REPULSIVE_FACTOR,
                repulsive_power=REPULSIVE_POWER,
            )

            if attempt <= 1 or potential_energy_of_system_next < potential_energy_of_system:
                print(f"{potential_energy_of_system_next=}")
                print(f"delta={potential_energy_of_system_next - potential_energy_of_system}")
                atom_positions = atom_positions_next
                potential_energy_of_system = potential_energy_of_system_next
            else:
                break

xs = atom_positions[:, 0]
ys = atom_positions[:, 1]
zs = atom_positions[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d', proj_type='ortho')
ax.scatter(xs, ys, zs)  # type: ignore

plt.show()
