import matplotlib.pyplot as plt
import numpy as np

from src.doublet import Doublet
from src.source import Source
from src.flow_field import FlowField

field = FlowField(
    Nx=150,
    Ny=150,
    x_bounds=(-8, 8),
    y_bounds=(-8, 8),
    dt=0.01
)

np.random.seed(42)

N_random_doublets = 15
x_0_s = np.random.uniform(low=field.x_bounds[0], high=field.x_bounds[1], size=N_random_doublets)
y_0_s = np.random.uniform(low=field.y_bounds[0], high=field.y_bounds[1], size=N_random_doublets)

magnitudes = np.random.uniform(low=5, high=15, size=N_random_doublets)
signs = np.random.choice([-1, 1], size=N_random_doublets)
strengths = magnitudes * signs

for i in range(N_random_doublets):
    s_2 = Doublet(strength=strengths[i], x0=x_0_s[i], y0=y_0_s[i])
    field.add(s_2)

N_steps = 30

phi_min_cmap = -10.0  # fixed color lims to improve visualization
phi_max_cmap = 10.0

for i_step in range(N_steps):
    field.step()

    plt.figure(figsize=(8, 8))
    plt.title(f"Step {i_step + 1} | Time: {field.time:.2f}s | Active Doublets: {len(field.potential_flows)}")
    plt.pcolormesh(field.X, field.Y, field.PHI, shading='auto', cmap='jet', vmin=phi_min_cmap, vmax=phi_max_cmap)

    plt.colorbar(label='Potential (PHI)')
    plt.streamplot(field.X, field.Y, field.U, field.V, color='black', density=1, linewidth=0.5)
    for elem in field.potential_flows:
        plt.plot(elem.x0, elem.y0, 'o', color='lime', markersize=5, markeredgecolor='black')

    plt.xlim(field.x_bounds)
    plt.ylim(field.y_bounds)
    plt.tight_layout()
    plt.show()