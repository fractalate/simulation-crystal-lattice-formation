import csv
import json
from pathlib import Path

import numpy as np

from simclf.typing import Point3DArray


class Reader():
    def __init__(self, input_directory: str | Path):
        self.input_directory = Path(input_directory)

    def read_points_from_csv(self, file_name: str | Path) -> Point3DArray:
        input_path = self.input_directory / Path(file_name)

        points = []

        with open(input_path, "r") as fin:
            for x, y, z in csv.reader(fin):
                points.append([float(x), float(y), float(z)])
        
        return np.array(points)

    def read_object_from_json(self, file_name: str | Path) -> dict:
        input_path = self.input_directory / Path(file_name)

        with open(input_path, "r") as fin:
            return json.loads(fin.read())

