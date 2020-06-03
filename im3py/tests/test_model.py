"""Tests for the configuration reader functionality.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os
import pkg_resources
import tempfile
import unittest

from im3py.model import Model


class TestModel(unittest.TestCase):
    """Tests for the `ReadConfig` class that reads the input configuration from the user."""

    # test config YAML file
    CONFIG_YAML = pkg_resources.resource_filename('im3py', 'tests/data/inputs/config.yml')

    # comparison outputs
    OUTPUT_2015 = pkg_resources.resource_filename('im3py', 'tests/data/comp_data/output_year_2015.txt')
    OUTPUT_2016 = pkg_resources.resource_filename('im3py', 'tests/data/comp_data/output_year_2016.txt')

    # expected attribute values
    OUTPUT_DIR = pkg_resources.resource_filename('im3py', "tests/data")
    START_STEP = 2015
    THROUGH_STEP = 2016
    TIME_STEP = 1
    ALPHA_PARAM = 2.0
    BETA_PARAM = 1.42

    def test_model_instantiation(self):
        """Test model instantiation."""

        run = Model(output_directory=TestModel.OUTPUT_DIR,
                     through_step=TestModel.THROUGH_STEP,
                     time_step=TestModel.TIME_STEP,
                     alpha_param=TestModel.ALPHA_PARAM,
                     beta_param=TestModel.BETA_PARAM)

        self.assertEqual(f"{type(run)}", "<class 'im3py.model.Model'>")

    def test_model_outputs(self):
        """Ensure model outputs are what is expected."""

        # create a temporary directory to hold the outputs
        with tempfile.TemporaryDirectory() as dirpath:

            run = Model(output_directory=dirpath,
                        start_step=TestModel.START_STEP,
                        through_step=TestModel.THROUGH_STEP,
                        time_step=TestModel.TIME_STEP,
                        alpha_param=TestModel.ALPHA_PARAM,
                        beta_param=TestModel.BETA_PARAM,
                        write_logfile=False)

            run.run_all_steps()

            # compare outputs to expected
            run_output_2015 = os.path.join(dirpath, 'output_year_2015.txt')
            run_output_2016 = os.path.join(dirpath, 'output_year_2016.txt')

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
