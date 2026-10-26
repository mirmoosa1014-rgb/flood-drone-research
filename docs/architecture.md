# Architecture

`core.py` is the single source of truth for generated hydrology, causal features, model training, replay and measurement gates. It uses standard-library arithmetic and seeded PRNGs. JSON stores coefficients; no uploaded serialized executable model is loaded.

`api.py` exposes FastAPI health, scenario and telemetry endpoints. `server.py` supplies a dependency-free HTTP alternative using the same engine. Documented launches bind to loopback. The frontend requests a bounded complete replay and renders timeline/3D geometry; interaction cannot alter hidden truth. No endpoint controls a vehicle.

`telemetry.py` optionally receives passive MAVLink and outputs normalized JSON. It preserves boot and receive timestamps. It does not automatically fuse asynchronous packets: an operator must establish timing, surveyed datum, uncertainty, baseline and return validity before submitting `/api/telemetry`.

The road is a parabolic transect with dip at zero local elevation. Hydrology `truth_m` is dip depth and illustrative water-plane elevation. At other positions, `local_truth_depth_m=max(0,water_surface-road)`. Geometry estimates local-point depth, which differs from dip-depth forecast. Sample clocks are seconds (`minute*60`).

The canvas rotates a 3D coordinate system, projects into 2D and paints numerical road polygons, water plane, airframe and beam. Horizontal axes are metres; vertical is exaggerated ×3. The airframe is illustrative. SVG chart values come from engine data.

Camera configuration validates HTTP(S) and creates a browser link. The backend never fetches it. There is no server-side URL proxy or invented vision output.

Bounds: 120 replay steps; seed 0–2^31−1; storm multiplier .2–3; fallback telemetry body below 10kB. Intended for local single-user use, not a public authenticated service.
