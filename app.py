"""Phase 2: the real (non-throwaway) FastAPI app.

Replaces the Phase 0 Flask prototype. The `engine/` package underneath is
unchanged — it was already framework-agnostic — only the web layer moved.

Scope for this milestone: profile -> goal -> recommendation, per the Year 1
plan's Phase 2 definition of done. The interactive simulator (sliders +
chart) is Phase 3 — deliberately left out here even though the engine
support for it already exists, so the phases stay honest checkpoints
rather than one big rebuild.

Run with:
    pip install -r requirements.txt
    python app.py
then open http://127.0.0.1:5000
"""

import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from engine.profile import (
    Goal,
    GoalType,
    InvestmentExperience,
    RiskTolerance,
    UserProfile,
    GOAL_LABELS,
)
from engine.recommendation import recommend

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _emergency_fund_months(current_savings: float, monthly_expenses: float) -> float:
    """How many months of expenses the user's savings would cover.

    Phase 0 testing showed people found it confusing to be asked for this
    directly right after already being asked for savings and expenses — it
    read as the same question twice. It isn't a separate fact someone
    usually knows off the top of their head anyway; it's arithmetic on two
    numbers we already collected, so we do that arithmetic instead of asking
    again. If they have no ongoing expenses to speak of, there's no burn
    rate to protect against, so we don't warn.
    """
    if monthly_expenses <= 0:
        return 99.0
    return current_savings / monthly_expenses


def _profile_from_form(form) -> UserProfile:
    monthly_expenses = float(form["monthly_expenses"])
    current_savings = float(form["current_savings"])

    return UserProfile(
        age=int(form["age"]),
        country=form["country"],
        occupation=form["occupation"],
        monthly_income=float(form["monthly_income"]),
        monthly_expenses=monthly_expenses,
        current_savings=current_savings,
        debt_amount=float(form["debt_amount"] or 0),
        debt_is_high_interest=form.get("debt_is_high_interest") == "on",
        emergency_fund_months=_emergency_fund_months(current_savings, monthly_expenses),
        investment_experience=InvestmentExperience(form["investment_experience"]),
        monthly_amount_available=float(form["monthly_amount_available"]),
        risk_tolerance=RiskTolerance(form["risk_tolerance"]),
        investment_horizon_years=float(form["investment_horizon_years"]),
    )


def _goal_from_form(form) -> Goal:
    # Phase 0 testing showed a second, goal-specific horizon question next to
    # the general one read as redundant rather than useful — people weren't
    # sure which one actually mattered. Dropped for now; every goal just uses
    # the one horizon answer. (The engine still supports a per-goal override
    # for when the product actually has multiple simultaneous goals.)
    return Goal(goal_type=GoalType(form["goal_type"]))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "goal_types": list(GoalType),
            "goal_labels": GOAL_LABELS,
            "risk_options": list(RiskTolerance),
            "experience_options": list(InvestmentExperience),
        },
    )


@app.post("/results", response_class=HTMLResponse)
async def results(request: Request):
    form = await request.form()
    profile = _profile_from_form(form)
    goal = _goal_from_form(form)

    rec = recommend(profile, goal)
    horizon = goal.effective_horizon(profile)

    return templates.TemplateResponse(
        request,
        "results.html",
        {
            "profile": profile,
            "goal": goal,
            "goal_label": GOAL_LABELS[goal.goal_type],
            "horizon": horizon,
            "rec": rec,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), reload=True)
