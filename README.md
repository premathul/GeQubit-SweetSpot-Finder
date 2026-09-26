# GeQubit-SweetSpot-Finder

GeQubit-SweetSpot-Finder is a research software project for identifying, characterizing, and comparing robust operating points in germanium hole-spin qubits. The central focus is the search for magnetic-field orientations and electrical operating conditions where the qubit becomes less sensitive to fluctuations in its environment while preserving a useful spin response. Rather than treating a “sweet spot” as a single angle or a single optimized number, the project treats sweet-spot identification as a local sensitivity problem that should be described by gradients, curvatures, noise covariance, and robustness against experimental misalignment.

This distinction is important for Ge/SiGe hole-spin qubits because their spin response can be strongly anisotropic. The effective Zeeman splitting depends on the magnetic-field direction through the (g)-tensor, and the (g)-tensor can itself depend on gate voltages and confinement. Consequently, a magnetic-field angle that produces a favorable qubit frequency may not be the same angle that minimizes electrical dephasing. Similarly, a mathematically exact optimum may be extremely narrow and therefore experimentally fragile. The purpose of this repository is to provide tools that can distinguish between these different notions of optimality.

For a magnetic field of magnitude (B) pointing along a unit vector (mathbf n(	heta,phi)), the effective qubit frequency is modeled as

[
f_Z(	heta,phi)
=
rac{mu_B B}{h}
left|
mathbf g mathbf n(	heta,phi)
ight|,
]

with

[
mathbf n(	heta,phi)=
egin{pmatrix}
sin	hetacosphi\
sin	hetasinphi\
cos	heta
end{pmatrix}.
]

The angular dependence enters directly through the anisotropic (g)-tensor. This allows the code to scan the full magnetic-field sphere rather than restricting the analysis to a single plane.

The repository provides numerical derivatives with respect to (	heta) and (phi). If an observable (F(	heta,phi)) is being optimized, its first-order angular sensitivity is represented by

[

abla_Omega F
=
left(
rac{partial F}{partial	heta},
rac{partial F}{partialphi}
ight).
]

A point with a small gradient is locally insensitive to small angular errors. However, first derivatives alone are not sufficient to describe robustness. The code therefore also evaluates the angular Hessian,

[
H=
egin{pmatrix}
rac{partial^2F}{partial	heta^2} &
rac{partial^2F}{partial	hetapartialphi}\
rac{partial^2F}{partialphipartial	heta} &
rac{partial^2F}{partialphi^2}
end{pmatrix},
]

which contains information about local curvature. A broad plateau and a sharp extremum may both have zero gradient at the exact optimum, but their Hessians are very different. For experiment, that difference can be decisive.

The package also supports electrical-noise analysis. If the qubit frequency depends on several noisy control voltages, then the first-order frequency fluctuation is

[
delta f
approx
sum_i
rac{partial f}{partial V_i}delta V_i.
]

With sensitivity vector (mathbf s) and voltage covariance matrix (mathbf C_V), the frequency-noise standard deviation is

[
sigma_f=
sqrt{mathbf s^Tmathbf C_Vmathbf s}.
]

For Gaussian quasistatic noise, the corresponding dephasing time is

[
T_2^*=
rac{1}{sqrt{2}pisigma_f}.
]

This formulation means that the optimization is not restricted to independent gates. Correlated fluctuations can be represented directly through off-diagonal covariance terms.

The repository is organized around a small set of transparent modules. The `core.py` file contains basic effective-(g) and scanning utilities. The `optimization.py` file contains angular direction generation, Zeeman-frequency evaluation, numerical gradients, Hessians, and ranking of candidate operating points. The `robustness.py` file contains covariance-aware noise estimates and simple robustness metrics. Example scripts demonstrate how these functions can be combined, and the automated test suite verifies derivative accuracy against analytical functions and checks expected behavior for synthetic tensors.

Installation is straightforward:

```bash
git clone https://github.com/premathul/GeQubit-SweetSpot-Finder.git
cd GeQubit-SweetSpot-Finder
python -m pip install -e .
```

For development and testing,

```bash
python -m pip install -e .[dev]
pytest -q
```

A simple magnetic-field scan can be performed using

```python
import numpy as np
from gequbit_sweetspot.optimization import frequency_from_g

g = np.diag([0.25, 0.35, 8.0])
B = 0.5

for theta in np.linspace(0, 90, 10):
    f = frequency_from_g(g, B, theta, 0.0)
    print(theta, f / 1e9)
```

The parameters in this example are synthetic. They are intended to illustrate anisotropy and should not be interpreted as the calibrated response of a specific device.

A local angular sensitivity can be evaluated numerically with

```python
from gequbit_sweetspot.optimization import central_gradient_2d

f = lambda theta, phi: frequency_from_g(g, B, theta, phi)

gradient = central_gradient_2d(
    f,
    theta_deg=45.0,
    phi_deg=0.0,
    step_deg=0.05,
)

print(gradient)
```

The finite-difference step is itself a numerical parameter. In serious calculations it should be varied to confirm convergence. Too large a step can smear local structure, while too small a step can amplify floating-point noise or numerical noise in an externally supplied frequency model.

A key principle of this project is that there is no universally correct definition of a sweet spot. One device may be limited by plunger-gate noise, another by barrier-gate noise, and another by angular misalignment or magnetic-field drift. A point may maximize (T_2^*) while simultaneously reducing the Rabi frequency or exchange controllability. For that reason, the project is moving toward multi-objective optimization rather than a single scalar maximum. In a realistic design problem, one may want to maximize coherence while requiring a minimum drive strength, a minimum exchange coupling, or a maximum allowed sensitivity to fabrication variation.

The current code deliberately separates candidate generation from scientific interpretation. A grid search can identify the largest value of a chosen metric, but that point should not automatically be labeled the “best” operating point without considering local curvature and uncertainty. In future versions, candidate regions will be characterized by angular confidence areas, parameter uncertainty, and tolerance to calibration errors. This is especially important for experiments because a narrow optimum that requires sub-degree alignment may be less useful than a slightly lower but much broader region.

The present implementation does not derive the (g)-tensor from first principles. It assumes that the tensor, or a frequency model built from it, has already been obtained from experiment or from a separate device simulation. This design is intentional. The project is meant to serve as the optimization layer between a physics model and an experimental operating decision. In the future, it will interface more directly with the GeHoleQubit-Simulator repository so that (g)-tensor and susceptibility calculations can be fed into the sweet-spot search automatically.

Another planned connection is to QuantumDot-Noise-Lab. The current (T_2^*) calculation assumes quasistatic Gaussian frequency noise. Real semiconductor devices can exhibit (1/f) noise, random telegraph signals, broadband noise, and gate-to-gate correlations that depend on frequency. A more complete workflow will replace a single covariance matrix with a frequency-dependent cross-spectral-density matrix (S_{ij}(f)). At that point the sweet-spot problem becomes a filter-function-weighted noise optimization rather than only a first-order quasistatic calculation.

The long-term architecture is therefore

[
g(V_i,	heta,phi)
ightarrow
f_Z
ightarrow

abla_V f_Z
ightarrow
S_{ij}(f)
ightarrow
W(t)
ightarrow
T_2^*
ightarrow
	ext{robust operating region}.
]

The phrase “operating region” is intentional. Experimental robustness is usually more meaningful when expressed as a finite region of acceptable performance rather than as a single mathematically optimal coordinate.

Reproducibility is an important part of the project. A reported sweet spot should include the exact (g)-tensor or frequency model, magnetic-field magnitude, angular convention, angular grid, derivative step size, voltage-noise assumptions, covariance matrix, optimization metric, and Git commit. Reporting only a field angle without the model and conventions is generally insufficient for independent reproduction.

The current test suite verifies effective-(g) values for diagonal tensors, numerical gradients and Hessians against analytical functions, ranking logic, positive covariance-derived noise, and finite positive dephasing times. Additional tests will be added as optimization methods become more sophisticated.

The project is suitable for synthetic studies, method development, comparison of operating strategies, and post-processing of device simulations. It should not be interpreted as a complete predictive model unless the supplied (g)-tensor, noise model, and control susceptibilities have been independently validated for the device of interest.

## Contact

**Athul Prem**

For questions, scientific discussion, collaboration, or suggestions concerning the project, please contact Athul Prem through the GitHub account associated with this repository.
