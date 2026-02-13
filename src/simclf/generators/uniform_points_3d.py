import numpy as np

from simclf.typing import Point3D, Point3DArray


def generate_uniform_points_3d(extents_a: Point3D, extents_b: Point3D, count: int) -> Point3DArray:
    parts = []

    for i in range(3):
        low, high = min(extents_a[i], extents_b[i]), max(extents_a[i], extents_b[i])
        parts.append(np.random.uniform(
            low=low,
            high=high,
            size=count,
        ))

    return np.stack(parts).T
