from typing import TypeGuard

import numpy as np
import numpy.typing as npt

# Since the dimension of the numpy array isn't encoded in the type system, these are mostly for
# indicating the disposition of values. Use check functions if you need to validate that values
# are indeed the correct type and shape.
Scalers = npt.NDArray[np.float64]
Point3D = npt.NDArray[np.float64]
Point3DArray = npt.NDArray[np.float64]
Lattice3D = npt.NDArray[np.float64]

def check_scalers(scalers: Scalers)-> TypeGuard[Scalers]:
    if len(scalers.shape) != 1:
        raise ValueError(f"invalid Scalers shape {scalers.shape}")
    if scalers.dtype != np.float64:
        raise ValueError(f"invalid Scalers dtype {scalers.dtype}")
    return True

def check_point_3d(point: Point3D)-> TypeGuard[Point3D]:
    if point.shape != (3, ):
        raise ValueError(f"invalid Point3D shape {point.shape}")
    if point.dtype != np.float64:
        raise ValueError(f"invalid Point3D dtype {point.dtype}")
    return True

def check_point_3d_array(point: Point3DArray) -> TypeGuard[Point3DArray]:
    if len(point.shape) != 2:
        raise ValueError(f"invalid Point3DArray shape {point.shape}")
    if point.shape[1:] != (3, ):
        raise ValueError(f"invalid Point3DArray shape {point.shape}")
    if point.dtype != np.float64:
        raise ValueError(f"invalid Point3DArray dtype {point.dtype}")
    return True

def check_lattice_3d(lattice: Lattice3D) -> TypeGuard[Lattice3D]:
    if len(lattice.shape) != 3:
        raise ValueError(f"invalid Lattice3D shape {lattice.shape}")
    if lattice.dtype != np.float64:
        raise ValueError(f"invalid Lattice3D dtype {lattice.dtype}")
    return True
