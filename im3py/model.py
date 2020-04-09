"""<Sentence description of what this file does.>

:author:   <developer names>
:email:   <developer emails>

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import datetime
import logging
import os
import sys
import time

from im3py.read_config import ReadConfig
from im3py.process_step import ProcessStep


class Model:
    """Model wrapper for <your model name>

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
    :type alpha_urban:                          float


    :param beta_urban:                          float. Beta parameter for urban. Reflects the significance of distance
                                                to surrounding cells on the suitability of a focal cell.  Within 100 km,
                                                beta determines how distance modifies the effect on suitability.
                                                Acceptable range:  -0.5 to 2.0
    :type beta_urban:                           float

    :param alpha_rural:                         float. Alpha parameter for rural. Represents the degree to which the
                                                population size of surrounding cells translates into the suitability
                                                of a focal cell.  A positive value indicates that the larger the
                                                population that is located within the 100 km neighborhood, the more
                                                suitable the focal cell is.  More negative value implies less suitable.
                                                Acceptable range:  -2.0 to 2.0
    :type alpha_rural:                          float

    :param beta_rural:                          float. Beta parameter for rural. Reflects the significance of distance
                                                to surrounding cells on the suitability of a focal cell.  Within 100 km,
                                                beta determines how distance modifies the effect on suitability.
                                                Acceptable range:  -0.5 to 2.0
    :type beta_rural:                           float

    Examples:

        # Option 1:  run model for all years by passing a configuration YAML as the sole argument
        >>> from im3py.model import Model
        >>> run = Model(config_file="<path to your config file with the file name and extension.")
        >>> run.run_all_steps()

        # Option 2:  run model for all years by passing argument values
        >>> from im3py.model import Model
        >>> run = Model(output_directory="<output directory path>",
        >>>                 start_year=2015,
        >>>                 through_year=2030,
        >>>                 time_step=1,
        >>>                 alpha_urban= 2.0,
        >>>                 alpha_rural=0.08,
        >>>                 beta_urban=1.78,
        >>>                 beta_rural=1.42)
        >>> run.run_all_steps()

        # Option 3:  run model by year by passing argument values and updating them between time steps.
        >>> from im3py.model import Model
        >>> run = Model(output_directory="<output directory path>",
        >>>                 start_year=2015,
        >>>                 through_year=2030,
        >>>                 time_step=1,
        >>>                 alpha_urban= 2.0,
        >>>                 alpha_rural=0.08,
        >>>                 beta_urban=1.78,
        >>>                 beta_rural=1.42)

        # initialize model
        >>> run.initialize()

        # downscale year 0
        >>> run.advance_step()

        # modify the calibrated alpha parameter value for urban
        >>> run.alpha_urban = -0.1

        # run next step with modified parameters
        >>> run.advance_step()

        # close out run
        >>> run.close()

    """
    def __init__(self, config_file=None, output_directory=None, start_year=None,  through_year=None,
                 time_step=None, alpha_urban=None, beta_urban=None, alpha_rural=None, beta_rural=None):

        # get current time
        self.date_time_string = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')

        # read the YAML configuration file
        self.cfg = ReadConfig(config_file=config_file,
                              output_directory=output_directory,
                              start_year=start_year,
                              through_year=through_year,
                              time_step=time_step,
                              alpha_urban=alpha_urban,
                              beta_urban=beta_urban,
                              alpha_rural=alpha_rural,
                              beta_rural=beta_rural)

        # expose key variables that we want the user to have non-nested access to
        self.alpha_urban = self.cfg.alpha_urban
        self.beta_urban = self.cfg.beta_urban
        self.alpha_rural = self.cfg.alpha_rural
        self.beta_rural = self.cfg.beta_rural

        # logfile path
        self.logfile = os.path.join(self.cfg.output_directory, 'logfile_{}.log'.format(self.date_time_string))

        # set up time step generator
        self.timestep = self.build_step_generator()

    @staticmethod
    def make_dir(pth):
        """Create dir if not exists."""

        if not os.path.exists(pth):
            os.makedirs(pth)

    def init_log(self):
        """Initialize project-wide logger. The logger outputs to both stdout and a file."""

        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_level = logging.INFO

        logger = logging.getLogger()
        logger.setLevel(log_level)

        # logger console handler
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setLevel(log_level)
        c_handler.setFormatter(log_format)
        logger.addHandler(c_handler)

        # logger file handler
        f_handler = logging.FileHandler(self.logfile)
        c_handler.setLevel(log_level)
        c_handler.setFormatter(log_format)
        logger.addHandler(f_handler)

    def initialize(self):
        """Setup model."""

        # build output directory first to store logfile and other outputs
        self.make_dir(self.cfg.output_directory)

        # initialize logger
        self.init_log()

        logging.info("Start time:  {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

        # log run parameters
        logging.info("Input parameters:")
        logging.info("\toutput_directory = {}".format(self.cfg.output_directory))

    def build_step_generator(self):
        """Build step generator."""

        for step in self.cfg.steps:
            yield ProcessStep(self.cfg, step, self.alpha_urban, self.beta_urban, self.alpha_rural, self.beta_rural)

    def advance_step(self):
        """Advance to next time step."""

        next(self.timestep)

    def run_all_steps(self):
        """Run model for all years."""

        # initialize model
        self.initialize()

        # start time
        td = time.time()

        logging.info("Starting model run")

        # process all years
        for _ in self.cfg.steps:
            self.advance_step()

        logging.info("Model run completed in {} minutes.".format((time.time() - td) / 60))

        # clean logger
        self.close()

    @staticmethod
    def close():
        """End model run and close log files."""

        logging.info("End time:  {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

        # Remove logging handlers
        logger = logging.getLogger()

        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        logging.shutdown()
