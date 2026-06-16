import matplotlib.pyplot as plt
import numpy as np

from src.source import Source
from src.flow_field import FlowField

field = FlowField()


s_1 = Source(10, -1,0)
field.add(s_1)

s_2 = Source(-10, 1,0)
field.add(s_2)


x_0_s = np.random.uniform(low=field.x_bounds[0], high=field.x_bounds[1], size=20)
y_0_s = np.random.uniform(low=field.y_bounds[0], high=field.y_bounds[1], size=20)
for i in range(20):
    s_2 = Source(-10, x_0_s[i], y_0_s[i])
    field.add(s_2)

N_steps = 10
for i_step in range(N_steps):
    field.step()
    plt.pcolormesh(field.X, field.Y, field.PHI)
    plt.streamplot(field.X, field.Y, field.U, field.V)
    plt.show()

# field.compute()
#
#
# plt.pcolormesh(field.X, field.Y, field.PHI)
# # plt.streamplot(field.X, field.Y, field.PHI)
# plt.show()




a = 2