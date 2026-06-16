class PotentialFlow:
    """Base class for 2D potential flow elements."""

    def potential(self, x, y):
        """Velocity potential phi(x, y)."""
        raise NotImplementedError