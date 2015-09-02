def parse_logfile(filename): 
    """Parse the logfile from an MS IBI optimization

    Args
    ----
    filename : str
        The name of the logfile from the MS IBI optimization

    Returns
    -------
    logfile_info : dict
        Keys are pairs, values are dicts where keys are states, values are lists of fit
        values
    """
    logfile_info = {}
    for line in open(filename, 'r'):
        try: 
            keyword = line.split()[1]
        except IndexError:
            pass
        if keyword == 'pair':
            try:
                logfile_info[line.split()[2][:-1]][line.split()[4][:-1]].append(
                        line.split()[-1])
            except KeyError:  # pair not in logfile_info
                try:
                    logfile_info[line.split()[2][:-1]][line.split()[4][:-1]] = [
                            line.split()[-1]]
                except KeyError:  # state not in pairs in logfile_info
                    logfile_info[line.split()[2][:-1]] = {
                            line.split()[4][:-1]: [line.split()[-1]]}
    return logfile_info
