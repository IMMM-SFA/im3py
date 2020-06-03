"""<Sentence description of what this file does.>

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import logging
import os
import time

import im3py.process_step as proc

# Logger inherits ReadConfig
from im3py.logger import Logger


class Model(Logger):
    """Model wrapper for <your model name>.  This class inherits both ReadConfig and Logger classes from this package.
    Input parameters are specified and controlled in ReadConfig class in 'read_config.py'.

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

    Examples:

        # Option 1:  run model for all steps by passing a configuration YAML as the sole argument
        >>> from im3py.model import Model
        >>> run = Model(config_file="<path to your config file with the file name and extension.>")
        >>> run.run_all_steps()

        # Option 2:  run model for all steps by passing argument values
        >>> from im3py.model import Model
        >>> run = Model(output_directory="<output directory path>",
        >>>                 start_step=2015,
        >>>                 through_step=2030,
        >>>                 time_step=1,
        >>>                 alpha_param= 2.0,
        >>>                 beta_param=1.42)
        >>> run.run_all_steps()

        # Option 3:  run model by year by passing argument values and updating them between time steps.
        >>> from im3py.model import Model
        >>> run = Model(output_directory="<output directory path>",
        >>>                 start_step=2015,
        >>>                 through_step=2030,
        >>>                 time_step=1,
        >>>                 alpha_param= 2.0,
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

    def __init__(self, config_file=None, output_directory=None, start_step=None,  through_step=None,
                 time_step=None, alpha_param=None, beta_param=None, write_logfile=True):

        super(Logger, self).__init__(config_file, output_directory, start_step,  through_step,
                                     time_step, alpha_param, beta_param, write_logfile)

        # initialize time step generator
        self._timestep_generator = self.build_timestep_generator()

    @staticmethod
    def make_dir(pth):
        """Create dir if not exists."""

        if not os.path.exists(pth):
            os.makedirs(pth)

    def log_parameters(self):
        """Write parameters to log."""

        logging.info(f"output_directory = {self.output_directory}")
        logging.info(f"start_step = {self.start_step}")
        logging.info(f"through_step = {self.through_step}")
        logging.info(f"time_step = {self.time_step}")
        logging.info(f"alpha_param = {self.alpha_param}")
        logging.info(f"beta_param = {self.beta_param}")

    def initialize(self):
        """Setup model."""

        # build output directory first to store logfile and other outputs
        self.make_dir(self.output_directory)

        # initialize logger
        self.initialize_logger()

        logging.info("Start time:  {}".format(time.strftime(self.datetime_format)))

        # log run parameters
        logging.info("Model parameters:")
        self.log_parameters()

    def build_timestep_generator(self):
        """Construct time step generator from ProcessStep class."""

        for step in self.step_list:
            yield proc.process_step(step, self.alpha_param, self.beta_param, self.start_step, self.output_directory)

    def advance_step(self):
        """Advance time step."""

        next(self._timestep_generator)

    def close(self):
        """End model run and close log files."""

        logging.info("End time:  {}".format(time.strftime(self.datetime_format)))

        # Remove logging handlers
        self.close_logger()

    def run_all_steps(self):
        """Run model for all years."""

        # initialize model
        self.initialize()

        # start time
        td = time.time()

        logging.info("Starting model run")

        # process all years
        for _ in self.step_list:

            logging.info(_)
            self.advance_step()

        logging.info("Model run completed in {} minutes.".format((time.time() - td) / 60))

        # clean logger
        self.close()
