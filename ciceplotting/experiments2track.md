#End of Internship

The most up-to-date experiments are in three main folders:

1. ```/home/fsd001/data/ppp8/cice/runs/gx1IMEX/history```
2. ```/home/fsd001/data/ppp8/cice/runs/INSTAhpcBOX/history```
3. ```/home/fsd001/data/ppp8/cice/runs/INSTAhpcLISLAND/history```

They were run with ppp8 and they were done with the last version of IMEX. 
Those experiments are mostly sensititivy experiments. The time step was varied for 
a set of given parameters between experiments and its effect on the instabilities 
was observed (with and without IMEX). 

For the idealised experiments, the naming convention if the following:

- GridTimeStepIcestrengthRheology

So, an experiment will look like: ```B1hrk1VP-IMEX```

Most of the idealised experiments were run for one day so, in their respective directory, only
one file will be in it ```iceh.2005-01-02.nc```


There is really one set of gx1 experiments that are worth to look at now. The naming convention for the 
global experiments is quite different:

- Grid-ItsnonlinItsFGMRESItsPGMRES-Ice Strength-Time step

So, an experiment will like:

- B-N10F50P20-k0-3hr 

Inside of the directory will be monthly state files for the given number of years the experiment was run. 


# Experiments - gx1 
This is the list of experiments made with CICE to test IMEX and the newly 
implemented preconditionners. 


## Experiments with Pstar = 27.5e3 
Those are the right experiments with the right Pstar. They all use the Hibler parametrization:
$$
P = P^*h e^{-C(1-A)}
$$

Now, a couple of bugs with IMEX were fixed. 

### For one year with dt = 2hr:
The data is in ```/home/fsd001/data/ppp7/cice/runs/gx1IMEX/history```
- N10F50T1e-4P10Asym2hr_year


### For one year with dt = 1hr:
- N10F50T1e-4P10AsymIMEX_year (Done with old bug)
- N10F50T1e-4P10Asym_year

In this experiment, the instability is not present in the experiment without IMEX. The timestep will be increased in the next experiment to find out if the instability comes out. 


### For one month with dt = 1hr:
- N10F50P20diag_month: pgmres with diag
- N10F50P20Asym_month: pgmres with asym
- N10F50Bi20Asym_month: BiCGSTAB with asym
- N10F50P20DiagIMEX_month: pgmres with diag and IMEX
- N10F50P20AsymIMEX_month: pgmres with asym and IMEX


## Experiments with Pstar = 27.5e4
Those experiments are the ones we want to analyse since the ice does not 
move all because of the very high maximal compressive strength. 

### For one time step with dt = 1hr
- N30F50P20IDT
- N30F50P20Diag
- N30F50P20Asym
- N30F50Bi20Asym

### For one day with dt = 1hr
- N30F50P20IDT_Day,
- N30F50P20Diag_Day
- N30F50P20Asym_Day
- N30F50P20AsymIMEX_Day


