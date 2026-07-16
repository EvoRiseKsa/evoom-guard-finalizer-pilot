def add(left: int, right: int) -> int:
    """Return the mathematical sum of two integers."""
    if type(left) is not int or type(right) is not int:
        raise TypeError("left and right must be integers")
    return left + right
