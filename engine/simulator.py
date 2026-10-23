"""Compound-interest projection for the interactive simulator.

All returns used here are the illustrative per-portfolio assumptions defined
in recommendation.py, not live or historical market data. Every output of
this module should be shown to users next to a visible reminder that these
are assumptions, not predictions.
"""

from dataclasses import dataclass

from .recommendation import ModelPortfolio


@dataclass
class YearPoint:
    year: int
    balance: float


@dataclass
class ScenarioResult:
    label: str  # "pessimistic" | "expected" | "optimistic"
    annual_return: float
    points: list[YearPoint]
    final_balance: float


def project_growth(
    initial_amount: float,
    monthly_contribution: float,
    annual_return_rate: float,
    years: float,
    every_month: bool = False
) -> list[YearPoint]:
    """Month-by-month compounding, contribution added at the end of each month.

    Returns one point per completed year (plus year 0 = the starting amount)
    so the result is cheap to chart.
    """
    monthly_rate = (1 + annual_return_rate) ** (1 / 12) - 1
    total_months = round(years * 12)

    balance = initial_amount
    points = [YearPoint(year=0, balance=round(balance, 2))]

    for month in range(1, total_months + 1):
        balance = balance * (1 + monthly_rate) + monthly_contribution
        if every_month:
            points.append(YearPoint(year=round(month / 12,2), balance=round(balance, 2)))
        elif month % 12 ==0:
            points.append(YearPoint(year=month//12, balance=round(balance,2)))
            

    # Capture a partial final year if the horizon isn't a whole number of years.
    if total_months % 12 != 0 and not every_month:
        points.append(YearPoint(year=round(years, 1), balance=round(balance, 2)))

    return points


def run_scenarios(
    portfolio: ModelPortfolio,
    initial_amount: float,
    monthly_contribution: float,
    years: float,
) -> list[ScenarioResult]:
    scenarios = [
        ("pessimistic", portfolio.pessimistic_return),
        ("expected", portfolio.expected_return),
        ("optimistic", portfolio.optimistic_return),
    ]
    results = []
    for label, rate in scenarios:
        points = project_growth(initial_amount, monthly_contribution, rate, years)
        results.append(ScenarioResult(
            label=label,
            annual_return=rate,
            points=points,
            final_balance=points[-1].balance,
        ))
    return results
