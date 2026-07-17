import matplotlib.pyplot as plt
import numpy as np

from src.doublet import Doublet
from src.source import Source
from src.flow_field import FlowField
from src.visualization import save_frame

import os
os.makedirs("output", exist_ok=True)

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

N_steps = 200

cmap_min = -10.0  # fixed color lims to improve visualization
cmap_max = 10.0

for step in range(N_steps):
    field.step()
    if step % 20 == 0:
        print(f"Saving frame for step {step}...")
        save_frame(field, step, cmap_min, cmap_max)

print("Simulation complete. Check the 'output' directory for frames.")