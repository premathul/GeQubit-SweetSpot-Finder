import numpy as np

def direction(theta_deg, phi_deg=0.0):
    t, p = np.deg2rad([theta_deg, phi_deg])
    return np.array([np.sin(t)*np.cos(p), np.sin(t)*np.sin(p), np.cos(t)])

def effective_g(g_tensor, theta_deg, phi_deg=0.0):
    n = direction(theta_deg, phi_deg)
    return np.linalg.norm(np.asarray(g_tensor, float) @ n)

def finite_difference_susceptibility(freq_fn, x, step):
    if step <= 0:
        raise ValueError("step must be positive")
    return (freq_fn(x+step)-freq_fn(x-step))/(2*step)

def quasistatic_t2star(sensitivities_hz_per_v, sigma_v):
    s=np.asarray(sensitivities_hz_per_v,float)
    sig=np.broadcast_to(np.asarray(sigma_v,float),s.shape)
    sf=np.sqrt(np.sum((s*sig)**2))
    return np.inf if sf==0 else 1/(np.sqrt(2)*np.pi*sf)

def scan_angles(metric_fn, theta_grid, phi_grid):
    best=None
    rows=[]
    for th in theta_grid:
        for ph in phi_grid:
            val=float(metric_fn(float(th),float(ph)))
            rows.append((float(th),float(ph),val))
            if best is None or val>best[2]:
                best=(float(th),float(ph),val)
    return best, rows
