# GeQubit-SweetSpot-Finder

GeQubit-SweetSpot-Finder is a research-oriented Python toolkit for identifying and characterizing **magnetic-field and control-parameter sweet spots in Ge/SiGe hole-spin qubits**.

A sweet spot is a region of parameter space where a qubit observable—most commonly the qubit transition frequency—becomes weakly sensitive to fluctuations in one or more control parameters.

The central question addressed by this repository is:

> Given an anisotropic spin response and a set of noisy control parameters, where should the device be operated to reduce first-order dephasing while retaining useful qubit control?

---

## 1. Physical motivation

In a hole-spin qubit, the Zeeman energy generally depends on the full (g)-tensor and the magnetic-field direction.

For magnetic-field magnitude (B) and unit vector (mathbf n),

[
f_Z
=
rac{mu_B B}{h}
left|
mathbf g mathbf n
ight|.
]

Because the (g)-tensor itself may depend on gate voltages, confinement, strain, and electric field, voltage fluctuations can shift the qubit frequency.

For gate (V_i),

[
delta f_Z
approx
rac{partial f_Z}{partial V_i}delta V_i.
]

A first-order electrical sweet spot approximately satisfies

[
rac{partial f_Z}{partial V_i}approx0
]

for one or more dominant noisy controls.

The same concept can be extended to angular sensitivity, barrier sensitivity, detuning sensitivity, or any differentiable model parameter.

---

## 2. Current capabilities

The package currently provides:

- spherical magnetic-field direction generation,
- effective (g)-factor evaluation,
- Zeeman-frequency calculation,
- central finite-difference derivatives,
- 2D angular gradients,
- 2D angular Hessians,
- grid-based angular scans,
- ranking of candidate sweet spots,
- covariance-aware frequency-noise estimates,
- Gaussian quasistatic (T_2^*),
- simple robustness scores.

---

## 3. Mathematical framework

### 3.1 Magnetic-field direction

The magnetic-field unit vector is parameterized as

[
mathbf n(	heta,phi)
=
egin{pmatrix}
sin	hetacosphi\
sin	hetasinphi\
cos	heta
end{pmatrix}.
]

The effective (g)-factor is

[
g_{mathrm{eff}}(	heta,phi)
=
|mathbf gmathbf n|.
]

Then

[
f_Z(	heta,phi)
=
rac{mu_B B}{h}
g_{mathrm{eff}}(	heta,phi).
]

### 3.2 Angular gradient

For an observable (F(	heta,phi)),

[

abla_Omega F
=
left(
rac{partial F}{partial	heta},
rac{partial F}{partialphi}
ight).
]

The current implementation estimates these derivatives with centered finite differences.

A small gradient indicates local first-order angular insensitivity.

### 3.3 Angular Hessian

The Hessian is

[
H=
egin{pmatrix}
partial^2F/partial	heta^2 &
partial^2F/partial	hetapartialphi\
partial^2F/partialphipartial	heta &
partial^2F/partialphi^2
end{pmatrix}.
]

The Hessian helps distinguish broad robust operating regions from narrow extrema.

### 3.4 Multi-gate electrical noise

For sensitivity vector (mathbf s) and voltage covariance matrix (mathbf C),

[
sigma_f
=
sqrt{mathbf s^Tmathbf Cmathbf s}.
]

The Gaussian quasistatic Ramsey convention used here gives

[
T_2^*
=
rac{1}{sqrt{2}pisigma_f}.
]

This allows correlated gate noise to be treated explicitly.

---

## 4. Repository structure

```text
GeQubit-SweetSpot-Finder/
├── README.md
├── pyproject.toml
├── examples/
│   ├── example.py
│   └── robust_sweetspot_demo.py
├── src/
│   └── gequbit_sweetspot/
│       ├── __init__.py
│       ├── core.py
│       ├── optimization.py
│       └── robustness.py
├── tests/
│   ├── test_core.py
│   └── test_optimization.py
└── .github/
    └── workflows/
        └── tests.yml
```

---

## 5. Installation

```bash
git clone https://github.com/premathul/GeQubit-SweetSpot-Finder.git
cd GeQubit-SweetSpot-Finder
python -m pip install -e .
```

Development installation:

```bash
python -m pip install -e .[dev]
pytest -q
```

---

## 6. Example: angular Zeeman scan

```python
import numpy as np
from gequbit_sweetspot.optimization import frequency_from_g

g = np.diag([0.25, 0.35, 8.0])
B = 0.5

for theta in np.linspace(0, 90, 10):
    f = frequency_from_g(g, B, theta, 0.0)
    print(theta, f / 1e9)
```

---

## 7. Example: angular derivatives

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

The finite-difference step is a numerical parameter and should be convergence-tested.

---

## 8. What constitutes a sweet spot?

The repository deliberately does not impose a single universal definition.

Possible definitions include:

- minimum (|partial f/partial V|),
- minimum total (sigma_f),
- maximum (T_2^*),
- minimum angular gradient,
- a stationary point of (f_Z),
- maximum coherence subject to a minimum Rabi frequency,
- maximum coherence subject to an exchange-coupling constraint,
- minimum sensitivity across several gates simultaneously.

This distinction matters because a point that is optimal for one noise source may not be optimal for the total experimental noise budget.

---

## 9. Robustness versus optimality

A very sharp maximum in (T_2^*) can be experimentally less useful than a slightly lower but broad plateau.

For that reason, the code includes derivative and curvature tools.

A robust operating point should ideally be characterized by:

- value of the target metric,
- first derivatives,
- second derivatives,
- uncertainty in the model parameters,
- sensitivity to angular misalignment,
- sensitivity to gate calibration,
- sensitivity to fabrication variation.

Future versions will formalize multi-objective optimization around these quantities.

---

## 10. Numerical validation

Current automated checks include:

- exact effective (g)-factor values for diagonal tensors,
- finite-difference gradients of known analytic functions,
- finite-difference Hessians of quadratic functions,
- candidate ranking behavior,
- positive covariance-derived noise,
- positive finite (T_2^*).

---

## 11. Units

Typical units are:

- (B): tesla,
- (f_Z): hertz,
- voltage sensitivity: hertz/volt,
- voltage noise: volts,
- angular derivatives: hertz/degree in the current helper functions,
- (T_2^*): seconds.

Care is required when comparing degree-based numerical derivatives with analytical derivatives written in radians.

---

## 12. Scientific limitations

The current implementation assumes the supplied (g)-tensor and susceptibilities are already meaningful representations of the device.

It does not yet derive them from:

- self-consistent electrostatics,
- confinement wavefunctions,
- multiband semiconductor Hamiltonians,
- strain,
- microscopic disorder,
- atomistic interfaces.

Therefore the sweet-spot search is only as physically reliable as the model supplied to it.

---

## 13. Planned development

### Near-term

- full ((	heta,phi)) heat maps,
- periodic handling of (phi),
- local optimization after coarse grid search,
- uncertainty-aware ranking,
- confidence regions around sweet spots,
- per-gate dephasing contributions,
- CSV/JSON result export.

### Intermediate

- multi-objective optimization,
- (T_1) and (T_2^*) joint optimization,
- control-speed constraints,
- alignment-error Monte Carlo,
- gate-noise covariance inference,
- automatic finite-difference convergence studies.

### Long-term

The intended workflow is

[
g(V_i,	heta,phi)
ightarrow
f_Z
ightarrow

abla_V f_Z
ightarrow
S_V(f)
ightarrow
W(t)
ightarrow
T_2^*
ightarrow
	ext{robust operating point}.
]

---

## 14. Relationship to other repositories

This project is designed to complement:

- **GeHoleQubit-Simulator** for confinement and (g)-tensor modeling,
- **QuantumDot-Noise-Lab** for detailed noise spectra and filter-function calculations,
- **GeDQD-Exchange-Simulator** for exchange-related sweet spots in double quantum dots.

The long-term goal is interoperability rather than duplicate implementations.

---

## 15. Reproducibility

A reported sweet spot should ideally include:

- (g)-tensor,
- magnetic-field magnitude,
- angle convention,
- angular grid,
- derivative step size,
- voltage-noise amplitudes,
- covariance matrix,
- optimization metric,
- code commit,
- uncertainty model.

A single angle without this context is generally insufficient for reproducibility.

---

## 16. Contributing

Useful contributions include:

- alternative optimization methods,
- uncertainty propagation,
- analytical derivatives,
- visualization,
- experimental alignment models,
- benchmark cases,
- documentation,
- physically motivated example data.

Every new metric should define exactly what is being optimized and in what units.

---

## 17. License

MIT License.

---

## 18. Project status

**Status:** active research development.

The current code can already search and analyze synthetic angular sweet spots. The long-term objective is a robust, uncertainty-aware operating-point optimizer for realistic Ge/SiGe hole-spin-qubit devices.
