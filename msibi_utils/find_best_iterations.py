import numpy as np
import pandas as pd
from collections import OrderedDict
from msibi_utils.parse_logfile import parse_logfile

def find_best_iterations(logfile, weights=None):
    """ For each pair, find the iteration with the best fit

    Parameters
    --------
    logfile : str
        The name of the logfile from the MS IBI optimization
    weights ; optional,
        Rather than do a simple arithmetic mean for all states within
        a pair, weight them differently
        Not yet implemented

    Returns
    -------
    df : pd.DataFrame
        Contains information about each pair and the best iteration that yielded
        the highest fit for that pair
    """
    fits = parse_logfile(logfile)
    best_iterations = []
    for pair in sorted(fits):
        best_iterations.append(find_best_iteration(pair, fits))
    df = pd.DataFrame(best_iterations, columns=['pair', 'best_iterations'])
    return df

def find_best_iteration(pair, fits, weights=None):
    all_fits = []
    for state, fit in fits[pair].items():
        if 'npt' in state:
            float_fits=[float(val) for val in fit]
            all_fits.append(float_fits)
    all_fits = np.asarray(all_fits)
    weighted_fits = np.mean(all_fits,axis=0)
    #best_iteration = np.argmax(weighted_fits)
    sorted_iterations = np.argsort(weighted_fits)[-5:][::-1]
    return OrderedDict({"pair": pair, "best_iterations": sorted_iterations})
