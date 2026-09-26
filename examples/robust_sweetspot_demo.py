import numpy as np
from gequbit_sweetspot.optimization import frequency_from_g, central_gradient_2d

g=np.diag([0.25,0.35,8.0])
B=0.5
f=lambda th,ph: frequency_from_g(g,B,th,ph)
for th in (0,30,60,90):
    grad=central_gradient_2d(f,th,0,step_deg=0.05)
    print(f"theta={th:3d} deg  f={f(th,0)/1e9:8.3f} GHz  |grad|={np.linalg.norm(grad)/1e6:8.3f} MHz/deg")
