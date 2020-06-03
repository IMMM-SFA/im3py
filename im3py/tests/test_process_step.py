"""Tests for process_step.py functionality.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os
import pkg_resources
import tempfile
import unittest

from im3py.process_step import process_step


class TestProcessStep(unittest.TestCase):
    """Tests for the `ReadConfig` class that reads the input configuration from the user."""

    # expected attribute values
    OUTPUT_DIR = pkg_resources.resource_filename('im3py', 'tests/data')
    START_STEP = 2015
    THROUGH_STEP = 2016
    TIME_STEP = 1
    ALPHA_PARAM = 2.0
    BETA_PARAM = 1.42

    # comparison outputs
    OUTPUT_2015 = pkg_resources.resource_filename('im3py', 'tests/data/comp_data/output_year_2015.txt')

    @classmethod
    def create_output_directory(cls):
        """Create directory if it does not exist."""

        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)

    def test_process_step_outputs(self):
        """Test output equality."""

        # create a temporary directory to hold the outputs
        with tempfile.TemporaryDirectory() as dirpath:

            # instantiate class for the start year
            process_step(step=TestProcessStep.START_STEP,
                         alpha_param=TestProcessStep.ALPHA_PARAM,
                         beta_param=TestProcessStep.BETA_PARAM,
                         start_step=TestProcessStep.START_STEP,
                         output_directory=dirpath)

            # compare outputs to expected
            run_output_2015 = os.path.join(dirpath, 'output_year_2015.txt')

            self.assertEqual(self.get_file_content(run_output_2015), self.get_file_content(TestProcessStep.OUTPUT_2015))

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
