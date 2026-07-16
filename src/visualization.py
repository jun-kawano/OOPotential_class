import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)


def save_frame(field, step, cmap_min= -10.0, cmap_max= 10.0):
    """
    Generates and saves the dual-visualization frame containing both
    a quiver plot and a streamplot for a given FlowField.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for ax in (ax1, ax2):
        ax.set_aspect('equal')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_xlim(field.x_bounds)
        ax.set_ylim(field.y_bounds)
        ax.set_title(f"Step {step} | Active Doublets: {len(field.potential_flows)}")

    # left quiver plot
    ax1.pcolormesh(field.X, field.Y, field.PHI, cmap='jet',
                   vmin=cmap_min, vmax=cmap_max)

    stride = 6
    ax1.quiver(field.X[::stride, ::stride], field.Y[::stride, ::stride],
               field.U[::stride, ::stride], field.V[::stride, ::stride],
               color='black', pivot='middle')

    # right streamplot
    ax2.pcolormesh(field.X, field.Y, field.PHI, cmap='jet',
                   vmin=cmap_min, vmax=cmap_max)

    ax2.streamplot(field.X, field.Y, field.U, field.V, color='black', density=1, linewidth=0.5)

    # plot doublet positions
    for elem in field.potential_flows:
        ax1.plot(elem.x0, elem.y0, 'o', color='lime', markersize=5, markeredgecolor='black')
        ax2.plot(elem.x0, elem.y0, 'o', color='lime', markersize=5, markeredgecolor='black')

    plt.tight_layout()

    filename = f"output/frame_{step:04d}.png"
    plt.savefig(filename, dpi=120)
    plt.close(fig)