import os.path

import timplotlib as tpl

from msibi_utils.parse_logfile import parse_logfile
import numpy as np


def plot_pair_at_state(t1, t2, state, step, target_dir, 
        potentials_dir='./potentials', rdf_dir='./rdfs', use_agg=False, 
        to_angstrom=6.0, to_kcalpermol=0.1, lw=None):
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
    pot_name = 'step{step}.pot.{t1}-{t2}.txt'.format(**locals())
    pot_file = os.path.join(potentials_dir, pot_name)
    rdf_name = '{t1}-{t2}-{state}.txt'.format(**locals())
    rdf_file = os.path.join(target_dir, rdf_name)
    try:
        potential = np.loadtxt(pot_file)
    except:
        raise IOError('File not found: {pot_file}'.format(**locals()))
    try:
        rdfs = [np.loadtxt(rdf_file)]
    except: 
        raise IOError('File not found: {rdf_file}'.format(**locals()))
    potential[:, 0] *= to_angstrom
    potential[:, 1] *= to_kcalpermol
    rdfs[0][:, 0] *= to_angstrom
    rdf_name = 'pair_{t1}-{t2}-state_{state}-step{step}.txt'.format(**locals())
    rdf_file = os.path.join(rdf_dir, rdf_name)
    rdfs.append(np.loadtxt(rdf_file))
    rdfs[1][:, 0] *= to_angstrom
    for rdf, label in zip(rdfs, ['Target', 'Query']):
        if lw: 
            ax.plot(rdf[:, 0], rdf[:, 1], label=label, lw=lw)
        else:
            ax.plot(rdf[:, 0], rdf[:, 1], label=label)
    ax.set_xlabel(u'r, \u00c5')
    ax.set_ylabel('g(r)')
    ax.set_ylim(bottom=0)
    ax.set_title('{t1}-{t2}, {state}'.format(**locals()))

    pot_ax = ax.twinx()
    pot_ax.plot(potential[:, 0], potential[:, 1], "#0485d1")
    pot_ax.set_ylabel('V(r), kcal/mol')
    pot_ax.set_ylim(bottom=1.1*np.amin(potential[5:, 1]))
    pot_ax.set_ylim(top=-1.1*np.amin(potential[5:, 1]))
    ax.set_xlim(right=rdfs[0][-1, 0])
    extra = [[potential[-1, 0], ax.get_xlim()[1]], [0, 0]]
    pot_ax.plot(extra[0], extra[1], '#0485d1')
    ax.legend(loc=0)
    tpl.timize(ax)
    fig.tight_layout()
    if not os.path.exists('figures'):
        os.makedirs('figures')
    fig.savefig('figures/{t1}-{t2}-{state}-step{step}.pdf'.format(**locals()),
            transparent=True)
    plt.close('all')

def plot_all_rdfs(logfile_name, target_dir, 
        potentials_dir='./potentials', rdf_dir = './rdfs', step=-1, 
        use_agg=False, to_angstrom=6.0, to_kcalpermol=0.1, lw=None):
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
    for pair, state in logfile_info.items():
        for state, fits in state.items():
            if step == -1:
                step = len(fits) - 1
            type1 = pair.split('-')[0]
            type2 = pair.split('-')[1]
            plot_pair_at_state(type1, type2, state, step, target_dir,
                    potentials_dir, rdf_dir, use_agg, to_angstrom, to_kcalpermol,
                    lw=lw)
