import numpy as np
import matplotlib.pyplot as plt

# List of dataset paths
dataset_paths = [
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/no_ps/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.25/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.5/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/1.0/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/2.0/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/4.0/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/8.0/3GB1/walkers/',
]

# Load the pre-calculated KDE values for all datasets
kde_data = [np.load(f'kde_data_dataset_{i + 1}.npy') for i in range(len(dataset_paths))]
t = np.load(f't_values_dataset_1.npy')  # Assuming t values are the same for all datasets

# Create a figure and subplots with square dimensions
fig, axes = plt.subplots(3, 2, figsize=(7, 7), sharex=True, gridspec_kw={'hspace': 0.00, 'wspace': 0.0})

# Plot individual graphs for each file
for i, (kde_data_i, path) in enumerate(zip(kde_data, dataset_paths)):
    row = i % 3
    col = i //3

    for traj in range(30):
        # Use red for the last three entries in column 2
        #color = '#EC7063' if col == 1 else '#2E86C1'
        color = 'red' if col == 1 else '#2E86C1'
        ax = axes[row, col]
        ax.plot(t, kde_data_i[traj], '-', linewidth=1.0, color=color)

    # Set common properties for both columns
    for col in [0, 1]:
        axes[row, col].vlines(4, -1, 230, color='black', linestyles='dashed', linewidth=2.0)
        axes[row, col].set_xlim(0, 24)
        axes[row, col].set_ylim(0, 230)
        axes[row, col].set_xticks(np.arange(0, 24, 5))
        axes[row, col].tick_params(axis='both', which='major', labelsize=20, width=3, size=7,)
        axes[row, col].set_yticks(np.arange(0, 230, 100))
        ylabels = ['{:.1f}'.format(y/100) for y in axes[row, col].get_yticks()]
        axes[row, col].set_yticklabels(ylabels)
        # Remove x-axis labels for all but the last row
        #if row == 2:
         #   axes[row,col].set_xticklabels(np.arange(0, 23, 4), size=20, weight='bold')
            #axes[row, col].set_xticklabels([])

        # Set the linewidth of the entire border
        for spine in axes[row, col].spines.values():
            spine.set_linewidth(2)
            # Make tick labels bold
        for label in axes[row, col].get_xticklabels() + axes[row, col].get_yticklabels():
            label.set_weight("bold")
        # Set the y-axis label only for the first column
        if col == 1 :
            axes[row,col].set_yticklabels([])
        # Add x-axis label to the last row
        if row == 2:
            axes[row, col].set_xticklabels(np.arange(0, 24, 5), size=20, weight='bold')

# Add y-axis labels to column 1 only
#for i in range(3):
#    axes[i, 0].set_ylabel('RMSD (Å)', size=15, weight='bold')



plt.tight_layout()


# Save the figure
plt.savefig("kde_subplots_modified.pdf", dpi=320)
plt.savefig("kde_subplots_modified.png", dpi=320)
plt.show()

