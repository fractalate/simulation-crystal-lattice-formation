import csv
import json
from pathlib import Path

import numpy as np

from simclf.typing import Point3DArray


class Reader():
    def __init__(self, input_directory: str | Path):
        self.input_directory = Path(input_directory)

    def read_points_from_csv(self, file_name: str | Path) -> Point3DArray:
        return read_points_from_csv(self.input_directory / Path(file_name))

    def read_object_from_json(self, file_name: str | Path) -> dict:
        return read_object_from_json(self.input_directory / Path(file_name))

    def read_document(self, file_name: str | Path) -> str:
        return read_document(self.input_directory / Path(file_name))


def read_points_from_csv(file_name: str | Path) -> Point3DArray:
    points = []

    with open(file_name, "r") as fin:
        for x, y, z in csv.reader(fin):
            points.append([float(x), float(y), float(z)])
    
    return np.array(points)

def read_object_from_json(file_name: str | Path) -> dict:
    with open(file_name, "r") as fin:
        return json.loads(fin.read())

def read_document(file_name: str | Path) -> str:
    with open(file_name, "r") as fin:
        return fin.read()
