import numpy as np
from gequbit_sweetspot.core import effective_g, scan_angles

g=np.diag([0.2,0.4,7.5])
best, _ = scan_angles(lambda th,ph: effective_g(g,th,ph), np.linspace(0,180,181), [0.0])
print("Maximum effective g:", best)
