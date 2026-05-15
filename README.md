# pareto

The ORIQX hackathon track. Write hardware-agnostic code. The platform measures the tradeoff.

---

## What this is

**pareto** is the starter repo for the ORIQX track at the Idearum hackathon. You write a workload — molecular dynamics, fluid dynamics, density functional theory, or something you design yourself — on top of the `uniqx` SDK. ORIQX's analytics engine produces a Pareto frontier of execution options (CPU, GPU, mixed) with measurable cost, runtime, accuracy, and carbon for each. You pick a point on the frontier, justify it, and run.

The winning team is the one whose algorithm × hardware choice delivers the strongest measurable performance against the baseline, with the clearest reasoning behind the choice.

The platform is hardware-agnostic and vendor-agnostic. Your code does not name a backend. The execution engine extends to QPUs when `preflight()` indicates a measurable advantage — but a strong submission can use only classical hardware.

---

## How `uniqx` fits

You write Python. The SDK traces your operations into an IR graph. You call `preflight()`, read the option table, and pick where on the frontier you want to land:

```python
import os
import uniqx

GATEWAY = os.environ.get("UNIQX_GATEWAY", "api.oriqx.com:443")
uniqx.login(os.environ["UNIQX_API_KEY"], gateway=GATEWAY)  # persists creds to ~/.config/uniqx
client = uniqx.connect(GATEWAY)
module = my_workload(spec)             # traces — does not execute
options = uniqx.preflight(module, client=client)
print(options.summary())                # the Pareto table
choice = options.recommended            # or pick a different option
job_id = uniqx.submit(module, client=client, backend=choice["label"])
result = uniqx.get(job_id, client=client)
```

`options.summary()` prints a table with one row per execution plan: time, cost (USD), max error rate, carbon (g CO₂), and which nodes the engine plans to assign to CPU / GPU / QPU. That table is the artifact the judges read.

---

## Install

Two steps before any code runs: **register**, then **export your API key**.

### 1 · Register and get your API key

1. Open [app.oriqx.com](https://app.oriqx.com) and register with the invite code your organiser handed you (format: `hackathon-<tier>-XXXXXXXX`). A default API key is minted for you automatically — you'll reveal it in step 3.
2. **Confirm registration via the email link** to activate the account — you cannot sign in until you click through.
3. Sign in at [app.oriqx.com](https://app.oriqx.com), open the **Downloads** page in the sidebar, and click **"Lost your key? Regenerate"**. The new key (`uxk_...`) is shown exactly once — copy it immediately. Regenerating rotates the auto-minted default; any open Studio workspaces will need a refresh to pick up the new value.
4. Use that key everywhere: in the wheel-index URL (below) and as the argument to `uniqx.login()` in your code (the first cell of every starter calls it; the key persists to `~/.config/uniqx/credentials.json` so you only need it in env for the very first run).

Full walkthrough: [docs.oriqx.com/getting-started-hackathon](https://docs.oriqx.com/getting-started-hackathon).

### 2 · Export the key and install

```bash
export UNIQX_API_KEY="uxk_...your-key..."

python -m venv .venv && source .venv/bin/activate
pip install --extra-index-url "https://uniqx:${UNIQX_API_KEY}@wheels.oriqx.com/simple/" uniqx
pip install -e ".[all]"                  # pareto + baseline extras (PySCF, SciPy, ASE)
```

The key authenticates two things: pulling the wheel from the private index (URL embedding above), and authenticating every gateway call (passed once to `uniqx.login()` in the first cell of every starter notebook — after that the SDK reads it from `~/.config/uniqx/credentials.json`).

Your organiser will tell you the gateway target. Set it in the same shell when you have it:

```bash
export UNIQX_GATEWAY="<host:port your organiser gave you>"
```

> Treat the API key like a password. The install command embeds it in the URL — don't paste that line into shared logs or screenshots.

> **Prefer the browser?** Open **Studio** from the dashboard instead. The hosted workspace ships with `uniqx` pre-installed and your `UNIQX_API_KEY` already injected as an env var — you can skip step 1.3 and step 2, clone this repo from the Studio terminal, and go straight to `jupyter lab tracks/dft/starter.ipynb`.

---

## Teams

Solo entries are allowed. **Teams of 2–4 are recommended** — algorithm × hardware co-design rewards mixed skills (numerical, systems, domain knowledge), and the Pareto reasoning is easier when two people argue over the table than when one person stares at it. Maximum team size: 5.

Every team member's name goes into `results.json.members`. Pick one *team handle* (lowercase, hyphen-separated, e.g. `pareto-pilots`) that you'll use for the submission directory name and the PR title.

---

## Pick a track

| Track | What you optimize | Starter |
|---|---|---|
| **DFT** | SCF energy + NMR shieldings for a small molecule | [tracks/dft/](tracks/dft/) |
| **CFD** | 2-D Lattice-Boltzmann channel or cavity flow | [tracks/cfd/](tracks/cfd/) |
| **MD** | Harmonic FCC crystal velocity-Verlet (LJ extension scaffolded) | [tracks/md/](tracks/md/) |
| **AIMD** | Ab-initio Molecular Dynamics using RHF and velocity-Verlet | [tracks/AIMD/](tracks/AIMD/) |
| **Bring your own** | Any workload you can defend with a baseline | [examples/INDEX.md](examples/INDEX.md) |

The three pre-defined tracks each ship a working notebook, a NumPy/PySCF baseline, and a problem-extension prompt. The fourth track is open-ended: 15 curated example notebooks (`examples/notebooks/`) plus the full gallery of 60+ at [app.oriqx.com/examples](https://app.oriqx.com/examples) give you starting points for chemistry, quantum simulation, optimization, ML, and finance. Pick what fits your team, bring a baseline, defend your Pareto choice.

You are free to change the workload, the basis, the grid, the integrator — anything. The starter is a floor, not a ceiling.

---

## Judging

Four criteria, weighted equally:

| Criterion | What we look for |
|---|---|
| **Performance** | Wall-clock runtime, numerical accuracy vs. baseline, scalability with problem size |
| **Tradeoff reasoning** | Quality of the justification for your point on the Pareto frontier — read the `preflight()` table, defend your pick |
| **Creativity** | Originality of the algorithm, the parameter choice, or (for self-defined tracks) the workload itself |
| **Robustness** | Code quality, reproducibility, clean submission template |

Full rubric: [docs/judging.md](docs/judging.md).

---

## Submit

Copy [templates/submission/](templates/submission/), fill in `results.json` and `submission.ipynb`, paste your `preflight().summary()` output into `preflight_log.txt`, push a fork, and open a PR against this repo before the deadline.

Schema and walk-through: [docs/submission.md](docs/submission.md).

---

## Help

- 5-minute walkthrough: [docs/quickstart.md](docs/quickstart.md)
- `preflight()` reference: [docs/preflight.md](docs/preflight.md)
- FAQ: [docs/faq.md](docs/faq.md)
- Hackathon support: your organiser's Slack workspace

---

License: MIT. Starter code in this repo is yours to fork, modify, and ship. The `uniqx` SDK installed via the private index remains proprietary and is licensed for hackathon use through your API key.
