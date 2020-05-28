"""<Sentence description of what this file does.>

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import datetime
import logging
import os
import time

from im3py import ReadConfig
from im3py import ProcessStep
from im3py import Logger


class Model(ReadConfig):
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
        >>>                 beta_param=1.42)
        >>> run.run_all_steps()

        # Option 3:  run model by year by passing argument values and updating them between time steps.
        >>> from im3py.model import Model
        >>> run = Model(output_directory="<output directory path>",
        >>>                 start_year=2015,
        >>>                 through_year=2030,
        >>>                 time_step=1,
        >>>                 alpha_urban= 2.0,
        >>>                 beta_param=1.42)

        # initialize model
        >>> run.initialize()

        # downscale year 0
        >>> run.advance_step()

        # modify the calibrated alpha parameter value for urban
        >>> run.alpha_param = -0.1

        # run next step with modified parameters
        >>> run.advance_step()

        # close out run
        >>> run.close()

    """
    def __init__(self):

        super(ReadConfig, self).__init__(config_file=None, output_directory=None, start_year=None,  through_year=None,
                                         time_step=None, alpha_param=None, beta_param=None)

        # get current time
        self.date_time_string = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')

    @property
    def logger(self):
        """Convenience wrapper for Logger"""

        # logger file name
        logfile = os.path.join(self.output_directory, 'logfile_{}.log'.format(self.date_time_string))

        return Logger(logfile)

    @staticmethod
    def make_dir(pth):
        """Create dir if not exists."""

        if not os.path.exists(pth):
            os.makedirs(pth)

    def initialize(self):
        """Setup model."""

        # build output directory first to store logfile and other outputs
        self.make_dir(self.output_directory)

        # initialize logger
        self.logger.initialize_logger()

        logging.info("Start time:  {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

        # log run parameters
        logging.info("Input parameters:")
        logging.info("\toutput_directory = {}".format(self.output_directory))

    @property
    def timestep_generator(self):
        """Build step generator."""

        for step in self.steps:
            yield

    def advance_step(self):
        """Advance to next time step."""

        next(self.timestep_generator)

    def run_all_steps(self):
        """Run model for all years."""

        # initialize model
        self.initialize()

        # start time
        td = time.time()

        logging.info("Starting model run")

        # process all years
        for _ in self.steps:
            self.advance_step()

        logging.info("Model run completed in {} minutes.".format((time.time() - td) / 60))

        # clean logger
        self.close()

    def close(self):
        """End model run and close log files."""

        logging.info("End time:  {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

        # Remove logging handlers
        self.logger.close_logger()
