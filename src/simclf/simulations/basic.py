import os
import time

import numpy as np
import matplotlib.pyplot as plt

from simclf.generators.uniform_points_3d import generate_uniform_points_3d
from simclf.physics.atom import calculate_equilibrium_spacing
from simclf.physics.energy import calculate_potential_energy_of_basic_system
from simclf.writer import Writer


# XXX these magic numbers give like a 3 angstrom equilibrium spacing which is in the ballpark for some atomic configurations.
ATTRACTIVE_FACTOR = 3.6e-28
REPULSIVE_FACTOR = 1.0e-95
REPULSIVE_POWER = 8.0

NUMBER_OF_ATOMS = 75

equilibrium_spacing = calculate_equilibrium_spacing(
    attractive_factor=ATTRACTIVE_FACTOR,
    repulsive_factor=REPULSIVE_FACTOR,
    repulsive_power=REPULSIVE_POWER,
)
print(f"{equilibrium_spacing=}")

writer = Writer("basic", "1.0.0")

writer.write_object_to_json("config.json", {
    "number_of_atoms": NUMBER_OF_ATOMS,
    "attractive_factor": ATTRACTIVE_FACTOR,
    "repulsive_factor": REPULSIVE_FACTOR, 
    "repulsive_power": REPULSIVE_POWER,
})

# XXX math problem: given a XxYxZ space which we'll fill with uniformly sized spheres having radius r,
# what is that chance that uniformly adding N spheres to the space will produce a configuration with overlapping spheres?
# Or maybe it's more interesting to ask: given that space, how many overlapping spheres can we expect when adding N spheres?
# With this, I can generate N+fudge atoms for the simulation where fudge is this number.
# Then I can remove any overlapping and hopefully we're left with about N atoms.

# But for now we just put some atoms in for now and remove those which overlap.

# We'll simulate in a cube, so we roughly cube root N atoms along each axis.
# Scale with some fudge so it's less likely atoms will touch.
simulation_dimension = 1.0 * NUMBER_OF_ATOMS**(1/3) * (2 * equilibrium_spacing) * .2

atom_positions = generate_uniform_points_3d(
    np.array([-simulation_dimension / 2.0, -simulation_dimension / 2.0, -simulation_dimension / 2.0]),
    np.array([ simulation_dimension / 2.0,  simulation_dimension / 2.0,  simulation_dimension / 2.0]),
    NUMBER_OF_ATOMS,
)

writer.write_points_to_csv("initial.csv", atom_positions)

# XXX fuck I hate myself for this...
class DoItAgain(Exception):
    pass

while True:
    try:
        for i in range(atom_positions.shape[0] - 1):
            for j in range(i + 1, atom_positions.shape[0]):
                distance = np.linalg.norm(atom_positions[i] - atom_positions[j])
                if distance < equilibrium_spacing / 5.0: # XXX kindof let the overlap, but you don't want too much since repulsive force is so powerful
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

cycle = 0
def write_step_data_and_advance(atom_positions, potential_energy_of_system):
    global cycle
    writer.write_points_to_csv(f"step_{cycle:05d}.csv", atom_positions)
    writer.write_object_to_json(f"step_{cycle:05d}.metadata.json", {
        "potential_energy_of_system": potential_energy_of_system,
    })
    cycle += 1

write_step_data_and_advance(atom_positions, potential_energy_of_system)

for k in range(40):
    for i in range(atom_positions.shape[0]):
        for j in range(atom_positions.shape[1]):
            mask[i][j] = step_size
            temp0 = calculate_potential_energy_of_basic_system(
                atom_positions=atom_positions - mask / 2.0,
                attractive_factor=ATTRACTIVE_FACTOR,
                repulsive_factor=REPULSIVE_FACTOR,
                repulsive_power=REPULSIVE_POWER,
            )
            temp1 = calculate_potential_energy_of_basic_system(
                atom_positions=atom_positions + mask / 2.0,
                attractive_factor=ATTRACTIVE_FACTOR,
                repulsive_factor=REPULSIVE_FACTOR,
                repulsive_power=REPULSIVE_POWER,
            )
            gradient[i][j] = temp1 - temp0
            mask[i][j] = 0

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

                write_step_data_and_advance(atom_positions, potential_energy_of_system)
            else:
                break

#print(atom_positions)

xs = atom_positions[:, 0]
ys = atom_positions[:, 1]
zs = atom_positions[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d', proj_type='ortho')
ax.scatter(xs, ys, zs)  # type: ignore

plt.show()
