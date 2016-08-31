import pytest

from msibi_utils.general import get_fn
from msibi_utils.parse_logfile import parse_logfile


def test_all_pairs_same_number_of_states():
    filename = get_fn('opt.out')
    logfile_info = parse_logfile(filename)
    assert(len(logfile_info) == 15)
    for pair, states in logfile_info.items():
        assert len(states) == 4
        for state, f_fits in states.items():
            assert(len(f_fits) == 8)
