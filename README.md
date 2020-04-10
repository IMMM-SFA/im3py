[![Build Status](https://travis-ci.org/IMMM-SFA/im3py.svg?branch=master)](https://travis-ci.org/IMMM-SFA/im3py) [![codecov](https://codecov.io/gh/IMMM-SFA/im3py/branch/master/graph/badge.svg)](https://codecov.io/gh/IMMM-SFA/im3py)

# im3py
An IM3 template repository for Python projects that have time-steps


## Overview
The purpose of `im3py` is to help quickly establish a GitHub repository that conforms to IM3 software engineering standards.  Our hope is to create a common user experience for all Python modeling software developed for use in IM3 experiments.  We are mindfully developing software that exposes key variables per time-step that may be used in integrated and/or uncertainty characterization experiments while still maintaining the ability for autonomous use.  This template package establishes the structure necessary to wrap existing Python code in our modeling interface and time-step processing generator.  We also include:  a sample test suite, Travis-CI and codecov standards files, our expected docstring style, a stdout and file logger, and an example fake code file that represents a user's code.

## Getting Started
The `im3py` package uses only **Python 3.3** and up.

### Step 1:
You can install `im3py` by running the following from your cloned directory (NOTE: ensure that you are using the desired `pip` instance that matches your Python3 distribution):

`pip3 install git+https://github.com/IMMM-SFA/im3py.git --user`

### Step 2:
Confirm that the module and its dependencies have been installed by running from your prompt:

```python
from im3py import Model
```

If no error is returned then you are ready to go!

## Setting up a run

### Expected arguments
See examples below for how to pass into the `Model` class

| Argument | Type | Description |
|----|----|----|
| `config_file` | str | Full path to configuration YAML file with file name and extension. If not provided by the user, the code will default to the expectation of alternate arguments. |
| `output_directory` | string | Full path with file name and extension to the output directory where outputs and the log file will be written. |
| `start_year` | int | Four digit first year to process for the projection. |
| `through_year` | int | Four digit last year to process for the projection. |
| `time_step` | int | Number of steps (e.g. number of years between projections) |
| `alpha_urban` | float | Alpha parameter for urban. Represents the degree to which the population size of surrounding cells translates into the suitability of a focal cell.,A positive value indicates that the larger the population that is located within the 100 km neighborhood, the more suitable the focal cell is.,More negative value implies less suitable. Acceptable range:,-2.0 to 2.0 |
| `beta_urban` | float | Beta parameter for urban. Reflects the significance of distance to surrounding cells on the suitability of a focal cell.,Within 100 km, beta determines how distance modifies the effect on suitability. Acceptable range:,-2.0 to 2.0 |
| `alpha_rural` | float | Alpha parameter for rural. Represents the degree to which the population size of surrounding cells translates into the suitability of a focal cell.,A positive value indicates that the larger the population that is located within the 100 km neighborhood, the more suitable the focal cell is.,More negative value implies less suitable. Acceptable range:,-2.0 to 2.0 |
| `beta_rural` | float | Beta parameter for rural. Reflects the significance of distance to surrounding cells on the suitability of a focal cell.,Within 100 km, beta determines how distance modifies the effect on suitability. Acceptable range:,-2.0 to 2.0 |

### Variable arguments
Users can update variable argument values after model initialization; this includes updating values between time steps (see **Example 3**).  The following are variable arguments:
- `alpha_urban`
- `beta_urban`
- `alpha_rural`
- `beta_rural`

### YAML configuration file option (e.g., config.yml)
Arguments can be passed into the `Model` class using a YAML configuration file as well (see **Example 1**):

```yaml
# Example configuration file setup
output_directory:  "<Full path to the output directory>"
start_year: 2015
through_year: 2020
time_step: 1
alpha_urban: 2.0
alpha_rural: 0.08
beta_urban: 1.78
beta_rural: 1.42
```

### Expected outputs
Each time-step processed will generate a TEXT file containing a solution message and have the file name formatted as `output_year_<YYYY>.txt`. These will be written to where the `output_directory` has been assigned.

## Examples

### Example 1:  Run `im3py` for all years using a configuration file
```python
from im3py.model import Model

run = Model(config_file="<path to your config file with the file name and extension.")

run.run_all_steps()
```

### Example 2:  Run `im3py` for all years by passing argument values
```python
from im3py.model import Model

run = Model(output_directory="<output directory path>",
            start_year=2015,
            through_year=2030,
            time_step=1,
            alpha_urban= 2.0,
            alpha_rural=0.08,
            beta_urban=1.78,
            beta_rural=1.42)

run.run_all_steps()
```

### Example 3:  Run `im3py` by year by passing argument values; update value in between time step
```python
from im3py.model import Model

run = Model(output_directory="<output directory path>",
            start_year=2015,
            through_year=2030,
            time_step=1,
            alpha_urban= 2.0,
            alpha_rural=0.08,
            beta_urban=1.78,
            beta_rural=1.42)

# initialize model
run.initialize()

# downscale year 0
run.advance_step()

# modify the calibrated alpha parameter value for urban
run.alpha_urban = -0.1

# run next step with modified parameters
run.advance_step()

# close out run
run.close()
```
