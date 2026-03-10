import numpy as np
from matplotlib import pyplot as plt

from functools import lru_cache
from simclf.typing import Point3D, Point3DArray, Scalers

TWO_PI = np.pi * 2.0


def calculate_distance_to_reference_plane(position: Point3D, plane_normal: Point3D) -> float:
    return np.abs(np.dot(position, plane_normal)) / np.linalg.norm(plane_normal)


def calculate_distances_to_reference_plane(positions: Point3DArray, plane_normal: Point3D) -> Scalers:
    return np.abs(positions @ plane_normal) / np.linalg.norm(plane_normal)


def measure_single_atom(
    wavelength: float,
    phase: float,
    diffraction_angle: float,
    atom_position: Point3D,
):
    detector_normal = np.array([np.cos(diffraction_angle), 0.0, np.sin(diffraction_angle)])
    emitter_normal = np.array([np.cos(diffraction_angle), 0.0, -np.sin(diffraction_angle)])
    distance_emitter_to_atom = calculate_distance_to_reference_plane(atom_position, emitter_normal)
    measurement_at_atom = np.cos(distance_emitter_to_atom / wavelength * 2 * np.pi + phase)
    distance_atom_to_detector = calculate_distance_to_reference_plane(atom_position, detector_normal)
    return measurement_at_atom * np.cos((distance_emitter_to_atom + distance_atom_to_detector) / wavelength * 2 * np.pi + phase)


def measure_multiple_atoms(
    wavelength: float,
    phase: float,
    diffraction_angle: float,
    atom_positions: Point3DArray,
):
    detector_normal = np.array([np.cos(diffraction_angle), 0.0, np.sin(diffraction_angle)])
    emitter_normal = np.array([np.cos(diffraction_angle), 0.0, -np.sin(diffraction_angle)])
    distances_emitter_to_atom = calculate_distances_to_reference_plane(atom_positions, emitter_normal)
    measurement_at_atom = np.cos(distances_emitter_to_atom / wavelength * 2 * np.pi + phase)
    distances_atom_to_detector = calculate_distances_to_reference_plane(atom_positions, detector_normal)
    return np.sum(
        measurement_at_atom * np.cos((distances_emitter_to_atom + distances_atom_to_detector) / wavelength * 2 * np.pi + phase)
    )


class XRayDiffraction():
    def __init__(
        self,
        atom_positions: Point3DArray,
    ):
        self.atom_positions: Point3DArray = atom_positions

    def measure(
        self,
        wavelength: float,
        phase: float,
        diffraction_angle: float,
    ) -> float:
        return measure_multiple_atoms(wavelength, phase, diffraction_angle, self.atom_positions)


from simclf.reader import Reader
from simclf.generators.close_packed import generate_close_packed_plane_sequence

reader = Reader("./out/20260301-223321_adaptive_gradient_descent_1.0")
atom_positions = reader.read_points_from_csv("step_00499.csv")
#atom_positions = generate_close_packed_plane_sequence("ACAB", 10, 10, 3.006855086348474e-10)

with open("./deleteme.txt", "w") as fout:
    for x, y, z in atom_positions:
        fout.write(f"{x},{y},{z}\n")

xray = XRayDiffraction(
    atom_positions=atom_positions,
)

measurements = []

for theta in np.linspace(0.0, np.pi / 2, 1000):
    wavelength = 3.006855086348474e-10 / 3.0
    this_measurement = 0.0
    for phase in np.linspace(0.0, np.pi * 2, 100):
        measurement = xray.measure(wavelength, phase, theta)
        this_measurement += np.abs(measurement)
    measurements.append(this_measurement)

measurements = np.abs(np.array(measurements))

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(measurements)

plt.show()

