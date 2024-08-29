
Step0. Prerequisites
--------------------
version: MELD-0.6.1

Step1: Setting the setup script for MELD-Adapt
-----------------------------------------------

```setup_meld_adapt.py``` is a python script which is creates the platform for the simulation using MELD-Adapt.
This script creates the restraint files ```hydrophobe.dat``` and ```strand_pair.dat``` as well as generate the initial states for 
each replica at different temperature and hamiltonian (force constant/ restraint strength). The same script is used to input the values of the hyperparameters: reward (u0) and initial prior (starting belief). Finally launch OpenMM jobs associated with replica exchange protocol.

**Required input files**

```sequence.dat``` : contains the amino acid sequence of the target protein

```ss.dat```       : the secondary structure predictions of the protein. In the given file *H* represents Helix, *E* represents strand, *.* represents coil.

```minimized_protein.pdb``` in the /TEMPLATES directory #starting structure

**How to set up reward value ($\lambda$) and initial prior**

In the code the reward is given by u0. As shown in the given snippet, the reward (u0) is 1.0.
For sampling of hydrophobic contact based restraints: the initial prior is 1.2.


prior = param_sampling.DiscreteExponentialPrior(k=1.0)
sampler = param_sampling.DiscreteSampler(50, 100, 5)
param = system.param_sampler.add_discrete_parameter("param", 75, prior, sampler)

```
from meld.system import param_sampling

#creates parameter for sampling for hydrophobic contacts
    dists = get_dist_restraints_hydrophobe('hydrophobe.dat', s, scaler, ramp, seq)
    prior_hydrophobic = param_sampling.ScaledExponentialDiscretePrior(u0=1.0, temperature_scaler=s.temperature_scaler, scaler=scaler)
    sampler_hydrophobic = param_sampling.DiscreteSampler(int(1), int(1.00 * len(dists)), 1)
    param_hydrophobic = s.param_sampler.add_discrete_parameter("param_HP", int(1.2 * no_hy_res), prior_hydrophobic, sampler_hydrophobic)
    s.restraints.add_selectively_active_collection(dists, param_hydrophobic)
```

Line 4: Creates a prior that favors higher values with energy contribution for each unit of increase in the parameter.

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






