# Model card

Version 1: five-coefficient ridge regression, ten-minute horizon. Artifact `models/hydrology.json` embeds schema and training seeds.

Features at t: intercept, current noisy gauge depth, current rain/100, five-minute gauge change and ten available rain intensities summed/1000. No future forcing, gauge, truth or episode seed is a feature. Negative predictions clip to zero.

Training uses 80 whole episodes (seeds 0–79). Each varies runoff factor, drainage, storm peak and width. Target: dip depth at t+10. Fixed penalty .1 applies to non-intercept coefficients, without test tuning. Normal equations use partial pivoting. This small demonstration is not a general high-dimensional learner.

Generator depth increment is rain converted from mm/h to m/min times runoff times illustrative concentration factor 25, minus proportional drainage per one-minute step. Initial storage is .01 m. There is no terrain-resolved hydrodynamics, calibrated gauge transfer or real watershed. Spatial geometry is an illustrative road profile rather than a hydraulic flow solver.

No learned prediction interval is claimed. Dashboard measurement σ belongs to the separate geometry projection, not forecast confidence. OOD error increases; no real road-access decisions should use outputs.

The app loads shipped JSON; if absent, it deterministically retrains the same small model. Malformed artifacts fail rather than executing code. Uploaded models are not accepted.
