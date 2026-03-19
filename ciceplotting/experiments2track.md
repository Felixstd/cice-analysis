# Experiments with Pstar = 27.5e3 
Those are the right experiments with the right Pstar. They all use the Hibler parametrization:
$$
P = P^*h e^{-C(1-A)}
$$

# For one month with dt = 1hr:
- N10F50P20diag_month: pgmres with diag
- N10F50P20Asym_month: pgmres with asym
- N10F50Bi20Asym_month: BiCGSTAB with asym
- N10F50P20DiagIMEX_month: pgmres with diag and IMEX
- N10F50P20AsymIMEX_month: pgmres with asym and IMEX

# Experiments with Pstar = 27.5e4
Those experiments are the ones we want to analyse since the ice does not 
move all because of the very high maximal compressive strength. 

## For one time step with dt = 1hr
- N30F50P20IDT
- N30F50P20Diag
- N30F50P20Asym
- N30F50Bi20Asym

## For one day with dt = 1hr
- N30F50P20IDT_Day,
- N30F50P20Diag_Day
- N30F50P20Asym_Day
- N30F50P20AsymIMEX_Day

## For one month with dt = 1hr

