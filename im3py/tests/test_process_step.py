"""Tests for process_step.py functionality.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os
import pkg_resources
import unittest

from im3py.read_config import ReadConfig
from im3py.process_step import ProcessStep


class TestProcessStep(unittest.TestCase):
    """Tests for the `ReadConfig` class that reads the input configuration from the user."""

    # test config YAML file
    CONFIG_YAML = pkg_resources.resource_filename('im3py', 'tests/data/inputs/config.yml')

    # expected attribute values
    OUTPUT_DIR = pkg_resources.resource_filename('im3py', 'tests/data/outputs')
    START_YEAR = 2015
    THROUGH_YEAR = 2016
    TIME_STEP = 1
    ALPHA_URBAN = 2.0
    ALPHA_RURAL = 0.08
    BETA_URBAN = 1.78
    BETA_RURAL = 1.42

    @classmethod
    def create_output_directory(cls):
        """Create directory if it does not exist."""

        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)

    def test_instantiation(self):
        """Test model instantiation."""

        # create output directory if it does not exist
        self.create_output_directory()

        # read configuration from parameters
        cfg = ReadConfig(output_directory=TestProcessStep.OUTPUT_DIR,
                         start_year=TestProcessStep.START_YEAR,
                         through_year=TestProcessStep.THROUGH_YEAR,
                         time_step=TestProcessStep.TIME_STEP,
                         alpha_urban=TestProcessStep.ALPHA_URBAN,
                         alpha_rural=TestProcessStep.ALPHA_RURAL,
                         beta_urban=TestProcessStep.BETA_URBAN,
                         beta_rural=TestProcessStep.BETA_RURAL)

        # instantiate class for the start year
        step = ProcessStep(cfg,
                           TestProcessStep.START_YEAR,
                           TestProcessStep.ALPHA_URBAN,
                           TestProcessStep.BETA_URBAN,
                           TestProcessStep.ALPHA_RURAL,
                           TestProcessStep.BETA_RURAL)


if __name__ == '__main__':
    unittest.main()
