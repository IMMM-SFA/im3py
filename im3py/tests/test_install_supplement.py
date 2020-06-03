import os
import pkg_resources
import tempfile
import unittest

import pandas as pd

from im3py.install_supplement import InstallSupplement


class TestInstallSupplement(unittest.TestCase):

    # test info from Zenodo
    REMOTE_DATA_DIR = 'test'
    REMOTE_DATA_FILE = 'test_no-header.csv'

    # comparison datasets
    COMP_CSV = pkg_resources.resource_filename('im3py', 'tests/data/comp_data/test_no-header.csv')

    def test_fetch_and_unpack(self):

        # create a temporary directory to hold the outputs
        with tempfile.TemporaryDirectory() as dirpath:

            # instantiate class
            sup = InstallSupplement(dirpath)

            # fetch and unzip data to tempdir
            sup.fetch_unpack_data()

            # create path to unpacked file
            test_file = os.path.join(dirpath, TestInstallSupplement.REMOTE_DATA_DIR, TestInstallSupplement.REMOTE_DATA_FILE)

            # test file to data frame
            df_test = pd.read_csv(test_file)

            # comparison file to data frame
            df_comp = pd.read_csv(TestInstallSupplement.COMP_CSV)

            # compare for equality
            pd.testing.assert_frame_equal(df_comp, df_test)


if __name__ == '__main__':
    unittest.main()
