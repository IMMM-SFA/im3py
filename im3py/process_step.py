"""Process time step for <your model name>

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import logging
import time

import im3py.some_code as fake


def process_step(step, alpha_param, beta_param, start_step, output_directory):
    """Process a time step based on a condition.

    :param step:                                Current time step
    :type step:                                 int

    :param start_step:                          Start time step value
    :type start_step:                           int

    :param through_step:                        Through time step value
    :type through_step:                         int

    :param alpha_param:                         Alpha parameter for model.  Acceptable range:  -2.0 to 2.0
    :type alpha_param:                          float

    :param beta_param:                          Beta parameter for model.  Acceptable range:  -2.0 to 2.0
    :type beta_param:                           float

    """

    start_time = time.time()

    logging.info("Processing step:  {}".format(step))

    # create a value list for each parameter
    value_list = [alpha_param, beta_param]

    if step == start_step:

        # if year one, generate sum message file
        fake.write_sum_file(step, value_list, output_directory)

    else:

        # for other years, generate a mean message file
        fake.write_mean_file(step, value_list, output_directory)

    logging.info("Processing for step {} completed in {} minutes.".format(step, (time.time() - start_time) / 60))

