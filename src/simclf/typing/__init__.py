import numpy as np
import numpy.typing as npt

# Since the dimension of the numpy array isn't encoded in the type system, these are mostly for
# indicating the disposition of values. Use check functions if you need to validate that values
# are indeed the correct type and shape.
Point3D = npt.NDArray[np.float64]
Point3DArray = npt.NDArray[np.float64]  # TODO: is this really a good way to represent points?
Lattice3D = npt.NDArray[np.float64]

def check_point_3d(point: Point3D):
    if point.shape != (3, ):
        raise ValueError(f"invalid Point3D shape {point.shape}")
    if point.dtype != np.float64:
        raise ValueError(f"invalid Point3D dtype {point.dtype}")

def check_point_3d_array(point: Point3DArray):
    if len(point.shape) != 2:
        raise ValueError(f"invalid Point3DArray shape {point.shape}")
    if point.shape[1:] != (3, ):
        raise ValueError(f"invalid Point3DArray shape {point.shape}")
    if point.dtype != np.float64:
        raise ValueError(f"invalid Point3DArray dtype {point.dtype}")

def check_lattice_3d(lattice: Lattice3D):
    if len(lattice.shape) != 3:
        raise ValueError(f"invalid Lattice3D shape {lattice.shape}")
    if lattice.dtype != np.float64:
        raise ValueError(f"invalid Lattice3D dtype {lattice.dtype}")

