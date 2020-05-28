"""Configuration reader for <your model name>

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os
import yaml


class ReadConfig:
    """Read configuration data either provided in the configuration YAML file or as passed in via arguments.

    :param config_file:                         Full path to configuration YAML file with file name and
                                                extension. If not provided by the user, the code will default to the
                                                expectation of alternate arguments.
    :type config_file:                          str


    :param output_directory:                    Full path with file name and extension to the output directory
                                                where outputs and the log file will be written.
    :type output_directory:                     str

    :param start_year:                          Four digit first year to process for the projection.
    :type start_year:                           int

    :param through_year:                        Four digit last year to process for the projection.
    :type through_year:                         int

    :param time_step:                           int. Number of steps
    :type time_step:                            int

    :param alpha_param:                         Alpha parameter for urban. Represents the degree to which the
                                                population size of surrounding cells translates into the suitability
                                                of a focal cell.  A positive value indicates that the larger the
                                                population that is located within the 100 km neighborhood, the more
                                                suitable the focal cell is.  More negative value implies less suitable.
                                                Acceptable range:  -2.0 to 2.0
    :type alpha_param:                          float


    :param beta_param:                          float. Beta parameter for urban. Reflects the significance of distance
                                                to surrounding cells on the suitability of a focal cell.  Within 100 km,
                                                beta determines how distance modifies the effect on suitability.
                                                Acceptable range:  -0.5 to 2.0
    :type beta_param:                           float

    """

    OUT_DIR_KEY = 'output_directory'
    START_YR_KEY = 'start_year'
    THROUGH_YR_KEY = 'through_year'
    TIME_STEP_KEY = 'time_step'
    ALPHA_KEY = 'alpha_param'
    BETA_KEY = 'beta_param'

    def __init__(self, config_file=None, output_directory=None, start_year=None,  through_year=None,
                 time_step=None, alpha_param=None, beta_param=None):

        self._config_file = config_file
        self._output_directory = output_directory

        if config_file is None:

            self.start_year = start_year
            self.through_year = through_year
            self.time_step = time_step
            self.alpha_param = alpha_param
            self.beta_param = beta_param

        else:

            self.start_year = self.validate_key(cfg, 'start_year')
            self.through_year = self.validate_key(cfg, 'through_year')
            self.time_step = self.validate_key(cfg, 'time_step')
            self.alpha_param = self.validate_key(cfg, 'alpha_param')
            self.beta_param = self.validate_key(cfg, 'beta_param')

        # list of time steps in projection
        self.steps = range(self.start_year, self.through_year + self.time_step, self.time_step)

    @property
    def output_directory(self):
        """Validate output directory"""

        if self.config is None:
            return self.validate_directory(self._output_directory)
        else:
            key = self.validate_key(self.config, self.OUT_DIR_KEY)
            return self.validate_directory(key)

    @property
    def start_year(self):
        """Validate start year"""
        if self.config is None:
            return self.validate_step(self._start_year)
        else:
            key = self.validate_key(self.config, self.START_YR_KEY)
            return self.validate_step(key)

    @staticmethod
    def vaildate_step(step):
        """Ensure time step is within expected range and an integer"""
        pass

    @staticmethod
    def validate_directory(directory):
        """Validate file to ensure it exists.

        :param directory:                       Full path to the target directory.
        :type directory:                        str

        :return:                                Full path of a valid directory

        """
        if os.path.isdir(directory):
            return directory
        else:
            raise NotADirectoryError(f"`output_directory`: {directory} does not exist.")

    @staticmethod
    def validate_key(yaml_object, key):
        """Check to see if key is in YAML file, if not return None.

        :param yaml_object:                     YAML object for the configuration file

        :param key:                             Target key name from the configuration file.
        :type key:                              str

        :return:                                Value from configuration file matching the key. If no key present,
                                                return None.
        """
        try:
            return yaml_object[key]
        except KeyError:
            return None

    @property
    def config(self):
        """Read the YAML config file.

        :param config_file:                     Full path with file name and extension to the input config.yml file
        :type config_file:                      str

        :return:                                YAML config object

        """
        if self._config_file is None:
            return None

        else:
            with open(self._config_file, 'r') as yml:
                return yaml.load(yml)
