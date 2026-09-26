import numpy as np

def frequency_noise_sigma(sensitivities_hz_per_v, covariance_v2):
    s=np.asarray(sensitivities_hz_per_v,float)
    c=np.asarray(covariance_v2,float)
    if c.shape!=(s.size,s.size): raise ValueError("covariance shape mismatch")
    var=float(s@c@s)
    if var<0 and abs(var)>1e-12: raise ValueError("negative variance")
    return np.sqrt(max(var,0.0))

def t2star_gaussian(sensitivities_hz_per_v, covariance_v2):
    sf=frequency_noise_sigma(sensitivities_hz_per_v,covariance_v2)
    return np.inf if sf==0 else 1/(np.sqrt(2)*np.pi*sf)

def robustness_score(t2star_s, angular_gradient_hz_per_deg, weight=1.0):
    """Simple ranking score penalizing sharp angular sensitivity."""
    g=np.linalg.norm(np.asarray(angular_gradient_hz_per_deg,float))
    return float(t2star_s)/(1+weight*g)
