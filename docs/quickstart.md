# Quickstart

From zero to a running starter notebook in five minutes.

## 1. Register and get your API key

The order matters. You cannot install or run anything until the account is activated and you have a key.

> **Prefer the browser?** Skip steps 1.3 and 2 — open **Studio** from the dashboard. The hosted workspace already has `uniqx` installed and your `UNIQX_API_KEY` injected as an env var. Clone this repo from the Studio terminal and jump to step 3.

1. Open [app.oriqx.com](https://app.oriqx.com) and **register** with the invite code your organiser handed you (format: `hackathon-<tier>-XXXXXXXX`). A default API key is minted for you automatically when you sign up.
2. **Confirm via the email link** to activate the account. Sign-in is blocked until you click through.
3. Sign in at [app.oriqx.com](https://app.oriqx.com), open the **Downloads** page in the sidebar, and click **"Lost your key? Regenerate"**. The new key (`uxk_...`) is shown exactly once — copy it now. (Regenerating rotates the auto-minted default; any Studio workspaces already running on the old key will need a refresh.)
4. Export the key:

```bash
export UNIQX_API_KEY="uxk_...your-key..."
```

Your organiser will give you the gateway target — set it in the same shell when you have it:

```bash
export UNIQX_GATEWAY="<host:port your organiser gave you>"
```

> Treat the API key like a password. Never paste the install command into shared logs or screenshots — it embeds the key.

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
GATEWAY = os.environ.get("UNIQX_GATEWAY", "api.oriqx.com:443")
uniqx.login(os.environ["UNIQX_API_KEY"], gateway=GATEWAY)  # persists to ~/.config/uniqx
client = uniqx.connect(GATEWAY)
print("connected:", client is not None)
```

`uniqx.login()` writes the key (chmod 0600) to `~/.config/uniqx/credentials.json` and sets the in-process env, so subsequent notebook kernels won't need `UNIQX_API_KEY` in their shell — they pick it up from the credentials file. If `login()` raises `KeyError`, you forgot to `export UNIQX_API_KEY`. If `connect()` raises `UNAUTHENTICATED`, the key is wrong, expired, or your account is not yet email-confirmed — back to step 1.

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
