import numpy as np

from simclf.algorithm.gradient import calculate_gradient
from simclf.generators.uniform_points_3d import generate_uniform_points_3d
from simclf.physics.atom import calculate_equilibrium_spacing
from simclf.physics.energy import calculate_potential_energy_of_basic_system
from simclf.reader import Reader
from simclf.typing import Point3DArray
from simclf.writer import Writer


class SimulationGradientDescent():
    def __init__(
        self,
        attractive_factor: float,
        repulsive_factor: float,
        repulsive_power: float,
        atom_positions: Point3DArray,
        gradient: Point3DArray,
    ):
        self.attractive_factor: float = attractive_factor
        self.repulsive_factor: float = repulsive_factor
        self.repulsive_power: float = repulsive_power
        self.atom_positions: Point3DArray = atom_positions
        self.gradient: Point3DArray = gradient
        self.potential_energy_of_system: float = calculate_potential_energy_of_basic_system(
            atom_positions=self.atom_positions,
            attractive_factor=self.attractive_factor,
            repulsive_factor=self.repulsive_factor,
            repulsive_power=self.repulsive_power,
        )

    def save_state(self, writer: Writer):
        writer.write_object_to_json("state.json", {
            "attractive_factor": self.attractive_factor,
            "repulsive_factor": self.repulsive_factor,
            "repulsive_power": self.repulsive_power,
        }, overwrite=True)
        writer.write_points_to_csv("state.atom_positions.csv", self.atom_positions, overwrite=True)
        writer.write_points_to_csv("state.gradient.csv", self.gradient, overwrite=True)

    @staticmethod
    def load_state(reader: Reader):
        config = reader.read_object_from_json("state.json")
        atom_positions = reader.read_points_from_csv("state.atom_positions.csv")
        gradient = reader.read_points_from_csv("state.gradient.csv")
        return {
            **config,
            "atom_positions": atom_positions,
            "gradient": gradient,
        }

    def get_potential_energy_of_system(self):
        return self.potential_energy_of_system

    def step(self, step_size: float):
        def objective_function(atom_positions):
            return calculate_potential_energy_of_basic_system(
                atom_positions=atom_positions,
                attractive_factor=self.attractive_factor,
                repulsive_factor=self.repulsive_factor,
                repulsive_power=self.repulsive_power,
            )
        self.gradient = calculate_gradient(
            self.atom_positions,
            objective_function,
            step_size,
            gradient=self.gradient,
        )

        scale_factor = np.linalg.norm(self.gradient.flatten())
        if scale_factor > 0.0:
            perturbation = - self.gradient / scale_factor * step_size

            attempt = 0
            reductions = 0
            while True:
                # March ahead while there are gains.
                attempt += 1
                atom_positions_next = self.atom_positions + perturbation
                potential_energy_of_system_next = calculate_potential_energy_of_basic_system(
                    atom_positions=atom_positions_next,
                    attractive_factor=self.attractive_factor,
                    repulsive_factor=self.repulsive_factor,
                    repulsive_power=self.repulsive_power,
                )

                if potential_energy_of_system_next < self.potential_energy_of_system:
                    self.atom_positions = atom_positions_next
                    self.potential_energy_of_system = potential_energy_of_system_next
                elif reductions < 5:
                    perturbation /= 2.0
                    reductions += 1
                    attempt -= 1
                elif attempt <= 1:
                    break
                else:
                    break


def setup_and_run_simulation(
    number_of_atoms: int = 20,
    number_of_steps: int = 100,
):
    if number_of_atoms < 1:
        raise Exception(f"invalid {number_of_atoms=}. must be 1 or more.")

    if number_of_steps < 1:
        raise Exception(f"invalid {number_of_steps=}. must be 1 or more.")

    attractive_factor = 3.6e-28
    repulsive_factor = 1.0e-95
    repulsive_power = 8.0

    equilibrium_spacing = calculate_equilibrium_spacing(
        attractive_factor=attractive_factor,
        repulsive_factor=repulsive_factor,
        repulsive_power=repulsive_power,
    )
    # We'll simulate in a cube, so we roughly cube root N atoms along each axis.
    # Scale it down so we're really packing things into the space.
    # The system should expand to reach equilibrium.
    simulation_dimension = number_of_atoms**(1/3) * (2 * equilibrium_spacing) * .5
    step_size = equilibrium_spacing / 10.0

    atom_positions = generate_uniform_points_3d(
        np.array([-simulation_dimension / 2.0, -simulation_dimension / 2.0, -simulation_dimension / 2.0]),
        np.array([ simulation_dimension / 2.0,  simulation_dimension / 2.0,  simulation_dimension / 2.0]),
        number_of_atoms,
    )

    # XXX maybe it's a good idea to make sure the atoms are not too close to each other.

    simulation = SimulationGradientDescent(
        attractive_factor=attractive_factor,
        repulsive_factor=repulsive_factor,
        repulsive_power=repulsive_power,
        atom_positions=atom_positions,
        gradient=np.zeros_like(atom_positions)
    )

    writer = Writer("gradient_descent", "1.2")

    writer.info(f"output will be written to {writer.output_directory}")

    writer.write_object_to_json("config.json", {
        "equilibrium_spacing": equilibrium_spacing,
        "number_of_atoms": number_of_atoms,
        "number_of_steps": number_of_steps,
        "simulation_dimension": simulation_dimension,
        "step_size": step_size,
    })

    def save_step(step_number: int, extra: None | dict = None):
        nonlocal simulation
        nonlocal writer
        writer.write_points_to_csv(f"step_{step_number:05d}.csv", simulation.atom_positions)
        writer.write_object_to_json(f"step_{step_number:05d}.json", {
            **(extra or {}),
            "potential_energy_of_system": simulation.get_potential_energy_of_system(),
        })

    simulation.save_state(writer)
    save_step(0)

    for step_number in range(1, number_of_steps):
        potential_energy_of_system_before = simulation.get_potential_energy_of_system()

        writer.info(f"{step_number=}")
        simulation.step(step_size / ((step_number // 10) + 1))

        potential_energy_of_system_after = simulation.get_potential_energy_of_system()
        change_in_potential_energy = potential_energy_of_system_after - potential_energy_of_system_before

        simulation.save_state(writer)
        save_step(step_number, {
            "change_in_potential_energy": change_in_potential_energy,
        })

    writer.info(f"see output in {writer.output_directory}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--atoms", "--number_of_atoms", "--number-of-atoms", dest="number_of_atoms", type=int)
    parser.add_argument("--steps", "--number_of_steps", "--number-of-steps", dest="number_of_steps", type=int)

    args = {}
    for k, v in vars(parser.parse_args()).items():
        if v is not None:
            args[k] = v

    setup_and_run_simulation(**args)
