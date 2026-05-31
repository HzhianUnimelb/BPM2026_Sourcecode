import matplotlib.pyplot as plt
import scipy.interpolate as si
from matplotlib import cm
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np

def grids_maker(filepath):
    # Get the data
    df = pd.read_csv(filepath, sep='\s+', header=0)

    # Extract the columns
    x = df['XA']
    y = df['YA']
    z = df['ZA']
    g = df['GA']

    reso_x = reso_y = 50
    interp = 'cubic'  # or 'nearest' or 'linear'

    # Convert the 4d-space's dimensions into grids
    grid_x, grid_y = np.mgrid[
        x.min():x.max():1j*reso_x,
        y.min():y.max():1j*reso_y
    ]

    grid_z = si.griddata(
        np.column_stack((x, y)), z.values,
        (grid_x, grid_y),
        method=interp
    )

    grid_g = si.griddata(
        np.column_stack((x, y)), g.values,
        (grid_x, grid_y),
        method=interp
    )

    return {
        'x': grid_x,
        'y': grid_y,
        'z': grid_z,
        'g': grid_g,
    }

fgrids = dict.fromkeys([

    'sim_totaloutput0.07.txt'
])
g_values = []  # Store all g values for normalization

# Create a figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, fpath in enumerate(fgrids.keys()):
    fgrids[fpath] = grids = grids_maker(fpath)
    g_values.extend(grids['g'].flatten())  # Collect all g values

# Normalize the color range based on the g values
norm = Normalize(vmin=min(g_values), vmax=max(g_values))

for i, fpath in enumerate(fgrids.keys()):
    grids = fgrids[fpath]
    
    # Plot the 3D surface with a vertical offset
    surf = ax.plot_surface(
        grids['x'], grids['y'], grids['z'] + i,
        facecolors=cm.jet_r(norm(grids['g'])),  # Use the reversed colormap here
        antialiased=True,
        rstride=1, cstride=1, alpha=None
    )

# Set the z-axis limits based on the minimum and maximum values

# Add axis labels
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

plt.show()
