# FinPilot — Phase 0 Log

*Started 2026-08-30. Companion to `PROJECT_BRIEF.md` and `YEAR1_PLAN.md`.*

## What was built

A local Flask prototype implementing the full Phase 0 loop: profile form → goal selection → rule-based recommendation → interactive compound-interest simulator with a live-updating chart.

Architecture: business logic (`engine/recommendation.py`, `engine/simulator.py`, `engine/profile.py`) is framework-agnostic and unit-tested. The Flask layer (`app.py` + Jinja templates) is intentionally throwaway — the `engine/` package is what's meant to carry into Phase 2.

## Key rule-engine decisions

- Risk score = min(risk capacity from time horizon, self-reported risk willingness) — a short horizon caps an aggressive self-rating, but a long horizon never overrides someone who says they're cautious. The reasoning behind whichever number wins is always shown to the user, not just the resulting number.
- Guardrails (high-interest debt, thin emergency fund) surface as warnings before any portfolio talk, not blockers.
- Goal type "emergency fund" always forces the Conservative portfolio, regardless of computed risk score — that money needs to be reliably there, not exposed to a downturn.
- Four fixed model portfolios (Conservative/Balanced/Growth/Aggressive) with hand-set illustrative pessimistic/expected/optimistic annual return assumptions — explicitly not backtested or sourced from real market data (that's Year 2 scope).

## Round 1 of real user testing (2026-09-21)

Shown to a handful of people in the target audience (students / first-time investors). Feedback was overall positive; two specific points of confusion came up more than once:

1. **Two horizon questions read as one question asked twice.** The form had both a "general investment horizon" and an optional "goal-specific horizon" override. Testers weren't sure which one actually mattered.
   **Fix:** dropped the goal-specific override from the form entirely. There's now one horizon question. (The engine layer still supports a per-goal override for later, when the product handles multiple simultaneous goals — only the form was simplified.)

2. **Asking for "savings" and "emergency fund" separately felt redundant.** Testers who keep everything in one undifferentiated savings account (common for a young beginner) don't mentally split their money into labeled buckets, so being asked for both felt like the same question twice.
   **Fix:** removed the emergency-fund-months form field. It's now computed from savings ÷ monthly expenses, and the resulting warning message shows that arithmetic explicitly (e.g. *"Based on your €900 in savings and €900/month in expenses, that's about 1.0 months of expenses covered..."*) so it's transparent rather than mysterious — and it teaches the underlying concept for free, instead of assuming the user already thinks in those terms.

Both fixes verified with unit tests (21/21 passing) and a visual check before shipping.

## Next step

This round of feedback has been addressed. Rather than loop Phase 0 testing indefinitely — the core concept already tested positively — next is Phase 1/2: starting the real (non-throwaway) build, per `YEAR1_PLAN.md`.
