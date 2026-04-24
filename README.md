# CICE-Analysis

A Python toolkit for testing new implementations and analysing outputs from the CICE sea ice model.

## Project Structure

| Directory | Description |
|---|---|
| `ciceplotting/` | Main package — reads model outputs and generates figures |
| `CICE-UTILS/` | Saved `ice_in` configuration files for running experiments |
| `Figures/` | Generated figures, organised by case |
| `Fortran/` | Lightweight Fortran scripts for prototyping |
| `Numerics/` | Sparse matrix solver implementations |
| `Rheology/` | Free drift solver implementations and VP stress plotting routines |

## Core Package: `ciceplotting`

The `ciceplotting` package is the heart of this project. It provides everything needed to read NetCDF output files and `cice.runlog` to produce figures. It supports both **idealised** and **global** experiments.


# How to Use `ciceplotting`

## 1. Set Up the Environment

Install the conda environment using the provided `cice-env.yml` file:

```bash
conda env create -f cice-env.yml
```

## 2. Configure the Namelist

Edit the appropriate namelist file to match your experiment:

| Experiment Type | Namelist File |
|---|---|
| Global | `namelist` |
| Idealised | `namelist_ideal` |

Both files share the same structure. Two separate namelists are maintained for convenience, to avoid repeatedly switching the same file back and forth.

The namelists are organised as follows:

###`[Experiments]`

| Parameter | Description |
|---|---|
| `exp` | Experiment name |
| `case` | Case name — determines the subdirectory in `Figures/` where figures are saved |
| `plot_fields` | `1` or `0` — plot ice area and thickness fields *(deprecated)* |
| `read_all` | `1` or `0` — read `cice.runlog` |
| `plot_single` | Plot a transect *(deprecated)* |

### `[Dynamics]`

| Parameter | Description |
|---|---|
| `kstrength` | Ice strength parameterisation used |
| `gridtype` | Grid type used |
| `var` | NetCDF file prefix to analyse (typically `iceh` or `iceh_inst`) |
| `dx` | Horizontal resolution |

### `[Numerical]`

| Parameter | Description |
|---|---|
| `solver` | Solver used during the run (typically `fgmres`) |
| `imex` | `1` or `0` |
| `global` | `1` or `0` |
| `precond` | Preconditioner used during the run |

###`[Figures]`

| Parameter | Description |
|---|---|
| `datadir` | Path to the input data directory |
| `figdir` | Path to the output figures directory |
| `labels` | Experiment label as it appears in figures |

### `[Time]`

| Parameter | Description |
|---|---|
| `dt` | Time step |
| `datestr` | Date to analyse |
| `startdate` | Start date for reading data |
| `enddate` | End date for reading data |
| `freq` | Output frequency |


If you want to read multiple experiments at the same time, you just need to provide multiple experiment names, solvers, preconditionners
and labels. As long as they are located in the same directory and have the same outputs, the code will read and plot them all on the same figures. 
You might need to tweak the legend placement manually. 

## 3. Running the analysis

To run the package, you need to use the following command:
```
python cice_analysis.py -c 'ideal or gx'
```

ideal is for idealised experiments while gx is for global. 


### Scripts

In the ciceplotting directory, there is also an unused (directly by cice_analsysis) folder 
but which contains useful bash scripts when using cice.


### Architecture 
```
- ciceplotting/
        - cice_analysis.py
        - namelists
        - setup.py
        - ciceplotting/
                - data/
                        - readdata.py
			- readnamelist.py 
		- plotting/
			- plot_cice.py
			- science.mplstyle 
		- scritps/
			- rename_files.sh 
			- run_segments.sh 
		- utils/
			- manip_arrays.py 
			- TimeUtilities.py 
```
