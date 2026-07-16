import numpy as np
from scipy.interpolate import RegularGridInterpolator


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

    def interpolate_velocity(self, x_c, y_c):
        pass

    def build_interpolator(self):
        xx = self.X[0, :]  # 1D array of x-coordinates
        yy = self.Y[:, 0]  # 1D array of y-coordinates
        U_interpolator = RegularGridInterpolator((xx, yy), self.U.T)
        V_interpolator = RegularGridInterpolator((xx, yy), self.V.T)

        self.U_interpolator = U_interpolator
        self.V_interpolator = V_interpolator


    def compute(self):
        self.PHI = np.zeros_like(self.X, dtype=float) # require to not accumulate phi values
        for potential_flow in self.potential_flows:
            self.PHI += potential_flow.potential(self.X, self.Y)

    """Example on how to compute the potential without the current potential flow."""
    def compute_ignore_own(self, potential_flow):
        for potential_flow in self.potential_flows:
            if potential_flow in self.potential_flows:
                continue
            self.PHI += potential_flow.potential(self.X, self.Y)

    def compute_velocity(self):
        dx = self.X[0, 1] - self.X[0, 0]
        dy = self.Y[1, 0] - self.Y[0, 0]

        self.V, self.U = np.gradient(self.PHI, dx, dy, edge_order=2)
        #self.V, self.U = self.U, self.V  # np.gradient returns (d/dy, d/dx) — swap needed
        self.build_interpolator()


    def compute_velocity_excluding(self, exclude_element):
        """Compute PHI and velocity, skipping one element."""
        phi_without = np.zeros_like(self.X, dtype=float)
        for elem in self.potential_flows:
            if elem is not exclude_element:
                phi_without += elem.potential(self.X, self.Y)

        dx = self.X[0, 1] - self.X[0, 0]
        dy = self.Y[1, 0] - self.Y[0, 0]

        # get x and y velocities
        self.V, self.U = np.gradient(phi_without, dy, dx, edge_order=2)
        self.build_interpolator()

    def boundary_deletion(self):
        active_flows = []
        for elem in self.potential_flows:
            if (self.x_bounds[0] <= elem.x0 <= self.x_bounds[1] and
                    self.y_bounds[0] <= elem.y0 <= self.y_bounds[1]):
                active_flows.append(elem)
        self.potential_flows = active_flows

    def euler_step(self):
        element_velocities = []
        for elem in self.potential_flows:
            # update local velocity interpolators ignoring elem
            self.compute_velocity_excluding(elem)

            # use the interpolator to evaluate velocity at given coordinates
            pt = np.array([[elem.x0, elem.y0]])
            u_val = self.U_interpolator(pt)[0]
            v_val = self.V_interpolator(pt)[0]

            element_velocities.append((elem, u_val, v_val))

        for elem, u, v in element_velocities:
            # first order Euler
            elem.x0 += u * self.dt
            elem.y0 += v * self.dt

        self.boundary_deletion()
        self.time += self.dt

    def step(self):
        self.euler_step()
        self.compute()
        self.compute_velocity()