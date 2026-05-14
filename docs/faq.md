# FAQ

## Register / install / auth

**What's the full sign-up flow?**
Three steps, in order: (1) register at [app.oriqx.com](https://app.oriqx.com) with the invite code your organiser gave you (`hackathon-<tier>-XXXXXXXX`) — a default API key is auto-minted; (2) confirm the activation email; (3) sign in. If you'll use **Studio** (browser), you're done — the key is already injected into the workspace. If you'll use the SDK locally, open **Downloads** in the sidebar and click **"Lost your key? Regenerate"** to reveal a fresh key (`uxk_...`) once.

**Where do I get an invite code?**
From your hackathon organiser. Without one you cannot register at `app.oriqx.com`.

**Where do I find my API key?**
Two places, depending on path. In **Studio**, the key is already exported as `UNIQX_API_KEY` inside the workspace pod — run `echo $UNIQX_API_KEY` in the terminal to confirm. For local SDK use, open the **Downloads** page (sidebar) and click **"Lost your key? Regenerate"**; the new key is shown once. The legacy `/api-keys` page is admin-only now and is not where regular hackathon users get a key.

**`pip install` says 401 Unauthorized.**
Your `UNIQX_API_KEY` is wrong, expired, or not exported in the current shell. Re-export it and re-run. The install URL embeds the key — be careful not to paste it into shared logs.

**My budget shows $0.**
Either you have not redeemed an invite code, or your tier has exhausted its budget. The dashboard shows the remaining figure. Ping your organiser.

## Connecting

**`connect()` raises `UNAUTHENTICATED` or `PERMISSION_DENIED`.**
You did not pass `api_key=` to `uniqx.connect()`, or the key is wrong. The starter notebooks read it from `UNIQX_API_KEY`; confirm the env var is set in the shell that launched Jupyter (not just in `.bashrc`).

**`connect()` raises `UNAVAILABLE`.**
Confirm `UNIQX_GATEWAY` is set. Production is `api.oriqx.com:443`, staging is `dev-api.oriqx.com:443`. If you're running a local gateway, it's typically `localhost:50050` (no API key required for the local gateway).

**The notebook submits but `get()` times out.**
Default timeout is 300 s. For large workloads pass `timeout=None` or a longer value: `uniqx.get(job_id, client=client, timeout=600)`.

## `preflight()`

**`options.summary()` shows only one row.**
The engine found one viable execution plan for your graph. This is normal for very small workloads. Increase problem size to see more options.

**`options.recommended` is `None`.**
The engine returned no options. This usually means the traced module is empty or the gateway hit an internal error. Check `module.to_text()` is non-trivial and re-run.

**No `qpu` row appears.**
Either the workload has no quantum-amenable structure, or the platform's QPU pool is currently sized to zero for the hackathon. A purely classical submission is fully valid — the hackathon does not require quantum.

## SDK semantics

**`runtime_inputs` complains about length mismatch.**
The traced module's function expects N parameters. You passed M values. Inspect with `module.functions[0].params`. The chemistry modules expect 6 flat lists (exps, coeffs, centers, ang, atom_coords, charges) — see `tracks/dft/starter.ipynb`.

**Can I use NumPy inside `@uniqx.to_module`?**
No. The decorator traces operations into IR; calling NumPy at trace time computes locally and breaks the abstraction. Use `uniqx.ops` for anything inside the decorated function. NumPy is fine in your baseline, your setup code, and your post-processing.

**Can I send precomputed matrices as `runtime_inputs`?**
Yes — that's how `build_lbm_step_module` ships the operator and initial state. The rule is about not bypassing tracing with hidden compute, not about input shapes. Big inputs are slow to serialize; prefer building structure inside the trace when you can.

## Submission

**My PR's CI is failing.**
Run `ruff check tracks/ submissions/` locally. The lint catches the common cases: malformed `results.json`, unexecuted notebook cells, missing `preflight_log.txt`.

**I want to submit multiple variants.**
One PR per team. Put variants under `submissions/<team-handle>/<variant-name>/` and nominate one in the PR description. Others are bonus material.

**Can I submit after the deadline?**
Your PR must be *opened* before the deadline. Pushes to an open PR are accepted up to the close of judging. Cutting it close is a Robustness liability — earlier is better.

## Help that this FAQ does not cover

- Operational status: [status.oriqx.com](https://status.oriqx.com)
- Hackathon support: Slack workspace shared by your organiser
- SDK docs: [docs.oriqx.com](https://docs.oriqx.com)
