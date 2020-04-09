"""Configuration reader for <your model name>

@author   <developer names>
@email:   <developer emails>

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

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

    :param alpha_urban:                         Alpha parameter for urban. Represents the degree to which the
                                                population size of surrounding cells translates into the suitability
                                                of a focal cell.  A positive value indicates that the larger the
                                                population that is located within the 100 km neighborhood, the more
                                                suitable the focal cell is.  More negative value implies less suitable.
                                                Acceptable range:  -2.0 to 2.0
    :type alpha_urban:                          int


    :param beta_urban:                          float. Beta parameter for urban. Reflects the significance of distance
                                                to surrounding cells on the suitability of a focal cell.  Within 100 km,
                                                beta determines how distance modifies the effect on suitability.
                                                Acceptable range:  -0.5 to 2.0
    :type beta_urban:                           int

    :param alpha_rural:                         float. Alpha parameter for rural. Represents the degree to which the
                                                population size of surrounding cells translates into the suitability
                                                of a focal cell.  A positive value indicates that the larger the
                                                population that is located within the 100 km neighborhood, the more
                                                suitable the focal cell is.  More negative value implies less suitable.
                                                Acceptable range:  -2.0 to 2.0
    :type alpha_rural:                          int

    :param beta_rural:                          float. Beta parameter for rural. Reflects the significance of distance
                                                to surrounding cells on the suitability of a focal cell.  Within 100 km,
                                                beta determines how distance modifies the effect on suitability.
                                                Acceptable range:  -0.5 to 2.0
    :type beta_rural:                           int

    """

    def __init__(self, config_file=None, output_directory=None, start_year=None,  through_year=None,
                 time_step=None, alpha_urban=None, beta_urban=None, alpha_rural=None, beta_rural=None):

        if config_file is None:

            self.output_directory = output_directory
            self.start_year = start_year
            self.through_year = through_year
            self.time_step = time_step
            self.alpha_urban = alpha_urban
            self.beta_urban = beta_urban
            self.alpha_rural = alpha_rural
            self.beta_rural = beta_rural

        else:

            # extract config file to YAML object
            cfg = self.get_yaml(config_file)

            self.output_directory = self.validate_key(cfg, 'output_directory')
            self.start_year = self.validate_key(cfg, 'start_year')
            self.through_year = self.validate_key(cfg, 'through_year')
            self.time_step = self.validate_key(cfg, 'time_step')
            self.alpha_urban = self.validate_key(cfg, 'alpha_urban')
            self.beta_urban = self.validate_key(cfg, 'beta_urban')
            self.alpha_rural = self.validate_key(cfg, 'alpha_rural')
            self.beta_rural = self.validate_key(cfg, 'beta_rural')

        # list of time steps in projection
        self.steps = range(self.start_year, self.through_year + self.time_step, self.time_step)

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

    @staticmethod
    def get_yaml(config_file):
        """Read the YAML config file.

        :param config_file:                     Full path with file name and extension to the input config.yml file
        :type config_file:                      str

        :return:                                YAML config object

        """
        with open(config_file, 'r') as yml:
            return yaml.load(yml)
