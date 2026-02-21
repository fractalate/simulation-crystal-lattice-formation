import sys
import argparse

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np

from simclf.reader import read_points_from_csv


parser = argparse.ArgumentParser()
parser.add_argument("--edge_method", "--edge-method", dest="edge_method", required=False)
parser.add_argument("-o", "--output", dest="output", required=False)
parser.add_argument("file_names", nargs="+")

args = parser.parse_args()

animated = False

if len(args.file_names) == 0:
    print("no files")
    sys.exit(1)
elif len(args.file_names) > 1:
    animated = True


def calculate_segments_and_colors(atom_positions):
    segments = []
    colors = []

    if not args.edge_method:

        pass

    elif args.edge_method == "experimental":

        for i in range(atom_positions.shape[0] - 1):
            for j in range(i + 1, atom_positions.shape[0]):
                x0, y0, z0 = p0 = atom_positions[i]
                x1, y1, z1 = p1 = atom_positions[j]
                dist = np.linalg.norm(p1 - p0)
                if dist < 3.006855086348474e-10 * 1.25:
                    segments.append([
                        [x0, y0, z0],
                        [x1, y1, z1],
                    ])
                    if dist > 3.006855086348474e-10:
                        high, low = 3.006855086348474e-10 * 1.25, 3.006855086348474e-10
                        ratio_red = (dist - low) / (high - low)
                        ratio_green = 1 - ratio_red
                        colors.append((ratio_red, ratio_green, 0.0, 0.25))
                    elif dist > 3.006855086348474e-10 / 2:
                        high, low = 3.006855086348474e-10, 3.006855086348474e-10 / 2
                        ratio_green = (dist - low) / (high - low)
                        ratio_blue = 1 - ratio_green
                        colors.append((0.0, ratio_green, ratio_blue, 0.25))
                    else:
                        colors.append("black")

    else:

        raise RuntimeError(f"unhandled {args.edge_method=}")

    # Make a dummy segment that's invisible so Line3DCollection cooperates with ax.add_collection3d().
    if not segments:
        segments.append([(0, 0, 0), (0, 0, 0)])
        colors.append((0, 0, 0, 0))

    segments = np.array(segments)
    return segments, colors


atom_positions = read_points_from_csv(args.file_names[0])
x = atom_positions[:, 0]
y = atom_positions[:, 1]
z = atom_positions[:, 2]

segments, colors = calculate_segments_and_colors(atom_positions)
line_collection = Line3DCollection(segments, colors=colors)

fig = plt.figure()
ax = fig.add_subplot(projection="3d", proj_type="ortho")
scatter_plot = ax.scatter(x, y, z)  # type: ignore
lines_plot = ax.add_collection3d(line_collection)

ani = None
if animated:
    def update(frame):
        global x, y, z
        global atom_positions
        global segments
        global colors

        index = frame + 1
        atom_positions = read_points_from_csv(args.file_names[index])
        x = atom_positions[:, 0]
        y = atom_positions[:, 1]
        z = atom_positions[:, 2]

        scatter_plot._offsets3d = (x, y, z)  # type: ignore

        segments, colors = calculate_segments_and_colors(atom_positions)

        line_collection.set_segments(segments)  # type: ignore
        line_collection.set_colors(colors)

        return (scatter_plot, lines_plot)

    ani = FuncAnimation(fig, update, frames=len(args.file_names) - 1, interval=50)

# Output still images before showing.
if args.output:
    if not animated:
        plt.savefig(args.output, dpi=300)

plt.show()

# Output animations after showing.
if args.output:
    if animated:
        if ani:
            ani.save(args.output, writer="pillow", fps=20)
