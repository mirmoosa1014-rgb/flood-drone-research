# Data Signal design

## Source and revision

Adapted from **Motion Graphic Style Library → Data Signal**, style id `signal`, library `motionstyle_signal`, upstream revision **ab7faf2be3e17350f5c6c7e78dfb53d1792ae9cc**. Source: `catalog/signal.md`; exported `signal.css` and `signal.json`. The exported CSS is copied verbatim into `frontend/src/motion-theme.css` and imported by the application stylesheet. The complete MIT license is retained in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

## Instrument layout

The application is a dense telemetry console, not a promotional landing page. A connection/quality strip identifies the local API, synthetic replay source, disconnected hardware, selected-return quality and selected clock time. Horizontal Observatory / Hardware / Evidence tabs replace the old sidebar. A large time-aligned depth plot is paired with a rainfall signal, a geometric return instrument and an explicit measurement/rejection ledger. The ledger shows the actual selected replay rows; it never replaces unknown depth with zero.

Numbers use the mono stack. Every quantitative readout carries a unit or a labeled column. The forecast plot is target-time-aligned; its readout remains the issued +10-minute prediction. The observation is local transect depth, distinct from dip depth, and this distinction is stated directly below the plot. No simulated source is presented as connected hardware.

## Tokens

All surface, type, shape and timing tokens come from the exported CSS:

| Role | Token / value |
|---|---|
| Canvas | `--bg` / `#070B16` |
| Raised / surface | `#101828` / `#0E1728` |
| Text / muted text | `#E7F0FA` / `#8AA0B8` |
| Primary signal | `#3EE0FF` |
| Forecast / comparison | `#7AA2FF` |
| Observation / selected-time annotation | `#FFB020` |
| Invalid quality | `#FF5D73` |
| Grid / border | `#17304A` |
| Radius | `8px` |
| Shadows / blur | `none` / `0px` |

Display uses Helvetica Neue / Helvetica / Arial, weight 600, tracking −.030em. Body uses the same stack at 450, tracking 0, line height 1.4. Mono uses SF Mono / ui-monospace / Menlo / Consolas at 600, tracking .020em and compact line height 1.1. There is no added palette, decorative glow, gradient or AI logo. The faint grid is confined to quantitative plots and geometry.

## Motion and adaptations

`line_draw` uses stroke offset 1→0 over **0.9s**, `cubic-bezier(0.65, 0, 0.35, 1)`. It runs only on a newly mounted scenario plot; scrub/play updates the cursor without restarting line drawing. `tick_in` uses opacity 0→1 over **0.25s**, `cubic-bezier(0.16, 1, 0.3, 1)`, with the source **0.06s** stagger on repeated horizontal tick labels. There are no springs.

The source is a narrated motion-graphics style with count-up and idle pulses. In this scientific interface those are intentionally omitted: numbers show real measurements instantly, and no chart moves unless the user requests replay or changes the scenario. This avoids invented intermediate values and ambient activity that might be confused with incoming telemetry. `prefers-reduced-motion: reduce` disables reveal animations entirely; all series and ticks remain visible. Explicit Play/Pause and direct orbit gestures remain user-controlled operations.

The source's fixed 1920×1080 video canvas and 96px safe area are adapted to a responsive application. At 390px the instruments stack, the ledger keeps its numeric fields while hiding the verbose reason column, and current rejection reasons remain available in the return-quality block. The physical projection, data model, time alignment, simulation, telemetry APIs and benchmark outputs are unchanged. Only canvas/SVG appearance changes.

## Evidence and checks

Strict TypeScript/Vite build passes. The SVG evidence panel and PNG research figure were restyled from existing saved outputs; no training or experiment was rerun. Backend source, model and result-file hashes remain unchanged.

The redesigned UI's browser smoke script checks numerical readout against the API, replay play/pause, minute-52 rejection, 3D orbit, storm refresh, exported JSON, Hardware/Evidence tabs, camera link, 390px overflow and reduced-motion styles. It captures desktop, 390px mobile and reduced-motion screenshots. Local Mac Chrome launches abort under the current OS sandbox, so those revised browser checks and revised app screenshots are **not claimed passed locally**. The prior implementation's capture is retained separately as historical evidence, not presented as the redesigned interface.

To run the deterministic captures on a normal Linux machine: Python 3.11+, Node 24; run `npm ci`, `npm run build`, and `npx playwright install --with-deps chromium` in `frontend`, then `python3 scripts/visual_qa.py` from the project root. The script starts and cleans up its own loopback backend. `.github/workflows/visual-qa.yml` runs this sequence on `design/**` branch pushes, pull requests and manual dispatch, and uploads the captures as artifacts. No GitHub push or workflow execution was performed for this revision.
