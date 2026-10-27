# Evaluation

Full run: 80 training episodes; 20 untouched test episodes (1000–1019); 20 untouched intense-storm OOD episodes (2000–2019, rain ×2.5). Each test episode has 105 origins, minutes 5–109. Ridge/persistence use identical observations and t+10 targets. Synthetic labels are not field data.

Held-out ridge MAE .0229703 m versus persistence .0607601 m; OOD .0580498 m versus .1570011 m. Absolute-error p95 is .0628846/.1888031 m. Across-episode MAE standard deviation is .0026376/.0216499 m. Source: `results/metrics.json`.

`results/predictions.csv` has 4,200 origins with split/seed/prediction/persistence/truth/error. `results/demo.json` drives example replay. SVG/PNG derive from saved outputs. Forecast curves shift ten minutes to valid target time.

Failure case: intense-storm tails grow substantially. This OOD stress changes forcing intensity but preserves underlying model family; shared assumptions may favor the learned model. No operational warning recall, actual lead-time benefit, trained vision performance or field-detection metric is claimed.

Checks: 28 unit/API/HTTP tests; TypeScript/Vite build; quick/full benchmarks; live loopback HTTP and browser interaction checks after Linux recovery. Original Mac sandbox denied socket launch and lacked Chromium. Linux loopback HTTP and headless-shell Chromium work. The full Chrome executable fails on sandbox AF_UNIX restrictions; the supported headless-shell binary ran the app interaction tests and generated a real screenshot. CI execution, hardware and camera validation remain pending.


The Data Signal presentation revision preserves all numerical evaluation outputs. Its TypeScript/Vite build passes. Expanded UI/export/mobile/reduced-motion checks are pending because Mac Chrome aborts under the current sandbox. Earlier browser passes describe the earlier UI. The Visual QA workflow provides a reproducible Linux capture route; it has not been executed for this revision.
