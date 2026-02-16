import numpy as np

from simclf.typing import Point3D, Point3DArray


def generate_uniform_points_3d(extents_a: Point3D, extents_b: Point3D, count: int) -> Point3DArray:
    return np.random.uniform(
        low=extents_a,
        high=extents_b,
        size=(count, 3),
    )
