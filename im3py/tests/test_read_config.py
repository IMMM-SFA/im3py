"""Tests for the configuration reader functionality.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import pkg_resources
import unittest

from im3py.read_config import ReadConfig


class TestReadConfig(unittest.TestCase):
    """Tests for the `ReadConfig` class that reads the input configuration from the user."""

    # test config YAML file
    CONFIG_YAML = pkg_resources.resource_filename('im3py', 'tests/data/inputs/config.yml')

    # expected attribute values
    OUTPUT_DIR = pkg_resources.resource_filename('im3py', "tests/data/outputs")
    START_YEAR = 2015
    THROUGH_YEAR = 2020
    TIME_STEP = 1
    ALPHA_URBAN = 2.0
    ALPHA_RURAL = 0.08
    BETA_URBAN = 1.78
    BETA_RURAL = 1.42

    # expected attribute types
    OUTPUT_DIR_TYPE = str
    START_YEAR_TYPE = int
    THROUGH_YEAR_TYPE = int
    TIME_STEP_TYPE = int
    ALPHA_URBAN_TYPE = float
    ALPHA_RURAL_TYPE = float
    BETA_URBAN_TYPE = float
    BETA_RURAL_TYPE = float

    def test_instance_attributes_config(self):
        """Test that the correct instance attribute values are generated from the config file read."""

        # read configuration from file
        cfg = ReadConfig(config_file=TestReadConfig.CONFIG_YAML)

        # check value equality for each variable with expected
        self.check_values(cfg)

        # check type equality for each variable with expected
        self.check_types(cfg)

    def test_instance_attributes_params(self):
        """Test that the correct instance attribute values are generated from parameters."""

        # read configuration from parameters
        cfg = ReadConfig(output_directory=TestReadConfig.OUTPUT_DIR,
                         start_year=TestReadConfig.START_YEAR,
                         through_year=TestReadConfig.THROUGH_YEAR,
                         time_step=TestReadConfig.TIME_STEP,
                         alpha_urban= TestReadConfig.ALPHA_URBAN,
                         alpha_rural=TestReadConfig.ALPHA_RURAL,
                         beta_urban=TestReadConfig.BETA_URBAN,
                         beta_rural=TestReadConfig.BETA_RURAL)

        # check value equality for each variable with expected
        self.check_values(cfg)

        # check type equality for each variable with expected
        self.check_types(cfg)

    def check_values(self, cfg):
        """Check values of each configuration attribute against expected.

        :param cfg:                     Configuration object

        """
        self.assertEqual(cfg.output_directory, TestReadConfig.OUTPUT_DIR)
        self.assertEqual(cfg.start_year, TestReadConfig.START_YEAR)
        self.assertEqual(cfg.through_year, TestReadConfig.THROUGH_YEAR)
        self.assertEqual(cfg.time_step, TestReadConfig.TIME_STEP)
        self.assertEqual(cfg.alpha_urban, TestReadConfig.ALPHA_URBAN)
        self.assertEqual(cfg.alpha_rural, TestReadConfig.ALPHA_RURAL)
        self.assertEqual(cfg.beta_urban, TestReadConfig.BETA_URBAN)
        self.assertEqual(cfg.beta_rural, TestReadConfig.BETA_RURAL)

    def check_types(self, cfg):
        """Check types of each configuration attribute against expected.

        :param cfg:                     Configuration object

        """
        self.assertEqual(type(cfg.output_directory), TestReadConfig.OUTPUT_DIR_TYPE)
        self.assertEqual(type(cfg.start_year), TestReadConfig.START_YEAR_TYPE)
        self.assertEqual(type(cfg.through_year), TestReadConfig.THROUGH_YEAR_TYPE)
        self.assertEqual(type(cfg.time_step), TestReadConfig.TIME_STEP_TYPE)
        self.assertEqual(type(cfg.alpha_urban), TestReadConfig.ALPHA_URBAN_TYPE)
        self.assertEqual(type(cfg.alpha_rural), TestReadConfig.ALPHA_RURAL_TYPE)
        self.assertEqual(type(cfg.beta_urban), TestReadConfig.BETA_URBAN_TYPE)
        self.assertEqual(type(cfg.beta_rural), TestReadConfig.BETA_RURAL_TYPE)


if __name__ == '__main__':
    unittest.main()
