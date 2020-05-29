"""Install data supplement from remote source.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import argparse
import os
import requests
import logging
import zipfile

from pkg_resources import get_distribution
from io import BytesIO


class InstallSupplement:
    """Download and unpack example data supplement from Zenodo that matches the current installed distribution.

    :param example_data_directory:              Full path to the directory you wish to install
                                                the example data to.  Must be write-enabled
                                                for the user.
    :type example_data_directory:               str

    """

    PACKAGE_NAME = 'im3py'

    # URL for DOI minted example data hosted on Zenodo
    DATA_VERSION_URLS = {'0.1.0': 'https://zenodo.org/record/3856417/files/test.zip?download=1'}

    def __init__(self, example_data_directory):

        # full path to the root directory where the example dir will be stored
        self._example_data_directory = example_data_directory

    @property
    def example_data_directory(self):
        """Check validitiy of user provided directory"""

        if os.path.isdir(self._example_data_directory):
            return self._example_data_directory
        else:
            raise NotADirectoryError(f"The specified `example_data_directory` : '{self._example_data_directory}' is not a valid directory.")

    @property
    def current_version(self):
        """Get the current version of the package."""

        return get_distribution(self.PACKAGE_NAME).version

    @property
    def data_url(self):
        """Get the data url based off of the currenct package version."""

        try:
            return self.DATA_VERSION_URLS[self.current_version]

        except KeyError:
            raise KeyError(f"Link to data missing for current version:  {self.current_version}.  Please contact admin.")

    @property
    def download_data(self):
        """Get request."""

        # retrieve content from URL
        logging.info(f"Downloading data for version {self.current_version}")

        return requests.get(self.data_url)

    @property
    def fetch_unpack_data(self):
        """Download and unpack the Zenodo example data supplement for the
        current distribution."""

        with zipfile.ZipFile(BytesIO(self.download_data.content)) as zipped:

            # extract each file in the zipped dir to the project
            for f in zipped.namelist():
                logging.info(f"Unzipped: {os.path.join(self.example_data_directory, f)}")
                zipped.extract(f, self.example_data_directory)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    help_msg = 'Full path to the directory you wish to install the supplemental data to.'
    parser.add_argument('example_data_directory', type=str, help=help_msg)
    args = parser.parse_args()

    zen = InstallSupplement(args.example_data_directory)
