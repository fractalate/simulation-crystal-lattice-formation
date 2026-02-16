import numpy as np
import numpy.typing as npt

from simclf.typing import Point3DArray, check_point_3d_array


def calculate_potential_energy_of_basic_system(
    atom_positions: Point3DArray,
    attractive_factor: float,
    repulsive_factor: float,
    repulsive_power: float,
) -> np.float64:
    """
    WARNING: This function will blow up if your atoms are too close. Do something to prevent such configurations before calling.

    A is attractive_factor
    r is distance between atoms
    E_A is attractive potential

    E_A = -A / r

    B is repulsive_factor
    n is repulsive_power
    r is distance between atoms
    E_B is repulsive potential

    E_B = B / r^n
    """
    check_point_3d_array(atom_positions)
    number_of_atoms = atom_positions.shape[0]

    total = np.float64(0.0)

    for i in range(number_of_atoms - 1):
        for j in range(i + 1, number_of_atoms):
            distance = np.linalg.norm(atom_positions[i] - atom_positions[j])

            attractive_potential = -attractive_factor / distance
            repulsive_potential = repulsive_factor / distance**repulsive_power

            total += attractive_potential + repulsive_potential

    return total
