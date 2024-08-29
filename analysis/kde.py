import numpy as np
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
import os

# Function to plot rmsd for every protein
def rmsd_plot(a):
    kde_30 = []
    t = np.linspace(0, 20, 1000)  # Define 't' here

    # Load the data for each replica
    for index in range(30):
        data = np.loadtxt(a + "rmsd_" + str(index) + ".dat")[:, 1]
        data_2 = np.reshape(data, (len(data), 1))

        # Kernel density estimation, bandwidth defines the fit of the curve
        kde = KernelDensity(bandwidth=0.2, kernel='gaussian').fit(data_2)

        # Evaluate the KDE on the given range
        kde_dens = np.exp(kde.score_samples(t[:, None])) * 100
        kde_30.append(kde_dens)

    return kde_30, t

# List of dataset paths
dataset_paths = [
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/no_ps/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.25/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.5/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/1.0/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/2.0/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/4.0/3GB1/walkers/',
    '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/8.0/3GB1/walkers/'
]

for i, path in enumerate(dataset_paths):
    kde_data, t = rmsd_plot(path)
    np.save(f'kde_data_dataset_{i + 1}.npy', kde_data)
    np.save(f't_values_dataset_{i + 1}.npy', t)

