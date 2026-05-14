# Submission — &lt;your team name&gt;

> Replace this file's contents with your team's write-up. Keep it to one page.

## Team

- Members: ...
- Track: dft | cfd | md | custom

## What we built

One paragraph: the workload, the algorithmic choice you made, and the
problem size you ran at.

## Why this point on the Pareto frontier

Three to six sentences referencing specific numbers from the
`preflight().summary()` output in `preflight_log.txt`. Defend your pick.
If you overrode the recommendation, say why.

## Headline numbers

| Metric | Baseline | Our run | Delta |
|---|---|---|---|
| Wall-clock (s) | ? | ? | ? |
| Accuracy (rel err) | — | ? | ? |
| Cost (USD) | — | ? | — |
| Carbon (g CO₂) | — | ? | — |

## How to reproduce

**In Studio (recommended):** open `submission.ipynb` in your hosted
workspace. `uniqx` is pre-installed and `UNIQX_API_KEY` is already
exported in the pod — run all cells.

**Locally:**

```bash
export UNIQX_API_KEY="..." UNIQX_GATEWAY="..."
pip install --extra-index-url "https://uniqx:${UNIQX_API_KEY}@wheels.oriqx.com/simple/" uniqx
pip install -e ".[all]"
jupyter nbconvert --execute submissions/<team>/submission.ipynb
```

## What we'd do with more time

(Optional.) Stretch ideas, alternative algorithms, known failure modes.
