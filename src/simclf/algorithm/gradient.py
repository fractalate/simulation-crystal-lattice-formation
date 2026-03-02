import numpy as np


def _index_tensor(tensor):
    number_of_cells = np.prod(tensor.shape)
    for i in np.arange(number_of_cells):
        yield np.unravel_index(i, tensor.shape)

def index_tensor_excluding(tensor, omit_list):
    for idx in _index_tensor(tensor):
        if not any(np.array_equal(idx, x) for x in omit_list):
            yield idx


# If you pass `gradient`, it will get updated in-place.
def calculate_gradient(input_tensor, objective_function, step_size, gradient=None, index=None):
    tensor = np.copy(input_tensor)
    if gradient is None:
        gradient = np.zeros_like(tensor)
    if index is None:
        index = _index_tensor(tensor)
    for idx in index:
        original_value = tensor[idx]
        tensor[idx] = original_value - step_size / 2.0
        value0 = objective_function(tensor)
        tensor[idx] = original_value + step_size / 2.0
        value1 = objective_function(tensor)
        tensor[idx] = original_value
        gradient[idx] = value1 - value0
    return gradient
