import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Function to generate a gradient of colors between blue and red
def generate_color_gradient(n):
    colors = []
    for i in range(n):
        r = i / (n - 1)
        b = 1 - r
        colors.append((r, 0, b))  # RGB tuple: (Red, Green, Blue)
    return colors

# Function to visualize the parameters for multiple datasets
def visualize_multiple_parameters(files):
    # Create a figure with subplots
    fig, axes = plt.subplots(len(files), 1, figsize=(9, 7 * len(files)), sharex=True)
    
    # Flatten axes array for easier indexing
    if len(files) == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    # Generate a list of 30 colors ranging from blue to red
    colors = generate_color_gradient(30)
    
    for i, file in enumerate(files):
        params_data = np.load(file, allow_pickle=True)
        
        ax = axes[i]
        # Use only the first parameter entry (index 0)
        for replica_index in range(params_data.shape[1]):  # Iterate over 30 replicas
            # Apply Gaussian KDE to each replica
            kde = gaussian_kde(params_data[0, replica_index], bw_method='scott')
            x_values = np.linspace(0, 100, 500)  # Percentage scale
            kde_values = kde(x_values)

            # Plot the smoothed line for each replica
            ax.plot(x_values, kde_values, color=colors[replica_index], alpha=0.8, label=f'Replica {replica_index+1}')

        ax.set_xlim(0, 110)
        ax.set_ylim(0, 0.31)
        ax.set_xticks(np.arange(0, 110, 20))
        ax.set_yticks(np.arange(0, 0.31, 0.15))
        ax.tick_params(axis='both', which='major', labelsize=30)
        # Set the linewidth of the entire border
        for side in ['top', 'bottom', 'left', 'right']:
            ax.spines[side].set(lw=3.0)
        #ax.set_title(f'Dataset {i+1}', fontsize=14)
        #ax.grid(True, linestyle='--', alpha=0.6)

        ax.tick_params(which='both', size=12, width=5, direction='out')
    # Common X and Y labels
#    fig.text(0.5, 0.04, 'Restraints Enforced (%)', ha='center', fontsize=20)
#    fig.text(0.04, 0.5, 'Density', va='center', rotation='vertical', fontsize=20)

    # Collect handles and labels for the common legend
#        all_handles.extend(handles)
#        all_labels.extend(labels)
    # Create a common legend outside the plots
    #handles, labels = axes[0].get_legend_handles_labels()
    #fig.legend(all_handles, all_labels, loc='upper right', bbox_to_anchor=(0.98, 1), fontsize=20, ncol=1)

    plt.tight_layout()
    plt.savefig('combined_histogram_distributions.png', dpi=300)
    plt.show()

# Paths to the 6 files you want to plot
files = [
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.25/3GB1/parameters.npy',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.5/3GB1/parameters.npy',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/1.0/3GB1/parameters.npy',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/2.0/3GB1/parameters.npy',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/4.0/3GB1/parameters.npy',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/8.0/3GB1/parameters.npy',
]

visualize_multiple_parameters(files)

