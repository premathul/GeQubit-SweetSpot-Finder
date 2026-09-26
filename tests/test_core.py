import numpy as np
from gequbit_sweetspot.core import effective_g, quasistatic_t2star

def test_axis_values():
    g=np.diag([1.,2.,3.])
    assert np.isclose(effective_g(g,0,0),3)
    assert np.isclose(effective_g(g,90,0),1)

def test_t2_positive():
    assert quasistatic_t2star([1e9],[1e-6]) > 0
