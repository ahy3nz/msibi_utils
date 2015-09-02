import os.path

import numpy as np


def plot_pair_at_state(t1, t2, state, step, target_dir, 
        potentials_dir='./potentials', rdf_dir='./rdfs', use_agg=False, 
        to_angstrom=6.0, to_kcalpermol=0.1):
    """Plot the RDFs (target and CG) and potential on the same plot for a given pair at a
    given state.

    Args
    ----
    t1 : str
        The first type in the pair
    t2 : str
        The second type in the pair
    state : str
        The name of the state
    target_dir : str
        Path to target RDFs
    potentials_dir : str
        Path to potentials from MS IBI optimization
    rdf_dir : str
        Path to RDFs from MS IBI optimization
    use_agg : bool
        Use Agg backend if true, may be useful for clusters with no display
    to_angstrom : float
        Multiply distance units by this to get into Angstrom
    to_kcalpermol : float
        Multiple energy units by this to get into kcal/mol

    Returns
    -------
    Nothing - prints plots in './figures'
    """

    if use_agg:
        import matplotlib as mpl
        mpl.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax =  plt.subplots()
    pot_name = ''.join('step', step, '.pot.', t1, '-', t2, '.txt')
    pot_file = os.path.join(potentials_dir, pot_name)
    rdf_name = ''.join(t1, '-', t2, '-', state, '.txt')
    rdf_file = os.path.join(target_dir, rdf_name)
    try:
        potential = np.loadtxt(pot_file)
        rdfs = [np.loadtxt(rdf_file)]
    except:
        raise IOError('Potential or target RDF file not found')
    rdf_name = ''.join('pair_', t1, '-', t2, '-state_', state, '-step', step, '.txt')
    rdf_file = os.path.join(rdf_dir, rdf_file)
    rdfs.append(np.loadtxt(rdf_file))
    for rdf, label in zip(data, ['Target', 'Query']):
        ax.plot(rdf[:, 0]*to_angstrom, rdf[:, 1], label=label)
    ax.set_xlabel(u'r, \u00c5')
    ax.set_ylabel('g(r)')
    ax.set_ylim(bottom=0)

    pot_ax = ax.twinx()
    pot_ax.plot(potential[:, 0]*to_angstrom, potential[:, 1]*to_kcalpermol, "#0485d1")
    pot_ax.set_ylabel('V(r), kcal/mol')
    pot_ax.set_ylim(bottom=0.1*1.1*np.amin(potential[5:, 1]))
    pot_ax.set_ylim(top=-1.1*0.1*np.amin(potential[5:, 1]))
    ax.set_xlim(rdfs[0][-1, 0])
    extra = [[potential[-1, 0], ax.get_xlim()[1]], [0, 0]]
    pot_ax.plot(extra[0], extra[1], '#0485d1')

    ax.legend(loc=0)
    fig.tight_layout()
    fig.savefig('figures/{t1}-{t2}-{state}-step{step}.pdf'.format(**locals()))
    plt.close('all')

def plot_all_last_iteration(logfile_name, target_dir, 
        potentials_dir='./potentials', rdf_dir = './rdfs', step=-1, use_agg=False):
    """Plot the RDF vs. the target for each pair at each state

    Args
    ----
    fits : dict
        Dict with {pairs: {states: fits}}, as returned from parse_logfile
    target-dir : str
        path (relative or absolute) to target RDFs
    potentials_dir : str
        path (relative or absolute) to potentials from optimization
    step : int
        Print RDFs and potentials from this step
    use_agg : bool
        True to use Agg backend, may be useful on clusters with no display


    Returns
    -------
    Nothing is returned, but figures are plotted in './figures'

    The target rdfs are expected to have the format 'target-dir/type1-type2-state.txt'
    """
    if not os.path.exists('figures'):
        os.makedirs('figures')
    logfile_info = parse_logfile(logfile_name)
    for pair, state in logfile_info.iteritems():
        for state, fits in state.iteritems():
            if step = -1:
                new_step = len(fits)
            type1 = pair.split('-')[0]
            type2 = pair.split('-')[1]
            plot_pair_at_state(type1, type2, state, new_step,
                    potentials_dir, target_dir)
