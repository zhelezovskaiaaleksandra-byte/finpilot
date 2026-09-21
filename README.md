# FinPilot — Phase 0 prototype

This is the throwaway prototype from the Year 1 plan's Phase 0: a small local
web app to test whether the recommendation logic and simulator math actually
feel right to a real beginner, before any real frontend investment happens.

**It is not the product.** No accounts, no persistence, no styling budget,
no real market data. If Phase 0 goes well, this UI gets thrown away — the
`engine/` package underneath it (the actual rules) is the part meant to
survive into Phase 2.

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

Then open http://127.0.0.1:5000 in a browser. Fill out the form, submit,
and drag the sliders on the results page.

**This only runs on your own computer.** `python app.py` starts what's
called a local development server — "local" means it only listens on your
laptop, not the internet, so a link like `http://127.0.0.1:5000` means
nothing on anyone else's machine. There's no real link to send yet. For
Phase 0 testing, the best option is actually the low-tech one: sit next to
each tester with your own laptop and watch them use it — that's also how
you catch the hesitations and confused pauses that matter most (see
"What to actually test with people" below). If you need to test with
someone remote, a free tool called `ngrok` can temporarily expose your
local server as a real public link for the length of your laptop session,
without any real deployment — worth reaching for only if in-person testing
genuinely isn't possible, since it's one more tool to learn for a prototype
that gets thrown away. Deploying this for real, with a permanent public
address, is Phase 4 work, not now.

## Running the tests

```
python -m unittest discover -s tests -v
```

16 tests cover the recommendation rules (horizon-vs-comfort, guardrails,
the emergency-fund override) and the simulator math (compound interest
correctness against the standard formula).

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
`engine/simulator.py`, independent of Flask — so it can be lifted into a
FastAPI backend in Phase 2 largely unchanged, or driven from a CLI or
notebook to sanity-check numbers.

## What to actually test with people

The point of Phase 0 isn't "does the app work" (the tests cover that) —
it's "does this feel right and useful to a beginner." When you show this
to your 5–10 test people, useful questions:

- Does the *explanation* for the recommendation make sense, or does it feel
  like a black box even though it's shown in plain language?
- Does the split between "risk capacity" (horizon-based) and "risk
  willingness" (self-reported) make sense to them, or is it confusing that
  their own stated risk tolerance can get overridden?
- Do the guardrail warnings (debt, emergency fund) feel helpful, or
  preachy/annoying?
- Playing with the simulator sliders — does moving "horizon" or "risk
  level" change the outcome in a way that builds intuition, or does it
  just feel like a toy?
- Where did they hesitate, re-read something, or ask you a question out
  loud while using it? Those moments are the actual signal.

Write down what breaks. That list is the direct input to Phase 1/2 scoping
in the Year 1 plan.

## Known simplifications (deliberate, for Phase 0 only)

- Single risk-tolerance question instead of a real risk-profiling
  questionnaire.
- One investment horizon question total, applied to whichever single goal
  is selected — no multi-goal portfolio yet (see the iteration log below
  for why this used to be two horizon questions and no longer is).
- No persistence — refreshing loses your results.
- Chart is a small hand-rolled inline SVG, not a charting library — this
  environment couldn't reach any CDN to verify one would load, and for
  three lines on a chart it wasn't worth the external dependency anyway.
- No dependency on live financial data anywhere.

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
