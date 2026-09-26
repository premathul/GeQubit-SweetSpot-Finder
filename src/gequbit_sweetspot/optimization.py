import numpy as np

def angular_direction(theta_deg, phi_deg):
    t,p=np.deg2rad([theta_deg,phi_deg])
    return np.array([np.sin(t)*np.cos(p),np.sin(t)*np.sin(p),np.cos(t)])

def frequency_from_g(g_tensor, B_t, theta_deg, phi_deg, mu_b_over_h_hz_t=13.99624555e9):
    n=angular_direction(theta_deg,phi_deg)
    geff=np.linalg.norm(np.asarray(g_tensor,float)@n)
    return mu_b_over_h_hz_t*B_t*geff

def central_gradient_2d(fn, theta_deg, phi_deg, step_deg=1e-2):
    if step_deg<=0: raise ValueError("step_deg must be positive")
    dt=(fn(theta_deg+step_deg,phi_deg)-fn(theta_deg-step_deg,phi_deg))/(2*step_deg)
    dp=(fn(theta_deg,phi_deg+step_deg)-fn(theta_deg,phi_deg-step_deg))/(2*step_deg)
    return np.array([dt,dp],float)

def central_hessian_2d(fn, theta_deg, phi_deg, step_deg=1e-2):
    h=step_deg
    if h<=0: raise ValueError("step_deg must be positive")
    f0=fn(theta_deg,phi_deg)
    ftt=(fn(theta_deg+h,phi_deg)-2*f0+fn(theta_deg-h,phi_deg))/h**2
    fpp=(fn(theta_deg,phi_deg+h)-2*f0+fn(theta_deg,phi_deg-h))/h**2
    ftp=(fn(theta_deg+h,phi_deg+h)-fn(theta_deg+h,phi_deg-h)-fn(theta_deg-h,phi_deg+h)+fn(theta_deg-h,phi_deg-h))/(4*h**2)
    return np.array([[ftt,ftp],[ftp,fpp]],float)

def rank_sweet_spots(metric_grid, theta_grid, phi_grid, top_n=10, maximize=True):
    arr=np.asarray(metric_grid,float)
    if arr.shape!=(len(theta_grid),len(phi_grid)):
        raise ValueError("metric_grid shape mismatch")
    flat=np.argsort(arr.ravel())
    if maximize: flat=flat[::-1]
    out=[]
    for idx in flat[:top_n]:
        i,j=np.unravel_index(idx,arr.shape)
        out.append({"theta_deg":float(theta_grid[i]),"phi_deg":float(phi_grid[j]),"metric":float(arr[i,j])})
    return out
