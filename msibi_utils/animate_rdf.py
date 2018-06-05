import pdb
import os.path

from matplotlib import animation
from msibi_utils.parse_logfile import parse_logfile
import numpy as np


def animate_pair_at_state(t1, t2, state, step, target_dir, 
        potentials_dir='./potentials', rdf_dir='./rdfs', 
        potentials2_dir=None, rdf2_dir=None, use_agg=False, 
        to_angstrom=1.0, to_kcalpermol=1.0, n_skip=1):
    """Make an animation showing how the RDF and potential evolve for a particular pair at
    a particular state

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
    potentials2_dir : str, optional
        Path to potentials from MS IBI optimization
    rdf_dir : str
        Path to RDFs from MS IBI optimization
    rdf2_dir : str, optional
        Path to RDFs from MS IBI optimization
    use_agg : bool
        Use Agg backend if true, may be useful for clusters with no display
    to_angstrom : float
        Multiply distance units by this to get into Angstrom
    to_kcalpermol : float
        Multiple energy units by this to get into kcal/mol
    n_skip : int
        Skip this many RDFs when setting y-limits for rdf plot

    Returns
    -------
    Nothing - saves animation in './animations'
    """
    if use_agg:
        import matplotlib as mpl
        mpl.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 5.0*3/4))

    # Load all the primary rdfs and potentials
    rdfs = [np.loadtxt(
            os.path.join(rdf_dir, 'pair_{0}-{1}-state_{2}-step{3}.txt'.format(
            t1, t2, state, i))) for i in range(step)]
    potentials = [np.loadtxt(
            os.path.join(potentials_dir, 'step{0}.pot.{1}-{2}.txt'.format(
            i, t1, t2))) for i in range(step)]
    target_rdf = np.loadtxt(
            os.path.join(target_dir, '{t1}-{t2}-{state}.txt'.format(**locals())))
    # Do some checks if any of the rdfs or potentials were negative
    # Useful if the cluster has I/O errors
    for i, potential in potentials:
        if len(potential) == 0:
            potentials[i] = np.zeros((121,3))
    potentials=np.asarray(potentials)
    for i, rdf in rdfs:
        if len(rdf) == 0:
            rdfs[i] = np.zeros((200,2))
    rdfs = np.asarray(rdfs)
    target_rdf[:, 0] *= to_angstrom
    potentials[:, :, 0] *= to_angstrom
    potentials[:, :, 1] *= to_kcalpermol
    rdfs[:, :, 0] *= to_angstrom

    if potentials2_dir is not None and rdf2_dir is not None:
        rdfs2 = [np.loadtxt(
                os.path.join(rdf2_dir, 'pair_{0}-{1}-state_{2}-step{3}.txt'.format(
                t1, t2, state, i))) for i in range(step)]
        potentials2 = [np.loadtxt(
                os.path.join(potentials2_dir, 'step{0}.pot.{1}-{2}.txt'.format(
                i, t1, t2))) for i in range(step)]

        # Do some checks if any of the rdfs or potentials were negative
        # Useful if the cluster has I/O errors
        for i, potential in potentials2:
            if len(potential) == 0:
                potentials2[i] = np.zeros((121,3))
        for i, rdf in rdfs2:
            if len(rdf) == 0:
                rdfs2[i] = np.zeros((200,2))
        potentials2[:, :, 0] *= to_angstrom
        potentials2[:, :, 1] *= to_kcalpermol
        rdfs2[:, :, 0] *= to_angstrom
        potentials2=np.asarray(potentials2)
        rdfs2 = np.asarray(rdfs2)
    else:
        potentials2 = None
        rdfs2 = None


    ax.plot(target_rdf[:, 0], target_rdf[:, 1], label='Target')
    rdf_line, = ax.plot([], [], label='Query')
    #if np.amax(rdfs[:, :, 1]) > np.amax(target_rdf[:, 1]):
        #ax.set_ylim(top=np.ceil(np.amax(rdfs[n_skip:, :, 1])))
    ax.set_ylim(bottom=0, top=np.ceil(np.amax(target_rdf[:,1])))
    ax.set_ylim([-10 ,40])
    pot_ax = ax.twinx()
    pot_ax.grid(False)
    pot_line, = pot_ax.plot([], [], c='#0485d1')
    if potentials2_dir is not None and rdf2_dir is not None:
        pot_line2, = pot_ax.plot([], [], c='#0485d1', linestyle='--')
        rdf_line2, = ax.plot([], [], label='Query 2', linestyle='--')
    else:
        pot_line2 = None
        rdf_line2 = None
    pot_ax.set_ylim(bottom=1.1*np.amin(potentials[:, :, 1]))
    pot_ax.set_ylim(top=-1.1*np.amin(potentials[:, :, 1]))
    extra = [[potentials[0, -1, 0], ax.get_xlim()[1]], [0, 0]]
    pot_ax.plot(extra[0], extra[1], '#0485d1')
    ax.set_xlim((0, rdfs[0, -1, 0]))
    ax.set_xlabel(u'r, \u00c5')
    ax.set_ylabel('g(r)')
    iter_no = ax.text(0.95, 0.05, '', va='bottom', ha='right', transform=ax.transAxes,
            bbox={'facecolor': 'white', 'alpha': 0.8, 'edgecolor': 'none'})
    pot_ax.set_ylabel('V(r), kcal/mol', color=pot_line.get_c())
    for tl in pot_ax.get_yticklabels():
        tl.set_color(pot_line.get_c())
    ax.set_title('{t1}-{t2}, {state}'.format(**locals()))
    ax.legend()
    fig.tight_layout()
    anim = animation.FuncAnimation(fig, _animate, step, 
            fargs=(rdf_line, pot_line, potentials, rdfs, rdf_line2, pot_line2, potentials2, rdfs2,
                    iter_no ))
    if not os.path.exists('animations'):
        os.makedirs('animations')
    anim.save(os.path.join('animations', '{t1}-{t2}-{state}.mp4'.format(**locals())),
            dpi=400)
    plt.close('all')


def _animate(step, rdf_line, pot_line, potentials, rdfs, rdf_line2, pot_line2, 
            potentials2, rdf2, iter_no):
    rdf_line.set_data(rdfs[step, :, 0], rdfs[step, :, 1])
    pot_line.set_data(potentials[step, :, 0], potentials[step, :, 1])
    if rdfs2 is not None and potentials2 is not None:
        rdf_line2.set_data(rdfs2[step, :, 0], rdfs2[step, :, 1])
        pot_line2.set_data(potentials2[step, :, 0], potentials2[step, :, 1])

            
    iter_no.set_text('%d' % step)
    return rdf_line, pot_line, iter_no

def animate_all_pairs_states(logfile_name, target_dir, 
        potentials_dir='./potentials', rdf_dir = './rdfs', step=-1, 
        use_agg=False, to_angstrom=6.0, to_kcalpermol=0.1, n_skip=1):
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
    n_skip : int
        Set ylimits on RDF plot with RDFs after n_skip

    Returns
    -------
    Nothing is returned, but figures are plotted in './animations'

    The target rdfs are expected to have the format 'target-dir/type1-type2-state.txt'
    """
    if not os.path.exists('animations'):
        os.makedirs('animations')
    logfile_info = parse_logfile(logfile_name)
    for pair, state in logfile_info.items():
        for state, fits in state.items():
            if step == -1:
                step = len(fits)
            type1 = pair.split('-')[0]
            type2 = pair.split('-')[1]
            animate_pair_at_state(type1, type2, state, step, target_dir,
                    potentials_dir, rdf_dir, use_agg, to_angstrom, 
                    to_kcalpermol, n_skip)
