# Hardware integration boundary

Supplied context describes Pixhawk 2.4.8, ESP8266/MAVESP8266, TF-Luna and ESP32-CAM with regulated PDB rail. Only roles were adopted. Connector views, pin numbering, colors, clone variants, voltage compatibility and current budgets were not checked physically; this is not a verified wiring manual.

[ArduPilot Benewake documentation](https://ardupilot.org/copter/docs/common-benewake-tf02-lidar.html), consulted 2026-10-25, lists TF-Luna nominal .2–8 m range and current serial type 27, unlike dossier type 20. It uses metre-based `RNGFND1_MIN/MAX` rather than assuming old `_CM` names. Installed firmware may differ. No parameters are written by this app.

[MAVLink definitions](https://mavlink.io/en/messages/common.html) specify `GLOBAL_POSITION_INT.alt` as MSL millimetres; `relative_alt` is relative to home. Neither automatically matches surveyed NAVD88. Normalization preserves distinctions. Real depth requires common datum, stable altitude reference, lever-arm correction and uncertainty budget.

`DISTANCE_SENSOR` orientation 25 is downward; other orientations are marked unusable. Centimetres convert to metres; timing is preserved. No guesses about surface validity or asynchronous fusion are made. Projection assumes rigid downward mounting and a locally planar reflecting surface. First-order σ combines independent altitude/range/baseline/attitude errors; it is not a calibrated statistical coverage guarantee.

Water reflectance/transmission, foam, rain, incidence angle and optical windows can invalidate interpretation. These are uncharacterized here. A single range does not prove water-surface depth, so unvalidated returns are rejected by default. This is a conservative engineering requirement, not a tested detector claim.

[Espressif esp32-camera](https://github.com/espressif/esp32-camera) supports acquisition/streaming. This software does not include or claim ESP32-side YOLOv8s-seg. Future host-side segmentation needs labeled data, held-out evaluation and explicit failures.

Custom PVC/acrylic does not establish waterproof rating, motor rain tolerance, window performance, strength, endurance or thrust. The displayed quadcopter is illustrative; motor directions and pins are not certified.

Optional passive receiver: install hardware requirements, then `python -m flood_drone.telemetry --port 14550`. It listens on loopback and prints normalized JSON; a separately configured local router must forward the hardware stream. No arm, parameter, motor-test, mission-upload or flight commands are sent.
