def calculate_equilibrium_spacing(
    attractive_factor: float,
    repulsive_factor: float,
    repulsive_power: float,
):
    """
    Calculates the equilibrium spacing between atoms by finding the location of minimum potential in
    the sum of the atom's attractive and repulsive potential fields.

    A is attractive_factor
    r is distance between atoms
    E_A is attractive potential

    E_A = -A / r

    B is repulsive_factor
    n is repulsive_power
    r is distance between atoms
    E_B is repulsive potential

    E_B = B / r^n
    """
    # XXX Outline the derivation. With E(r) = B / r^n - A / r. Then dE/dr can be found and you end up with this equal to 0 when:
    return (repulsive_power * repulsive_factor / attractive_factor) ** (1 / (repulsive_power - 1))


