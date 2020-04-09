"""Process time step for <your model name>

:author:   <developer names>
:email:   <developer emails>

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import logging
import time

import im3py.some_code as fake


class ProcessStep:
    """Process a time step based on a condition.

    :param cfg:                                 Configuration file object

    :param yr:                                  Target year (YYYY) for a time step
    :type yr:                                   int

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


    """

    def __init__(self, cfg, yr, alpha_urban, beta_urban, alpha_rural, beta_rural):

        # start time
        td = time.time()

        logging.info("Processing year:  {}".format(yr))

        # create a value list for each parameter
        value_list = [alpha_urban, beta_urban, alpha_rural, beta_rural]

        if yr == cfg.start_year:

            # if year one, generate sum message file
            fake.write_sum_file(yr, value_list, cfg.output_directory)

        else:

            # for other years, generate a mean message file
            fake.write_mean_file(yr, value_list, cfg.output_directory

        logging.info("Processing for year {} completed in {} minutes.".format(yr, (time.time() - td) / 60))
