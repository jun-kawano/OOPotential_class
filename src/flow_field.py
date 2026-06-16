import numpy as np

class FlowField:
    def __init__(self, Nx=100, Ny=100,
                 x_bounds=(-5, 5),
                 y_bounds=(-5, 5),
                 dt=0.001):
        self.Nx = Nx
        self.Ny = Ny
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.potential_flows = []
        self.time = 0.0
        self.dt = dt

        self.X, self.Y = self.initialize_domain()
        self.U = None
        self.V = None
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

    def compute_velocity(self):
        dx = self.X[0, 1] - self.X[0, 0]
        dy = self.Y[1, 0] - self.Y[0, 0]

        self.U, self.V = np.gradient(self.PHI, dx, dy, edge_order=2)
        self.V, self.U = self.U, self.V  # np.gradient returns (d/dy, d/dx) — swap needed

    def step(self):
        self.compute()
        self.compute_velocity()