"""Rule-based recommendation engine.

Deliberately not machine learning — see the Year 1 plan for why. Every
number in here is a hand-set rule, which means every recommendation can be
explained by pointing at the specific rule that fired. That traceability is
the point: a beginner user (and a regulator) should be able to see exactly
why a given portfolio was suggested.

The design has two stages that are kept separate on purpose:

1. Guardrails — checks that run before any portfolio talk (high-interest
   debt, no emergency fund). These are about financial hygiene, not asset
   allocation, and the industry-standard advice is that they come first.
2. Portfolio selection — maps a risk score to one of four fixed model
   portfolios. The risk score is the *lower* of what the user says they're
   comfortable with and what their time horizon can actually support,
   because a short horizon doesn't leave room to recover from a bad year
   no matter how much volatility someone claims to tolerate.
"""

from dataclasses import dataclass
from enum import Enum

from .profile import Goal, GoalType, RiskTolerance, UserProfile


class RiskBand(int, Enum):
    CONSERVATIVE = 1
    BALANCED = 2
    GROWTH = 3
    AGGRESSIVE = 4


@dataclass(frozen=True)
class ModelPortfolio:
    band: RiskBand
    name: str
    equity_pct: int
    bond_pct: int
    cash_pct: int
    # Illustrative annual return assumptions per scenario, NOT a forecast.
    # These are simplified planning ranges for a Phase 0 prototype, not
    # backtested or sourced from live market data — that's Year 2 scope.
    pessimistic_return: float
    expected_return: float
    optimistic_return: float


MODEL_PORTFOLIOS: dict[RiskBand, ModelPortfolio] = {
    RiskBand.CONSERVATIVE: ModelPortfolio(
        RiskBand.CONSERVATIVE, "Conservative", equity_pct=20, bond_pct=70, cash_pct=10,
        pessimistic_return=0.01, expected_return=0.03, optimistic_return=0.05,
    ),
    RiskBand.BALANCED: ModelPortfolio(
        RiskBand.BALANCED, "Balanced", equity_pct=50, bond_pct=40, cash_pct=10,
        pessimistic_return=0.00, expected_return=0.05, optimistic_return=0.09,
    ),
    RiskBand.GROWTH: ModelPortfolio(
        RiskBand.GROWTH, "Growth", equity_pct=75, bond_pct=20, cash_pct=5,
        pessimistic_return=-0.02, expected_return=0.07, optimistic_return=0.12,
    ),
    RiskBand.AGGRESSIVE: ModelPortfolio(
        RiskBand.AGGRESSIVE, "Aggressive", equity_pct=90, bond_pct=10, cash_pct=0,
        pessimistic_return=-0.05, expected_return=0.08, optimistic_return=0.15,
    ),
}

_WILLINGNESS_BY_TOLERANCE = {
    RiskTolerance.VERY_CAUTIOUS: RiskBand.CONSERVATIVE,
    RiskTolerance.CAUTIOUS: RiskBand.BALANCED,
    RiskTolerance.COMFORTABLE: RiskBand.GROWTH,
    RiskTolerance.AGGRESSIVE: RiskBand.AGGRESSIVE,
}


@dataclass
class Guardrail:
    severity: str  # "warning" | "info"
    message: str


@dataclass
class Recommendation:
    portfolio: ModelPortfolio
    risk_capacity: RiskBand
    risk_willingness: RiskBand
    governing_factor: str  # "horizon" | "stated comfort" | "goal override"
    guardrails: list[Guardrail]
    explanation: str
    suggested_monthly_contribution: float


def _risk_capacity_from_horizon(years: float) -> RiskBand:
    """Longer time horizons can absorb more volatility, independent of temperament."""
    if years < 3:
        return RiskBand.CONSERVATIVE
    if years < 7:
        return RiskBand.BALANCED
    if years < 15:
        return RiskBand.GROWTH
    return RiskBand.AGGRESSIVE


def _check_guardrails(profile: UserProfile) -> list[Guardrail]:
    guardrails: list[Guardrail] = []

    if profile.debt_is_high_interest and profile.debt_amount > 0:
        guardrails.append(Guardrail(
            severity="warning",
            message=(
                "You have high-interest debt. Paying that down typically beats expected "
                "market returns, since the interest rate on the debt is a guaranteed cost — "
                "consider prioritizing it before investing significant amounts."
            ),
        ))

    if profile.emergency_fund_months < 3:
        guardrails.append(Guardrail(
            severity="warning",
            message=(
                f"Based on your €{profile.current_savings:.0f} in savings and €{profile.monthly_expenses:.0f}/month "
                f"in expenses, that's about {profile.emergency_fund_months:.1f} months of expenses covered as an "
                "emergency fund. Most guidance suggests 3-6 months of essential expenses in cash before investing "
                "meaningfully, so a market downturn doesn't force you to sell investments at a bad time."
            ),
        ))

    if profile.monthly_surplus <= 0:
        guardrails.append(Guardrail(
            severity="warning",
            message=(
                "Your reported monthly expenses meet or exceed your income, which leaves no surplus "
                "to invest. It may be worth revisiting the budget before committing to a monthly contribution."
            ),
        ))

    return guardrails


def recommend(profile: UserProfile, goal: Goal) -> Recommendation:
    guardrails = _check_guardrails(profile)

    risk_capacity = _risk_capacity_from_horizon(goal.effective_horizon(profile))
    risk_willingness = _WILLINGNESS_BY_TOLERANCE[profile.risk_tolerance]

    if goal.goal_type == GoalType.EMERGENCY_FUND:
        # Emergency-fund money needs to be there when you need it, not marked down
        # in a downturn — this overrides everything else regardless of horizon or comfort.
        final_band = RiskBand.CONSERVATIVE
        governing_factor = "goal override"
    elif risk_capacity.value <= risk_willingness.value:
        final_band = risk_capacity
        governing_factor = "horizon"
    else:
        final_band = risk_willingness
        governing_factor = "stated comfort"

    portfolio = MODEL_PORTFOLIOS[final_band]
    explanation = _build_explanation(
        profile, goal, portfolio, risk_capacity, risk_willingness, governing_factor
    )

    return Recommendation(
        portfolio=portfolio,
        risk_capacity=risk_capacity,
        risk_willingness=risk_willingness,
        governing_factor=governing_factor,
        guardrails=guardrails,
        explanation=explanation,
        suggested_monthly_contribution=max(profile.monthly_amount_available, 0),
    )


def _build_explanation(
    profile: UserProfile,
    goal: Goal,
    portfolio: ModelPortfolio,
    risk_capacity: RiskBand,
    risk_willingness: RiskBand,
    governing_factor: str,
) -> str:
    horizon = goal.effective_horizon(profile)

    if governing_factor == "goal override":
        return (
            f"Because this money is earmarked as your emergency fund, we're recommending the "
            f"{portfolio.name} portfolio regardless of your stated risk comfort or time horizon — "
            "an emergency fund needs to be reliably there when you need it, not exposed to a "
            "market downturn."
        )

    if governing_factor == "horizon":
        if risk_capacity.value < risk_willingness.value:
            return (
                f"You said you're comfortable with more risk, but this goal is only {horizon:.0f} "
                f"years away, so we capped the recommendation at {portfolio.name}. A shorter time "
                "horizon doesn't leave much room to recover from a bad year in the markets."
            )
        return (
            f"With a {horizon:.0f}-year horizon and your stated comfort with risk, "
            f"the {portfolio.name} portfolio ({portfolio.equity_pct}% equities / "
            f"{portfolio.bond_pct}% bonds / {portfolio.cash_pct}% cash) balances growth potential "
            "against how much time you have to ride out ups and downs."
        )

    return (
        f"Your {horizon:.0f}-year horizon could technically support more risk, but you told us "
        f"you're more cautious than that, so we're recommending {portfolio.name} "
        f"({portfolio.equity_pct}% equities / {portfolio.bond_pct}% bonds / {portfolio.cash_pct}% cash). "
        "It's your money and your comfort that set the ceiling here, not just the math."
    )
