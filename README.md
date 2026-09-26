# GeQubit-SweetSpot-Finder

Numerical search tools for magnetic-field and control-parameter sweet spots in Ge/SiGe hole-spin qubits.

## Goal
Given an effective g-tensor and one or more control susceptibilities, scan field orientation and identify regions where the qubit frequency is first-order insensitive to noise.

Core quantities include:
\\[
f_Z(\theta,\phi), \qquad
\frac{\partial f_Z}{\partial V_i}, \qquad
\sigma_f^2 = \sum_i \left(\frac{\partial f_Z}{\partial V_i}\sigma_{V_i}\right)^2.
\\]

For Gaussian quasistatic frequency noise, the package uses the convention
\\[
W(t)=\exp[-2\pi^2\sigma_f^2 t^2],
\\]
so \\(T_2^*=1/(\sqrt{2}\pi\sigma_f)\\).

## Quick start
```bash
python -m pip install -e .
python examples/find_angular_sweet_spot.py
pytest
```

## Status
Research prototype using generic synthetic parameters. It is intended for reproducible method development, not device-specific prediction without calibration.

## License
MIT.
