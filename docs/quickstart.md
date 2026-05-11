# Quickstart

From zero to a running starter notebook in five minutes.

## 1. Register and get your API key

The order matters. You cannot install or run anything until the account is activated and you have a key.

1. Open [app.oriqx.com](https://app.oriqx.com) and **register** with the invite code your organiser handed you (format: `hackathon-<tier>-XXXXXXXX`).
2. **Confirm via the email link** to activate the account. Sign-in is blocked until you click through.
3. Sign in at [app.oriqx.com](https://app.oriqx.com), open the **API keys** page, click **Generate new key**. The key (`uxk_...`) is shown exactly once — copy it now.
4. Export both:

```bash
export UNIQX_API_KEY="uxk_...your-key..."
export UNIQX_GATEWAY="api.oriqx.com:443"
```

> Treat the key like a password. Never paste the install command into shared logs or screenshots — it embeds the key.

## 2. Clone and install

```bash
git clone https://github.com/oriqx/pareto
cd pareto
python -m venv .venv && source .venv/bin/activate

# Install uniqx from the private wheel index, then this repo + baseline extras
pip install --extra-index-url "https://uniqx:${UNIQX_API_KEY}@wheels.oriqx.com/simple/" uniqx
pip install -e ".[all]"
```

Verify:

```python
import os
import uniqx

print("uniqx", uniqx.__version__)
client = uniqx.connect(
    os.environ["UNIQX_GATEWAY"],
    api_key=os.environ["UNIQX_API_KEY"],
)
print("connected:", client is not None)
```

If `connect()` raises `UNAUTHENTICATED`, your key is wrong, expired, or your account is not yet email-confirmed. Go back to step 1.

## 3. Run a starter notebook

Pick a track and launch Jupyter:

```bash
jupyter lab tracks/dft/starter.ipynb     # or cfd / md
```

Run all cells. The notebook will:

1. Build a traced module from the problem specification.
2. Call `uniqx.preflight()` and print the option table.
3. Submit the recommended option and fetch the result.
4. Compare against the NumPy/PySCF baseline.

Expected wall-clock for the DFT starter (H₂O / STO-3G): under 30 seconds end-to-job.

## 4. Modify, measure, justify

Change the problem size, the algorithm, the precision, or the time horizon. Re-run `preflight()` and watch how the Pareto frontier moves. Save the most interesting option's `summary()` output — that goes into your submission.

## 5. Submit

Copy `templates/submission/` into a fork of this repo, fill in the placeholders, and open a pull request. See [submission.md](submission.md) for the schema.
