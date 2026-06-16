import numpy as np

from src.potential_flow import PotentialFlow


class Source(PotentialFlow):

    def __init__(self, strength,x0=0.0, y0=0.0):
        self.strength = strength
        self.x0 = x0
        self.y0 = y0

    def potential(self, x, y):
        r2 = (x - self.x0) ** 2 + (y - self.y0) ** 2
        r2 = np.where(r2 < 1e-10, 1e-10, r2)
        return (self.strength / (2 * np.pi) * np.log(np.sqrt(r2)))
