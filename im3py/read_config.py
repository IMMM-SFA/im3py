"""Configuration reader for <your model name>

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import datetime
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

    :param start_step:                          Start time step value
    :type start_step:                           int

    :param through_step:                        Through time step value
    :type through_step:                         int

    :param time_step:                           Number of steps
    :type time_step:                            int

    :param alpha_param:                         Alpha parameter for model.  Acceptable range:  -2.0 to 2.0
    :type alpha_param:                          float


    :param beta_param:                          Beta parameter for model.  Acceptable range:  -2.0 to 2.0
    :type beta_param:                           float

    """

    OUT_DIR_KEY = 'output_directory'
    START_STEP_KEY = 'start_step'
    THROUGH_STEP_KEY = 'through_step'
    TIME_STEP_KEY = 'time_step'
    ALPHA_KEY = 'alpha_param'
    BETA_KEY = 'beta_param'

    # definition of acceptable range of values for parameters
    MAX_PARAM_VALUE = 2.0
    MIN_PARAM_VALUE = -2.0

    # format for datetime string
    DATETIME_FORMAT = '%Y-%m-%d_%Hh%Mm%Ss'

    def __init__(self, config_file=None, output_directory=None, start_step=None,  through_step=None,
                 time_step=None, alpha_param=None, beta_param=None):

        self._config_file = config_file
        self._output_directory = output_directory
        self._start_step = start_step
        self._through_step = through_step
        self._time_step = time_step
        self._alpha_param = alpha_param
        self._beta_param = beta_param

    @property
    def date_time_string(self):
        """Get a current time in a string matching the specified datetime format."""

        return datetime.datetime.now().strftime(self.DATETIME_FORMAT)

    @property
    def datetime_format(self):
        """Convenience wrapper for the DATETIME_FORMAT class attribute."""

        return self.DATETIME_FORMAT

    @property
    def config(self):
        """Read the YAML config file object"""

        if self._config_file is None:
            return None

        else:
            with open(self._config_file, 'r') as yml:
                return yaml.load(yml)

    @property
    def output_directory(self):
        """Validate output directory."""

        if self.config is None:
            return self.validate_directory(self._output_directory)
        else:
            key = self.validate_key(self.config, self.OUT_DIR_KEY)
            return self.validate_directory(key)

    @property
    def start_step(self):
        """Start time step."""

        return self.validate_step(self._start_step, self.START_STEP_KEY)

    @property
    def through_step(self):
        """Through time step."""

        return self.validate_step(self._through_step, self.THROUGH_STEP_KEY)

    @property
    def time_step(self):
        """Number of time steps."""

        return self.validate_step(self._time_step, self.TIME_STEP_KEY)

    @property
    def alpha_param(self):
        """Alpha parameter for model."""

        return self.validate_parameter(self._alpha_param, self.ALPHA_KEY)

    @alpha_param.setter
    def alpha_param(self, value):
        """Setter for alpha parameter."""

        self._alpha_param = self.validate_parameter(value, self.ALPHA_KEY)

    @property
    def beta_param(self):
        """Beta parameter for model."""

        return self.validate_parameter(self._beta_param, self.BETA_KEY)

    @beta_param.setter
    def beta_param(self, value):
        """Setter for alpha parameter."""

        self._beta_param = self.validate_parameter(value, self.BETA_KEY)

    @property
    def step_list(self):
        """Create a list of time steps from the start and through steps by the step interval."""

        return range(self.start_step, self.through_step + self.time_step, self.time_step)

    @property
    def logfile(self):
        """Full path with file name and extension to the logfile."""

        # logger file name
        return os.path.join(self.output_directory, 'logfile_{}.log'.format(self.date_time_string))

    @staticmethod
    def validate_int(step):
        """Ensure time step is type int"""

        try:
            return int(step)
        except TypeError:
            raise TypeError(f"Step value '{step}' is not an integer.")

    @staticmethod
    def validate_float(val):
        """Ensure parameter value is type float"""

        try:
            return float(val)
        except TypeError:
            raise TypeError(f"Parameter value '{val}' is not a float.")

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

    def validate_parameter(self, param, key):
        """Validate parameter existence and range.

        :param param:               Parameter value
        :type param:                float

        :param key:                 Configuration key from YAML file
        :type key:                  str

        :return:                    int; parameter

        """

        if self.config is None:
            is_float = self.validate_float(param)
            return self.validate_range(is_float)
        else:
            is_key = self.validate_key(self.config, key)
            is_float = self.validate_float(is_key)
            return self.validate_range(is_float)

    def validate_range(self, value):
        """Ensure value falls within an acceptable range."""

        if (value >= self.MIN_PARAM_VALUE) and (value <= self.MAX_PARAM_VALUE):
            return value
        else:
            raise ValueError(f"Parameter value '{value}' is not within the valid range of {self.MIN_PARAM_VALUE} - {self.MAX_PARAM_VALUE}.")

    def validate_step(self, step, key):
        """Validate step existence and value.

        :param step:                Time step value
        :type step:                 int

        :param key:                 Configuration key from YAML file
        :type key:                  str

        :return:                    int; time step

        """

        if self.config is None:
            return self.validate_int(step)
        else:
            is_key = self.validate_key(self.config, key)
            return self.validate_int(is_key)
