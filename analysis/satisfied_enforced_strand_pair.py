import numpy as np
import matplotlib.pyplot as plt

a=np.loadtxt('dummy_strand.dat')
max_val = 177
params_strand = (a / max_val) * 100
np.save('no_ps_percentage_strand.npy',params_strand)

def make_subplots():
    files_satisfied = [
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/no_ps/3GB1/analysis/satisfied_peak_strand.dat',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.25/3GB1/analysis/satisfied_peak_strand.dat',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/0.5/3GB1/analysis/satisfied_peak_strand.dat',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/1.0/3GB1/analysis/satisfied_peak_strand.dat',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/2.0/3GB1/analysis/satisfied_peak_strand.dat',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/4.0/3GB1/analysis/satisfied_peak_strand.dat',
        '/orange/alberto.perezant/bhumika/PARAMETER_SAMPLING/8.0/3GB1/analysis/satisfied_peak_strand.dat'
    ]

    files_enforced = [
        'no_ps_percentage_strand.npy',
        '0.25_params_strand.npy',
        '0.5_params_strand.npy',
        '1.0_params_strand.npy',
        '2.0_params_strand.npy',
        '4.0_params_strand.npy',
        '8.0_params_strand.npy'
    ]

    # Create a figure and subplots with square dimensions
    fig, axes = plt.subplots(len(files_satisfied), 1, figsize=(9, 7 * len(files_satisfied)), sharex=True)


    # Plot individual histograms for each dataset
    for i in range(len(files_satisfied)):
        #for file1, file2 in zip(files_satisfied, files_enforced):
            #print(file1,file2)
        ax = axes[i]

        # Load data from file
        y_sat = np.loadtxt(files_satisfied[i])
        y_en = np.load(files_enforced[i])

        # Calculate the max value from the loaded data
        max_val = 177

        constant = (8 / max_val) * 100
        ax.vlines(constant, ymin=0, ymax=19000, linestyle='--', color='black', linewidth=3.0)
        
        ## FOR SATISFIED
        # Calculate the percentage
        y_percentage = (y_sat / max_val) * 100
        #ax.hist(y_percentage, bins=20, color='#2E86C1', histtype='bar', rwidth=100.0)
        ax.hist(y_percentage, bins=int(y_sat.max()-y_sat.min()),alpha=1.0, color='#EC7063', histtype='bar', rwidth=100.0)
        #ax.hist(y_percentage, bins=20,alpha=1.0, color='#EC7063', histtype='bar', rwidth=100.0)
            #ax.hist(y_percentage, bins=20, color='#2E86C1', histtype='bar', rwidth=100.0)

        ## FOR ENFORCED 
        print(y_en.min(),y_en.max())
        ax.hist(y_en, bins=int(1+y_en.max()-y_en.min()), alpha=1.0, color='#2E86C1', histtype='bar', rwidth=100.0)
        #ax.hist(y_en, bins=20, alpha=1.0, color='#2E86C1', histtype='bar', rwidth=100.0)
        #ax.hist(y, bins=100, alpha=1.0, density=False, color = '#2E86C1')


        ax.set_xlim(0, 115)  # Adjust x-axis limit to accommodate percentages
        ax.set_ylim(0, 19000)
        ax.set_xticks(np.arange(0, 110, 20))
        ax.tick_params(axis='both', which='major', labelsize=30)
        ax.set_yticks(np.arange(0, 19000, 5000))

        ylabels = ['{:,}'.format(int(y/1000)) for y in ax.get_yticks()]
        ax.set_yticklabels(ylabels)

        # Increase the size of dashes for both major and minor ticks of the x and y axes
        ax.tick_params(which='both', size=12, width=5, direction='out')

        # Set the linewidth of the entire border
        for side in ['top', 'bottom', 'left', 'right']:
            ax.spines[side].set(lw=3.0)

        # Remove x-axis labels for all but the last row
        if i < len(files_satisfied) - 1:
            ax.set_xticklabels([])

        # Make tick labels bold
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_weight("bold")

        # Add x-axis label to the last row
        if i == len(files_satisfied) - 1:
            ax.set_xticklabels(np.arange(0, 110, 20), size=30, weight='bold')  # Add this line to show x-axis tick labels

    # Add tight layout
    plt.tight_layout()

    # Save the figure
    plt.savefig('test_subplots_strand.pdf', dpi=320)
    plt.show()

make_subplots()
