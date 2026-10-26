# Explain it simply

A drone measures distance to something below it. To turn that into height, we need drone altitude, sensor direction and proof of what surface was seen. A dry-road baseline must use the same vertical reference. If one part is missing, “unknown” is more honest than a precise-looking number.

This project supplies a virtual crossing without flying. A small generated storm fills/drains imaginary storage. Regression predicts depth ten minutes ahead from current and past observations, compared with assuming current depth persists. The 3D view uses actual numerical replay rows; it does not establish a real survey or camera detection. A model can do well in this generator yet fail in a real watershed.

## Ten reviewer questions

1. What is trained? Five ridge coefficients for synthetic ten-minute dip depth.
2. Where are labels from? The storage generator, not real floods.
3. How is leakage avoided? Past-only features and whole unseen test episodes.
4. Baseline? Current noisy gauge as the prediction at t+10.
5. What is σ? First-order geometric measurement uncertainty, separate from forecast error.
6. Why reject GPS? Unknown datums/excessive uncertainty are rejected; GPS is not categorically rejected.
7. Why can LiDAR fail? Its return may not correspond to water surface.
8. Does ESP32 run YOLO? No, only a potential stream source.
9. Can it fly? No, passive receiving only.
10. What makes it real? Surveyed calibration, verified hardware/timing, field data and independent validation.
