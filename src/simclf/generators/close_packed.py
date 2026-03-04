import numpy as np

from simclf.typing import Point3DArray


def generate_close_packed_plane(
    width: int,
    height: int,
    lattice_parameter: float,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
) -> Point3DArray:
    root_3_over_2 = np.sqrt(3) / 2.0
    atom_positions = []
    for row in range(height):
        odd_atom_offset = 0.0 if row % 2 == 0 else lattice_parameter / 2.0
        for col in range(width):
            atom_positions.append([
                col * lattice_parameter + odd_atom_offset + x,
                row * lattice_parameter * root_3_over_2 + y,
                z,
            ])
    return np.array(atom_positions)


def generate_close_packed_plane_sequence(sequence: str, width: int, height: int, lattice_parameter: float):
    generated_planes = []

    root_3_over_4 = np.sqrt(3) / 4
    interplanar_spacing = np.sqrt(6) / 3 * lattice_parameter

    last_x = None
    for x in sequence:
        layer_number = len(generated_planes)
        z = layer_number * interplanar_spacing
        if x == last_x:
            raise ValueError(f"repetitive letter {repr(x)} in sequence")
        if x == 'A':
            generated_plane = generate_close_packed_plane(width, height, lattice_parameter, z=z)
        elif x == 'B': # XXX I don't actually know if this organization of points is consistent with literature
            generated_plane = generate_close_packed_plane(
                width, height, lattice_parameter,
                x=lattice_parameter / 2.0,
                y=root_3_over_4 * lattice_parameter,
                z=z,
            )
        elif x == 'C':
            generated_plane = generate_close_packed_plane(
                width, height, lattice_parameter,
                x=root_3_over_4 * lattice_parameter,
                y=lattice_parameter / 2.0,
                z=z,
            )
        else:
            raise ValueError(f"invalid letter {repr(x)} in sequence. expected A, B, or C")
        last_x = x
        generated_planes.append(generated_plane)
    
    return np.concat(generated_planes)

