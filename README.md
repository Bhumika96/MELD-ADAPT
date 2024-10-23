
Prerequisites
--------------------
version: [MELD-0.6.1](https://github.com/maccallumlab/meld)

[My Image](image.png)

Fot the pupose of the tutorial, we have explained how to run MELD-Adapt as well as MELD. We have taken example of folding of Protein G (PDB ID: 3GB1) starting from the sequence of the protein. We have used Coarse Physical Insights (CPIs) to generate the ambiguous data [ref](https://doi.org/10.1073/pnas.1506788112).

Setting the setup script for MELD-Adapt
-----------------------------------------------

```setup_meld_adapt.py``` is a python script which creates the platform for the simulation using MELD-Adapt.
This script creates the restraint files ```hydrophobe.dat``` and ```strand_pair.dat``` as well as generate the initial states for 
each replica at different temperature and hamiltonian (force constant/ restraint strength). The same script is used to input the values of the hyperparameters: reward (u0) and initial prior (starting belief). Finally launch OpenMM jobs associated with replica exchange protocol.

**Required input files**

```sequence.dat``` : contains the amino acid sequence of the target protein

```ss.dat```       : the secondary structure predictions of the protein. In the given file *H* represents Helix, *E* represents strand, *.* represents coil.

```minimized_protein.pdb``` in the /TEMPLATES directory #starting structure from sequence after minimizing in AMBER.

**Setting the choices for the simulations**

We can set the choice of forcefield ```forcefield="ff14sbside"```, solvent model ```implicit_solvent_model = 'gbNeck2'```, 
time step ```use_big_timestep = True``` *(here, 3.5fs)*.

Since Hamiltonian, Temperature Replica Exchange Molecular Dynamics (H,T-REMD) is employed. The temperature can also be varied along the replica ladder. The Hamiltonian for restraints varies from parameter to parameter. 

Temperature ```s.temperature_scaler = meld.GeometricTemperatureScaler(0, 0.3, 300.*u.kelvin, 450.*u.kelvin)``` *(Here, temperature goes from 300K-450K)*

```
def setup_system():
    
    # load the sequence
    sequence = parse.get_sequence_from_AA1(filename='sequence.dat')
    n_res = len(sequence.split())

    # build the system
    p = meld.AmberSubSystemFromPdbFile('TEMPLATES/peptide_min.pdb')
    build_options = meld.AmberOptions(
      forcefield="ff14sbside",
      implicit_solvent_model = 'gbNeck2',
      use_big_timestep = True,
      cutoff = 1.8*u.nanometers,
      remove_com = False,
      #use_amap = False,
      enable_amap = False,
      amap_beta_bias = 1.0,
    )


    builder = meld.AmberSystemBuilder(build_options)
    s = builder.build_system([p]).finalize()
    #s.temperature_scaler = meld.ConstantTemperatureScaler(300.0 * u.kelvin)
    s.temperature_scaler = meld.GeometricTemperatureScaler(0, 0.3, 300.*u.kelvin, 450.*u.kelvin)
```

**How to set up reward value ($\lambda$) and initial prior**

In the code the reward is given by u0. As shown in the given snippet, the reward (u0) is 1.0.
For sampling of hydrophobic contact based restraints: the initial prior is 1.2.

```
from meld.system import param_sampling

#creates parameter for sampling for hydrophobic contacts
    dists = get_dist_restraints_hydrophobe('hydrophobe.dat', s, scaler, ramp, seq)
    prior_hydrophobic = param_sampling.ScaledExponentialDiscretePrior(u0=1.0, temperature_scaler=s.temperature_scaler, scaler=scaler)
    sampler_hydrophobic = param_sampling.DiscreteSampler(int(1), int(1.00 * len(dists)), 1)
    param_hydrophobic = s.param_sampler.add_discrete_parameter("param_HP", int(1.2 * no_hy_res), prior_hydrophobic, sampler_hydrophobic)
    s.restraints.add_selectively_active_collection(dists, param_hydrophobic)
```

Line 4: Creates a prior that favors higher values with $-1K_B T$ energy contribution for each unit of increase in the parameter.

Line 5: Creates a sampler with a minimum value of 1 and a maximum value of length of total dists *(calculated in line 3)*, both inclusive. It uses a step size of 1, so that random moves are attemped from the current value.

Line 6: Creates the parameter. Each parameter must have a unique name, "param_hydrophobic" in this case. We must also specify the initial value, here int(1.2 * no_hy_res). The resulting object, param_hydrophobic, can then be passed to other places in the MELD code base. Currently this can only be used as num_active when creating a group or collection.   

Similarly, we can add more parameters such as strand pair based restraints.
Here: 
The reward (u0) is 1.0.
For sampling of strand pair contact based restraints: the initial prior is 0.45.
```
#creates parameter sampling for strand pairing
    dists = get_dist_restraints_strand_pair('strand_pair.dat', s, scaler, ramp, seq)
    prior_strand = param_sampling.ScaledExponentialDiscretePrior(**u0=1.0**, temperature_scaler=s.temperature_scaler, scaler=scaler)
    sampler_strand = param_sampling.DiscreteSampler(int(1), int(1.00 * len(dists)), 1)
    param_strand = s.param_sampler.add_discrete_parameter("param_SP", int(0.45 * active), prior_strand, sampler_strand)
    s.restraints.add_selectively_active_collection(dists, param_strand)
```

After each round of molecular dynamics steps, the parameters are updated using a series of Monte Carlo trials. The number of trials is controlled by the ```param_mcmc_steps``` option of the RunOption object.

```
 # create the options
    options = meld.RunOptions(
        timesteps = 14286,
        minimize_steps = 20000,
        min_mc = sched,
        param_mcmc_steps=200
    )
```

Setting the setup script for MELD
----------------------------------

In case the user wants to fix the amount of data to trust throughout the simulations. ```setup_meld.py``` is a python script which creates the platform for the simulation using MELD. The following should be made to fix the amount of hydrophobe contacts as shown in the code snippet. *Note we no longer need to define prior_hydrophobic, sampler_hydrophobic, param_hydrophobic.*

```
#fixed restraints based on hydrophobic contacts
    dists = get_dist_restraints_hydrophobe('hydrophobe.dat', s, scaler, ramp, seq)
    #prior_hydrophobic = param_sampling.ScaledExponentialDiscretePrior(u0=1.0, temperature_scaler=s.temperature_scaler, scaler=scaler)
    #sampler_hydrophobic = param_sampling.DiscreteSampler(int(1), int(1.00 * len(dists)), 1)
    #param_hydrophobic = s.param_sampler.add_discrete_parameter("param_HP", int(1.2 * no_hy_res), prior_hydrophobic, sampler_hydrophobic)
    #s.restraints.add_selectively_active_collection(dists, param_hydrophobic)
    s.restraints.add_selectively_active_collection(dists, int(1.2 * no_hy_res))   
```
Similarly, we can fix the strand pair contacts.
```
#fixed restraints based on strand pairing
    dists = get_dist_restraints_strand_pair('strand_pair.dat', s, scaler, ramp, seq)
    #prior_strand = param_sampling.ScaledExponentialDiscretePrior(u0=1.0, temperature_scaler=s.temperature_scaler, scaler=scaler)
    #sampler_strand = param_sampling.DiscreteSampler(int(1), int(1.00 * len(dists)), 1)
    #param_strand = s.param_sampler.add_discrete_parameter("param_SP", int(0.45*active), prior_strand, sampler_strand)
    #s.restraints.add_selectively_active_collection(dists, param_strand)
    s.restraints.add_selectively_active_collection(dists, int(0.45*active))
```

Processing the trajectories
----------------------------
use ```extract_trajectories_walkers.sh``` to extract trajectories and walkers for further analysis.

For more detailed understanding of MELD-Adapt
-----------------------------------------------------------------------
1) [Bayesian Sampling of Parameters](http://meldmd.org/explain/param_sampling.html#parameter-sampling-background)
2) [How to use parameter sampling](http://meldmd.org/how_to/parameter_sampling.html)
3) MELD-Adapt: On-the-Fly Belief Updating in Integrative Molecular Dynamics [link](https://www.biorxiv.org/content/10.1101/2024.05.21.595263v1)




