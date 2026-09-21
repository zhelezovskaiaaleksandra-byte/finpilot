# FinPilot — Phase 2

The Phase 0 throwaway prototype (Flask) validated the recommendation logic
with real users and was retired. This is the real (non-throwaway) build,
per the Year 1 plan's Phase 2: a FastAPI app covering the core loop —
profile → goal → recommendation.

**Current scope.** No accounts, no persistence, no real market data. The
interactive simulator (sliders + growth chart) is Phase 3, not built into
this app yet — it's deliberately left out even though the engine already
supports it, so phases stay honest checkpoints. `engine/` is unchanged
from Phase 0: it was already framework-agnostic, so only the web layer
was rebuilt.

For the mission, roadmap, and full Phase 0 testing history, see
[`docs/`](./docs/README.md).

## One-time setup: a proper dev environment

Do this once, now, before making changes — it's a small amount of setup
that saves real pain later. Four pieces, what each one is for:

- **VS Code** — the code editor. Download it from code.visualstudio.com if
  you don't have it, then install the "Python" extension (by Microsoft)
  from the Extensions panel — it gives you error highlighting, a "run"
  button, and a built-in terminal.
- **A virtual environment (venv)** — every Python project you build will
  need its own set of installed packages, sometimes even different
  *versions* of the same package. A venv is a private, isolated folder of
  packages just for this project, so installing something here can never
  break a different project on your machine.
- **Git** — version control. Think of it as an unlimited "save point"
  system for your code: every commit is a snapshot you can always go back
  to, and it tracks exactly what changed and when.
- **GitHub** — a cloud home for your Git history. If your laptop dies, the
  code isn't gone. It's also where a lot of the free hosting services we'll
  use later (Render, Railway) deploy directly from.

Steps, run from inside this unzipped `finpilot-prototype` folder:

```bash
# 1. Open this folder in VS Code (or: code . from the terminal)

# 2. Create the virtual environment (one-time)
python3 -m venv venv

# 3. Activate it (do this every time you start working — your terminal
#    prompt will show "(venv)" when it's active)
source venv/bin/activate

# 4. Install this project's packages *inside* the venv
pip install -r requirements.txt

# 5. Confirm it still runs
python app.py
```

Then set up Git and GitHub:

```bash
# 6. Turn this folder into a Git repository (one-time)
git init
git add .
git commit -m "Phase 0: rule-based recommendation engine + simulator prototype"
```

(Already done for this repo — it's on GitHub. These steps are here for
reference, or for setting up a fresh clone.)

```bash
# 7. On github.com: click "New repository", name it e.g. finpilot,
#    leave it empty (no README/gitignore — we already have one), create it.
#    GitHub will show you a URL like https://github.com/<you>/finpilot.git

# 8. Connect this local repo to it and push
git remote add origin https://github.com/<you>/finpilot.git
git branch -M main
git push -u origin main
```

From now on, the habit is: make a change, `git add .`, `git commit -m "..."`
describing what changed, `git push`. That history becomes genuinely useful
once we're a few phases in and something breaks.

## Running it

```
source venv/bin/activate   # if not already active
python app.py
```

(This runs a Uvicorn server under the hood — `uvicorn app:app --reload`
works the same way and is the more idiomatic FastAPI habit to pick up.)

Then open http://127.0.0.1:5000 in a browser and fill out the form.

**This only runs on your own computer.** A link like
`http://127.0.0.1:5000` means nothing on anyone else's machine — "local"
means it only listens on your laptop, not the internet. A real, permanent
public deploy (Render/Railway/Fly.io, per the Year 1 plan) comes right
after this core loop works, not at the end.

## Running the tests

```
python -m unittest discover -s tests -v
```

21 tests cover the recommendation rules (horizon-vs-comfort, guardrails,
the emergency-fund override), the simulator math (compound interest
correctness against the standard formula, unused by the app for now but
still validated), and the form-parsing helpers in `app.py`.

## How the recommendation logic works

1. **Guardrails first.** High-interest debt and a thin emergency fund
   (< 3 months of expenses) surface as warnings before any portfolio talk —
   standard financial-planning order of operations.
2. **Risk score = the lower of two numbers**: what the user says they're
   comfortable with ("risk willingness") and what their time horizon can
   actually support ("risk capacity"). A short horizon caps an aggressive
   self-rating; a long horizon never overrides a cautious self-rating. The
   explanation shown to the user always says which of the two governed.
3. **Emergency-fund goals always get the Conservative portfolio**,
   regardless of horizon or stated comfort — that money needs to be there
   when needed, not marked down in a downturn.
4. Four fixed model portfolios (Conservative/Balanced/Growth/Aggressive),
   each just an equity/bond/cash split plus an illustrative assumed
   pessimistic/expected/optimistic annual return range for the simulator.
   These return assumptions are **not** backtested or sourced from real
   data — that's explicitly Year 2 scope (financial APIs).

All of this logic lives in `engine/recommendation.py` and
`engine/simulator.py`, independent of any web framework — it moved from
the Phase 0 Flask app into this FastAPI app completely unchanged, and
could equally be driven from a CLI or notebook to sanity-check numbers.

## Known simplifications (deliberate, for now)

- Single risk-tolerance question instead of a real risk-profiling
  questionnaire.
- One investment horizon question total, applied to whichever single goal
  is selected — no multi-goal portfolio yet (see the iteration log below
  for why this used to be two horizon questions and no longer is).
- No interactive simulator in this app yet — the engine math and UI both
  already exist and were validated in Phase 0, just not wired in here.
  That's Phase 3.
- No persistence — refreshing loses your results.
- No dependency on live financial data anywhere.

For how Phase 0 testing was actually run and what it found, see
[`docs/PHASE0_LOG.md`](./docs/PHASE0_LOG.md).

## Iteration log

**2026-09-21 — first round of real user testing.** Feedback was overall
positive; two specific points of confusion came up more than once:

1. Having both a "general investment horizon" question and an optional
   "goal-specific horizon" question read as being asked the same thing
   twice — testers weren't sure which one actually mattered. Fix: dropped
   the goal-specific override from the form entirely; there's now one
   horizon question. (`engine/recommendation.py` still supports a per-goal
   override for later, when the product actually handles multiple
   simultaneous goals — only the form was simplified.)
2. Testers who keep all their money in one undifferentiated savings
   account (common for a young beginner) found it odd to be asked
   separately "how much do you have saved" and "how many months of
   expenses is your emergency fund" — it felt redundant, since they don't
   mentally split their savings into labeled buckets. Fix: removed the
   emergency-fund question from the form; it's now computed from savings
   ÷ expenses (see `_emergency_fund_months` in `app.py`), and the warning
   message shows that arithmetic explicitly so it's clear where the number
   came from, rather than asking the same thing twice in different words.

**2026-09-21 — Phase 0 → Phase 2 migration.** Replaced the throwaway Flask
app with the real FastAPI app described above. `engine/` moved over
unchanged. The simulator (sliders, chart, `/api/simulate`) was
deliberately not carried over yet — Phase 2's definition of done is just
profile → goal → recommendation; the simulator comes back in Phase 3.
All 21 tests kept passing throughout since none of them touch the web
framework directly.
