from src.potential_flow import PotentialFlow
import numpy as np

class Doublet(PotentialFlow):

    def __init__(self, strength, x0=0.0, y0=0.0):
        self.strength = strength
        self.x0 = x0
        self.y0 = y0

    def potential(self, x, y):
        dx = x - self.x0
        dy = y - self.y0
        r2 = dx**2 + dy**2
        r2 = np.where(r2 < 1e-10, 1e-10, r2)
        return (self.strength / (2 * np.pi)) * dx / r2