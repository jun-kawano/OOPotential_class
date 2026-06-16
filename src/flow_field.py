import numpy as np

class FlowField:
    def __init__(self, Nx=100, Ny=100,
                 x_bounds=(-5, 5),
                 y_bounds=(-5, 5)):
        self.Nx = Nx
        self.Ny = Ny
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.potential_flows = []

        self.X, self.Y = self.initialize_domain()
        self.PHI = np.full_like(self.X, 0)

    def add(self, potential_flow):
        self.potential_flows.append(potential_flow)

    def initialize_domain(self):
        x_min = self.x_bounds[0]
        x_max = self.x_bounds[1]
        y_min = self.y_bounds[0]
        y_max = self.y_bounds[1]

        xx = np.linspace(x_min, x_max, num=self.Nx)
        yy = np.linspace(y_min, y_max, num=self.Ny)

        X, Y = np.meshgrid(xx, yy)
        return X, Y

    def compute(self):
        for potential_flow in self.potential_flows:
            self.PHI += potential_flow.potential(self.X, self.Y)