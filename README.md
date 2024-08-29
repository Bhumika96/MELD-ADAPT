
Step0. Prerequisites
--------------------
version: MELD-0.6.1

Step1: Setting the setup script for MELD-Adapt
-----------------------------------------------

```setup_meld_adapt.py``` is a python script which is creates the platform of the simulation we are going to carry out. 
With this create the restraint files ```hydrophobe.dat``` and ```strand_pair.dat```, generate the initial states for 
each replica at different temperature and hamiltonial (force constant/ restraint strength), and setup the hyperparameters: reward (u0) and 
initial prior (starting belief). Finally launch OpenMM jobs associated with replica exchange protocol.

**Required input files**

```sequence.dat``` : contains the amino acid sequence of the target protein
```ss.dat```       : the secondary structure predictions of the protein. In the given file H represents Helix, E: strand, .:coil
```minimized_protein.pdb``` in the /TEMPLATES directory #starting structure


```
#creates parameter for sampling for hydrophobic contacts
    dists = get_dist_restraints_hydrophobe('hydrophobe.dat', s, scaler, ramp, seq)
    prior_hydrophobic = param_sampling.ScaledExponentialDiscretePrior(u0=1.0, temperature_scaler=s.temperature_scaler, scaler=scaler)
    sampler_hydrophobic = param_sampling.DiscreteSampler(int(1), int(1.00 * len(dists)), 1)
    param_hydrophobic = s.param_sampler.add_discrete_parameter("param_HP", int(1.2 * no_hy_res), prior_hydrophobic, sampler_hydrophobic)
    s.restraints.add_selectively_active_collection(dists, param_hydrophobic)
    
    
    #creates parameter sampling for strand pairing
    dists = get_dist_restraints_strand_pair('strand_pair.dat', s, scaler, ramp, seq)
    prior_strand = param_sampling.ScaledExponentialDiscretePrior(u0=1.0, temperature_scaler=s.temperature_scaler, scaler=scaler)
    sampler_strand = param_sampling.DiscreteSampler(int(1), int(1.00 * len(dists)), 1)
    param_strand = s.param_sampler.add_discrete_parameter("param_SP", int(0.45*active), prior_strand, sampler_strand)
    s.restraints.add_selectively_active_collection(dists, param_strand)
```

