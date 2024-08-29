import numpy as np
import matplotlib.pyplot as plt
import os

def plot_violin(ax, data_paths, index):
    for row, data_path in enumerate(data_paths):
        a = []
        b = []

        for i in range(30):
            rmsd = np.loadtxt(os.path.join(data_path, f"rmsd_{i}.dat"), skiprows=1)[:, 1]
            replica_index = np.ones_like(rmsd) * (i + 1)
            a.append(rmsd)
            b.append(i)

        # Use red for the last three entries in column 2
        print(index)
        print(row)
        color = '#2E86C1' if index < 2  else '#EC7063'
        parts = ax[row].violinplot(a, b, showmeans=True, showmedians=False, vert=False, widths=1.5, points=1000)

        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_edgecolor(color)
            pc.set_alpha(1.0)
            pc.set_linewidth(1.0)

        for partname in ('cbars', 'cmins', 'cmaxes'):
            vp = parts[partname]
            vp.set_edgecolor('silver')
            vp.set_linewidth(0.5)

        for partname in ('cmeans',):
            vp = parts[partname]
            vp.set_edgecolor("silver")
            vp.set_linewidth(1)

        ax[row].vlines(4, -1, 35, color='black', linestyles='dashed', linewidth=2.0)
        ax[row].set_xlim(0, 35)
        ax[row].set_ylim(-1, 35)
        ax[row].set_xticks(np.arange(0, 35, 10))
        ax[row].tick_params(axis='both', which='major', labelsize=20, width=2, size=7,)
        ax[row].set_yticks(np.arange(0, 35, 10))

        # Set the y-axis label only for the first column
        if index == 2 :
            ax[row].set_yticklabels([])

        # Remove x-axis labels for all but the last row
        if row == 2:
            ax[row].set_xticklabels(np.arange(0, 35, 10), size=20, weight='bold')

        for spine in ax[row].spines.values():
            spine.set_linewidth(2)

        for label in ax[row].get_xticklabels() + ax[row].get_yticklabels():
            label.set_weight("bold")

# List of dataset paths
dataset_paths = [
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/no_ps/3GB1/trajectories/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.25/3GB1/trajectories/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.5/3GB1/trajectories/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/1.0/3GB1/trajectories/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/2.0/3GB1/trajectories/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/4.0/3GB1/trajectories/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/8.0/3GB1/trajectories/',
]

# Create a figure and subplots
fig, axes = plt.subplots(3, 2, figsize=(7,7), sharex=True, gridspec_kw={'hspace': 0.00, 'wspace': 0.0})
#fig, axes = plt.subplots(3, 2, figsize=(14, 7 * len(dataset_paths)), sharex='col', sharey='row', gridspec_kw={'hspace': 0.00, 'wspace': 0.0})

# Plot each dataset on a subplot
for i, (ax, data_paths) in enumerate(zip(axes.T, [dataset_paths[:3], dataset_paths[3:]]), start=1):
    plot_violin(ax, data_paths, i)
#plt.figure(facecolor =None)
# Save the figure
plt.tight_layout()

plt.savefig("stacked_subplots_poster.pdf", dpi=320)
plt.savefig("stacked_subplots_poster.png", dpi=320)
plt.show()

