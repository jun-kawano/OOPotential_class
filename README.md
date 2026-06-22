# OOPotential_class

A Python framework for 2D potential flow simulation using Object-Oriented Programming principles.

**Course:** EMC410235 — Scientific Programming for Thermal Engineering and Science

## Project Structure

```
OOPotential_class/
├── src/
│   ├── potential_flow.py    # Abstract base class for flow elements
│   ├── source.py            # Source element (radial outflow)
│   ├── doublet.py           # Doublet element (dipole)
│   └── flow_field.py        # Flow field container and solver
├── main.py                  # Example usage and visualization
└── README.md
```

## Classes

### `PotentialFlow`
Abstract base class for flow elements.

### `Source`
Radial flow element. Constructor: `Source(strength, x0=0.0, y0=0.0)`

### `Doublet`
Dipole flow element. Constructor: `Doublet(strength, x0=0.0, y0=0.0)`

### `FlowField`
Container for flow elements and solver.

**Methods:**
- `add(potential_flow)` — Add element
- `compute()` — Compute total potential from all elements
- `compute_velocity()` — Calculate velocity field
- `step()` — Execute one time step

**Attributes:**
- `X, Y` — Grid coordinates
- `PHI` — Velocity potential
- `U, V` — Velocity components

## Installation

```bash
git clone https://github.com/rafacerq/OOPotential_class.git
cd OOPotential_class
pip install numpy scipy matplotlib
```

## Usage

```python
import matplotlib.pyplot as plt
from src.doublet import Doublet
from src.flow_field import FlowField

field = FlowField(Nx=100, Ny=100)
doublet = Doublet(strength=10, x0=-1, y0=0)
field.add(doublet)
field.step()

plt.pcolormesh(field.X, field.Y, field.PHI, cmap='RdBu_r')
plt.streamplot(field.X, field.Y, field.U, field.V, color='black')
plt.show()
```

Run `python main.py` for a demonstration.

## Physical Interpretation

- **Streamlines**: Represent flow paths; fluid particles move tangent to these lines
- **Potential field**: Velocity potential φ; velocity magnitude is proportional to ∇φ
- **Velocity**: Computed as **u** = ∂φ/∂x and **v** = ∂φ/∂y using finite differences

## Implementation Notes

1. **Singularity Handling**: Floor value (1e-10) applied to r² to avoid division by zero.
2. **Velocity Computation**: `np.gradient` returns (∂φ/∂y, ∂φ/∂x); code applies swap to correct axis ordering.
3. **Interpolation**: `RegularGridInterpolator` for smooth velocity queries.

---


