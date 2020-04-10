"""Tests for the configuration reader functionality.

:author:   <developer names>
:email:    <developer emails>

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os
import pkg_resources
import unittest

from im3py.model import Model


class TestModel(unittest.TestCase):
    """Tests for the `ReadConfig` class that reads the input configuration from the user."""

    # test config YAML file
    CONFIG_YAML = pkg_resources.resource_filename('im3py', 'tests/data/comp_data/config.yml')

    # comparison outputs
    OUTPUT_2015 = pkg_resources.resource_filename('im3py', 'tests/data/comp_data/output_year_2015.txt')
    OUTPUT_2016 = pkg_resources.resource_filename('im3py', 'tests/data/comp_data/output_year_2016.txt')

    # expected attribute values
    OUTPUT_DIR = pkg_resources.resource_filename('im3py', "tests/data/outputs")
    START_YEAR = 2015
    THROUGH_YEAR = 2016
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

    def test_model_outputs(self):
        """Ensure model outputs are what is expected."""

        run = Model(output_directory=TestModel.OUTPUT_DIR,
                         start_year=TestModel.START_YEAR,
                         through_year=TestModel.THROUGH_YEAR,
                         time_step=TestModel.TIME_STEP,
                         alpha_urban= TestModel.ALPHA_URBAN,
                         alpha_rural=TestModel.ALPHA_RURAL,
                         beta_urban=TestModel.BETA_URBAN,
                         beta_rural=TestModel.BETA_RURAL)

        run.run_all_steps()

        # compare outputs to expected
        run_output_2015 = os.path.join(TestModel.OUTPUT_DIR, 'output_year_2015.txt')
        run_output_2016 = os.path.join(TestModel.OUTPUT_DIR, 'output_year_2016.txt')

        self.assertEqual(self.get_file_content(run_output_2015), self.get_file_content(TestModel.OUTPUT_2015))
        self.assertEqual(self.get_file_content(run_output_2016), self.get_file_content(TestModel.OUTPUT_2016))  

    @staticmethod
    def get_file_content(f):
        """Extract file content to a list.

        :param f:                       Full path with file name and extension to a text file.
        :type f:                        str

        :return:                        list of file content

        """

        with open(f) as get:
            return get.readlines()


if __name__ == '__main__':
    unittest.main()
