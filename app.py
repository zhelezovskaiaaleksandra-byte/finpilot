"""Phase 0 prototype: a deliberately plain Flask app.

The point of this app is NOT the UI — it's to get the recommendation and
simulator logic in front of real people fast and see whether the results
feel right to them. Styling, polish, and account persistence are all
Phase 2+ concerns.

Run with:
    pip install -r requirements.txt
    python app.py
then open http://127.0.0.1:5000
"""

import os

from flask import Flask, jsonify, render_template, request

from engine.profile import (
    Goal,
    GoalType,
    InvestmentExperience,
    RiskTolerance,
    UserProfile,
    GOAL_LABELS,
)
from engine.recommendation import recommend
from engine.simulator import run_scenarios

app = Flask(__name__)


def _profile_from_form(form) -> UserProfile:
    return UserProfile(
        age=int(form["age"]),
        country=form["country"],
        occupation=form["occupation"],
        monthly_income=float(form["monthly_income"]),
        monthly_expenses=float(form["monthly_expenses"]),
        current_savings=float(form["current_savings"]),
        debt_amount=float(form["debt_amount"] or 0),
        debt_is_high_interest=form.get("debt_is_high_interest") == "on",
        emergency_fund_months=float(form["emergency_fund_months"] or 0),
        investment_experience=InvestmentExperience(form["investment_experience"]),
        monthly_amount_available=float(form["monthly_amount_available"]),
        risk_tolerance=RiskTolerance(form["risk_tolerance"]),
        investment_horizon_years=float(form["investment_horizon_years"]),
    )


def _goal_from_form(form) -> Goal:
    horizon = form.get("goal_horizon_years")
    return Goal(
        goal_type=GoalType(form["goal_type"]),
        horizon_years=float(horizon) if horizon else None,
    )


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        goal_types=list(GoalType),
        goal_labels=GOAL_LABELS,
        risk_options=list(RiskTolerance),
        experience_options=list(InvestmentExperience),
    )


@app.route("/results", methods=["POST"])
def results():
    profile = _profile_from_form(request.form)
    goal = _goal_from_form(request.form)

    rec = recommend(profile, goal)
    horizon = goal.effective_horizon(profile)
    scenarios = run_scenarios(
        rec.portfolio,
        initial_amount=profile.current_savings,
        monthly_contribution=rec.suggested_monthly_contribution,
        years=horizon,
    )

    return render_template(
        "results.html",
        profile=profile,
        goal=goal,
        goal_label=GOAL_LABELS[goal.goal_type],
        horizon=horizon,
        rec=rec,
        scenarios=scenarios,
    )


@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """Recomputes scenarios when the user drags a slider, without a full page reload."""
    data = request.get_json()

    from engine.recommendation import MODEL_PORTFOLIOS, RiskBand

    portfolio = MODEL_PORTFOLIOS[RiskBand(int(data["risk_band"]))]
    scenarios = run_scenarios(
        portfolio,
        initial_amount=float(data["initial_amount"]),
        monthly_contribution=float(data["monthly_contribution"]),
        years=float(data["years"]),
    )

    return jsonify({
        "scenarios": [
            {
                "label": s.label,
                "annual_return": s.annual_return,
                "final_balance": s.final_balance,
                "points": [{"year": p.year, "balance": p.balance} for p in s.points],
            }
            for s in scenarios
        ]
    })


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
