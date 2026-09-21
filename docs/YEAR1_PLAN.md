# FinPilot — Year 1 Plan

*Drafted 2026-08-30. Companion to `PROJECT_BRIEF.md`.*

## Why this differs from a naive "build an MVP" plan

Taken literally, "build an MVP, learn web development, build a recommendation engine, build a simulator" is four separate hard problems tackled at once by someone who hadn't built a web app before, alongside a full Economics course load — a recipe for a half-finished app in twelve months, not a working one.

The plan below keeps the same destination but reorders and narrows it: validate the idea cheaply before writing production code, learn only the tools needed to ship the actual MVP (not a general web-dev curriculum), and cut everything that isn't the core loop. The AI assistant, real financial-market APIs, and ML all correctly stay out of Year 1.

## Phase 0 — Prove the logic before building the app (weeks 1–3)

Before any real frontend work: build the recommendation logic and the simulator math as a throwaway prototype, not production code. The goal is to answer one question fast: does the actual recommendation logic (profile + goals + risk → portfolio) produce results that feel right to a real beginner? Show it to 5–10 people in the target audience and watch where they get confused.

This phase is deliberately disposable. Skipping it is the single most common way solo builders waste months building a polished interface around logic nobody has validated.

**Status: done.** Prototype built (Flask + a framework-agnostic `engine/` package, unit-tested), tested locally, and shown to real people. First round of feedback surfaced two points of confusion (a redundant horizon question, a redundant emergency-fund question) — both fixed the same day. Full detail in `PHASE0_LOG.md`.

## Phase 1 — Learn exactly enough to build the MVP (months 1–3, overlapping Phase 0)

Not "learn web development" in the abstract — learn the specific slice this MVP needs, in this order: HTML/CSS fundamentals, enough JavaScript to make a form interactive and drive a chart, a backend framework, Git/GitHub, and how to deploy a small app (Render, Railway, or Fly.io all have workable free tiers).

**Stack:** Python on the backend (FastAPI), server-rendered HTML templates (Jinja2) rather than a JavaScript framework like React, plain JavaScript for the interactive simulator, and Postgres (via a hosted free tier like Supabase or Neon) for storage. Reasoning: Python is what I'm already building fluency in through statistics and, later, ML coursework, so the backend work directly compounds with my degree. A server-rendered app avoids also learning React/state management/build tooling in year one — real complexity that buys nothing yet, since this MVP has no need for a rich single-page app. This can be rebuilt in React/Next.js later if the product needs it — plenty of real products never do.

## Phase 2 — Core loop v1: profile, goals, recommendation (months 3–6)

Build the real (not prototype) version of: the profile form, the goals selection step, and a rule-based recommendation engine that maps risk tolerance + investment horizon + goal to one of a small fixed set of model portfolios (e.g. Conservative / Balanced / Growth / Aggressive), each expressed as ETF-category weights (equity/bond/cash splits by category, not individual stock picks). Each result ships with a plain-language explanation of *why* that portfolio was chosen — this explanation is as much the deliverable as the number.

Definition of done: a user can fill out their profile and goals and get back a recommended allocation with an explanation, running on a deployed URL, even if the rest of the site is ugly.

## Phase 3 — Interactive simulator (months 6–9)

Add the sliders (contribution, horizon, expected return, risk level) and the optimistic/expected/pessimistic scenario chart, driven by compound-interest math. Use fixed, clearly-labeled assumed return ranges per risk band — not live market data (that's Year 2) and not a forecast. Every screen showing projected numbers should say plainly that these are illustrative assumptions, not predictions or guarantees.

## Phase 4 — Education layer, polish, real users (months 9–12)

Add lightweight glossary/tooltip explanations for the core concepts (ETF, diversification, inflation, volatility, index funds, bonds) surfaced in context rather than as a separate wiki. Polish the onboarding flow based on what confused people in Phase 0. Add basic persistence so a returning user sees their saved profile and results. Then get it in front of real users outside my immediate circle and write down what breaks — that list becomes the input to Year 2 planning.

## Explicitly out of scope for Year 1

No AI assistant or LLM chat (Year 3). No live financial-market APIs — Year 1 uses static assumed returns (Year 2). No machine learning of any kind. No mobile app. No real user accounts tied to payment or bank data. No connection to actual brokerage execution.

## One thing to decide early, not late

Software that recommends a specific asset allocation to a named individual can brush up against investment-advice regulation in many jurisdictions, even with no execution attached. This doesn't block building the MVP, but two cheap habits from day one reduce the risk: frame output as *educational/illustrative*, never as "advice" or "you should," in both the UI copy and any internal naming; and add a visible disclaimer on every recommendation and simulator screen.

## Deploy early, not just at the end

My main goal for this project is a deployed, demoable product for my job-hunting portfolio (primarily a full-time role after graduation, with a possible summer internship search as an earlier soft checkpoint). That means a rough, ugly, but genuinely live version should go up right after Phase 2 (the core recommendation loop working), not wait for Phase 4 polish — a free host like Render or Railway is enough. Every phase after that redeploys the improved version.

## Year 1 exit criteria

A deployed, public, working web app where a stranger can complete profile → goals → recommendation → simulator → basic education, end to end, without me explaining anything to them. Real feedback collected from people outside my circle. Codebase clean enough that Year 2 (financial APIs, database growth, first ML) is an extension, not a rewrite.
