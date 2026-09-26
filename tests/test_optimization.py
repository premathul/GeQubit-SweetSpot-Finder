import numpy as np
from gequbit_sweetspot.optimization import central_gradient_2d, central_hessian_2d, rank_sweet_spots
from gequbit_sweetspot.robustness import frequency_noise_sigma, t2star_gaussian

def test_gradient_and_hessian():
    f=lambda x,y: (x-2)**2+3*(y+1)**2
    g=central_gradient_2d(f,2,-1,1e-3)
    h=central_hessian_2d(f,2,-1,1e-3)
    assert np.linalg.norm(g)<1e-8
    assert np.allclose(h,[[2,0],[0,6]],atol=1e-5)

def test_rank():
    a=np.array([[1,4],[3,2]])
    r=rank_sweet_spots(a,[0,1],[10,20],top_n=1)
    assert r[0]["theta_deg"]==0 and r[0]["phi_deg"]==20

def test_covariance_t2():
    s=[1e9,2e9]; c=np.diag([1e-12,4e-12])
    assert frequency_noise_sigma(s,c)>0
    assert t2star_gaussian(s,c)>0
