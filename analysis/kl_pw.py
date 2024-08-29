import numpy as np
import matplotlib.pyplot as plt
from scipy.special import rel_entr

def make_subplots():
    files = [
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/1.0/3GB1/walkers/',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.25/3GB1/walkers/',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.5/3GB1/walkers/',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/1.0/3GB1/walkers/',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/2.0/3GB1/walkers/',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/4.0/3GB1/walkers/',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/8.0/3GB1/walkers/'
    ]

    # Create a figure and subplots with square dimensions
    fig, axes = plt.subplots(len(files), 1, figsize=(9, 7 * len(files)), sharex=True)


    epsilon = 0.001  # Small constant to avoid division by zero

    for i, file_path in enumerate(files):
        ax=axes[i]
        print(f"Dataset {i+1}:")
        # Create a list to store all KL divergences
        avg_kl_divergences = []
        std_kl_divergences = []

        # Load data for all replicas
        data_replicas = []
        for index in range(30):
            data_replica = np.loadtxt(file_path + "rmsd_" + str(index) + ".dat")[:, 1]
            data_replicas.append(data_replica)

        # Calculate and normalize histograms for all replicas
        histograms_normalized = []
        for data_replica in data_replicas:
            hist, bins = np.histogram(data_replica, bins=100, range=(np.min(data_replica), np.max(data_replica)), density=True)
            # Normalize the histogram by adding epsilon and dividing by the sum of the counts
            hist_normalized = (hist + epsilon) / (np.sum(hist) + epsilon * len(hist))
            histograms_normalized.append(hist_normalized)

        # Calculate KL divergences and gather average and standard deviation
        print(f"KL Divergences for dataset {i + 1}:")
        
        for index1 in range(30):
            kl_divergences = []
            for index2 in range(30):
                if index1 != index2:
                    # Calculate KL divergence between replica index1 and replica index2
                    kl_divergence = np.sum(rel_entr(histograms_normalized[index2], histograms_normalized[index1]))
                    kl_divergences.append(kl_divergence)

           # Calculate the average and standard deviation of KL divergences for index1
            avg_kl_divergence = np.mean(kl_divergences)
            std_kl_divergence = np.std(kl_divergences)
            
            # Normalize KL divergences and standard deviations to be between 0 and 1
            max_kl_divergence = np.max(kl_divergences)  # Calculate max of KL divergences
            if max_kl_divergence > 0:  # Avoid division by zero
                avg_kl_divergence = avg_kl_divergence / max_kl_divergence
                std_kl_divergence = std_kl_divergence / max_kl_divergence
            
            avg_kl_divergences.append(avg_kl_divergence)
            std_kl_divergences.append(std_kl_divergence)            
            print(f"Average KL Divergence for replica {index1}: {avg_kl_divergence}")
            print(f"Standard deviation for replica {index1}: {std_kl_divergence}\n")


       # Plot the average KL divergences and standard deviation with a smooth shaded area
        replica_indices = np.arange(1, 31)
        # Plot the average normalized KL divergence for the current dataset
        ax.plot(replica_indices, avg_kl_divergences, marker='o', linestyle='-', color = '#2E86C1')
        #ax.hlines(y=1, xmin=0, xmax=33, linestyle='--', color='black', linewidth=5.0)

        # Add shaded area for the standard deviation
        ax.fill_between(replica_indices,
                         np.array(avg_kl_divergences) - np.array(std_kl_divergences),
                         np.array(avg_kl_divergences) + np.array(std_kl_divergences),
                         color='#2E86C1', alpha=0.3, linestyle ='--')


        ax.set_xlim(0, 32)
        ax.set_ylim(0.0, 1.2)
        ax.set_xticks(np.arange(0, 32, 5))
        ax.tick_params(axis='both', which='major', labelsize=30)
        ax.set_yticks(np.arange(0.0, 1.2, 0.5))

        # Increase the size of dashes for both major and minor ticks of the x and y axes
        ax.tick_params(which='both', size=12, width=5, direction='out')

        # Set the linewidth of the entire border
        for side in ['top', 'bottom', 'left', 'right']:
            ax.spines[side].set(lw=3.0)

        # Remove x-axis labels for all but the last row
        if i < len(files) - 1:
            ax.set_xticklabels([])

        # Make tick labels bold
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_weight("bold")

        # Add x-axis label to the last row
        if i == len(files) - 1:
            ax.set_xticklabels(np.arange(0, 35, 5), size=30, weight='bold')  # Add this line to show x-axis tick labels


    # Add tight layout
    plt.tight_layout()

    # Show the plot
    plt.savefig("kl_pw_hist_stacked.pdf", dpi=320)
    plt.savefig("kl_pw_hist_stacked.png", dpi=320)
    plt.show()

make_subplots()

