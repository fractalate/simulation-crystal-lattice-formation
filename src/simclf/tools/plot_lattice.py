import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from simclf.reader import read_points_from_csv


animated = False
file_names = sys.argv[1:]

if len(file_names) == 0:
    print("no files")
    sys.exit(1)
elif len(file_names) > 1:
    animated = True


atom_positions = read_points_from_csv(file_names[0])
x = atom_positions[:, 0]
y = atom_positions[:, 1]
z = atom_positions[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection="3d", proj_type="ortho")
scatter_plot = ax.scatter(x, y, z)  # type: ignore

ani = None
if animated:
    def update(frame):
        global x, y, z

        index = frame + 1
        atom_positions = read_points_from_csv(file_names[index])
        x = atom_positions[:, 0]
        y = atom_positions[:, 1]
        z = atom_positions[:, 2]

        scatter_plot._offsets3d = (x, y, z)  # type: ignore

        return (scatter_plot, )

    ani = FuncAnimation(fig, update, frames=len(file_names) - 1, interval=50)

plt.show()

if animated:
    if ani:
        ani.save("out.gif", writer="pillow", fps=20)
