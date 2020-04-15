"""DELETE THIS FILE.  This is a proxy code file that represents where some user code would be.  It is only for
illustrative purposes.

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os


def get_sum(list_of_values):
    """Get the sum from a list of values.

    :param list_of_values:                  List of numeric values
    :type list_of_values:                   list

    :return:                                float.  Sum value

    """
    return sum(list_of_values)


def get_mean(list_of_values):
    """Get the mean from a list of values.

    :param list_of_values:                  List of numeric values
    :type list_of_values:                   list

    :return:                                float.  Mean value

    """
    return sum(list_of_values) / len(list_of_values)


def write_file(message, yr, output_directory):
    """Write an output file for the time step.

    :param message:                         Message to write to file
    :type message:                          str

    :param yr:                              Target year (YYYY)
    :type yr:                               int

    :param output_directory:                Full path to the output directory
    :type output_directory:                 str

    """
    # create output file path
    out_file = os.path.join(output_directory, 'output_year_{}.txt'.format(yr))

    # write output file
    with open(out_file, 'w') as out:
        out.write(message)


def write_sum_file(yr, list_of_values, output_directory):
    """Write a file containing the a message to the user about the sum.

    :param yr:                              Target year (YYYY)
    :type yr:                               int

    :param list_of_values:                  List of numeric values
    :type list_of_values:                   list

    :param output_directory:                Full path to the output directory
    :type output_directory:                 str

    :return:                                Output string; write text file

    """
    message = "The value for year {} is calculated as:  {}\n".format(yr, get_sum(list_of_values))

    # write output file
    write_file(message, yr, output_directory)


def write_mean_file(yr, list_of_values, output_directory):
    """Write a file containing the a message to the user about the sum.

    :param yr:                              Target year (YYYY)
    :type yr:                               int

    :param list_of_values:                  List of numeric values
    :type list_of_values:                   list

    :param output_directory:                Full path to the output directory
    :type output_directory:                 str

    :return:                                Output string; write text file

    """
    message = "The value for year {} is calculated as:  {}\n".format(yr, get_mean(list_of_values))

    # write output file
    write_file(message, yr, output_directory)
