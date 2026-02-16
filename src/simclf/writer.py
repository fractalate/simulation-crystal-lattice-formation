import json
from pathlib import Path
import time

from simclf.typing import Point3DArray, check_point_3d_array


class Writer():
    def __init__(
        self,
        simulation_name: str,
        simulation_version: str,
        output_directory: None | str | Path = None,
    ):

        self.simulation_name: str = simulation_name
        self.simulation_version: str = simulation_version
        if output_directory is None:
            simulation_stamp: str = time.strftime("%Y%m%d-%H%M%S")
            self.output_directory: Path = (
                Path("out") / Path(f"{simulation_stamp}_{self.simulation_name}_{self.simulation_version}")
            )
        else:
            self.output_directory: Path = Path(output_directory)

    def ensure_output_directory_exists(self):
        output_directory = self.output_directory
        if not output_directory.is_dir():
            output_directory.mkdir(parents=True)  # TODO do I need an explicit mask?
        return output_directory

    def write_points_to_csv(self, file_name: str | Path, points: Point3DArray, overwrite: bool = False):
        check_point_3d_array(points)

        file_path = self.ensure_output_directory_exists() / Path(file_name)

        if not overwrite:
            if file_path.exists():
                raise FileExistsError(file_path)  # XXX is this valid?

        with open(file_path, "w") as fout:
            for x, y, z in points:
                fout.write(f"{x},{y},{z}\n")

    def write_object_to_json(self, file_name: str | Path, obj: dict, overwrite: bool = False):
        file_path = self.ensure_output_directory_exists() / Path(file_name)

        if not overwrite:
            if file_path.exists():
                raise FileExistsError(file_path)  # XXX is this valid?

        with open(file_path, "w") as fout:
            fout.write(json.dumps(obj, indent=2))
            fout.write("\n")
