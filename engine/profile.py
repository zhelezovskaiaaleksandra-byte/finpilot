"""Data model for a user's financial profile and goal.

Kept intentionally small for Phase 0: just what the recommendation and
simulator logic actually consume. Fields like country/occupation are
collected because the real product will eventually need them (tax rules,
local investment vehicles), but they're not used in any Phase 0 logic yet —
that's noted inline so it's obvious this isn't an oversight.
"""

from dataclasses import dataclass
from enum import Enum


class InvestmentExperience(str, Enum):
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class RiskTolerance(str, Enum):
    """Self-reported comfort with market swings, not the final risk score.

    The recommendation engine treats this as one input among several — see
    recommendation.py for why it doesn't get the final word.
    """

    VERY_CAUTIOUS = "very_cautious"
    CAUTIOUS = "cautious"
    COMFORTABLE = "comfortable"
    AGGRESSIVE = "aggressive"


class GoalType(str, Enum):
    EMERGENCY_FUND = "emergency_fund"
    HOUSE = "house"
    CAR = "car"
    STUDY_ABROAD = "study_abroad"
    RETIREMENT = "retirement"
    FINANCIAL_INDEPENDENCE = "financial_independence"
    PASSIVE_INCOME = "passive_income"
    LONG_TERM_WEALTH = "long_term_wealth"


GOAL_LABELS = {
    GoalType.EMERGENCY_FUND: "Build an emergency fund",
    GoalType.HOUSE: "Buy a house",
    GoalType.CAR: "Buy a car",
    GoalType.STUDY_ABROAD: "Study abroad",
    GoalType.RETIREMENT: "Retirement",
    GoalType.FINANCIAL_INDEPENDENCE: "Financial independence",
    GoalType.PASSIVE_INCOME: "Passive income",
    GoalType.LONG_TERM_WEALTH: "Long-term wealth",
}


@dataclass
class UserProfile:
    age: int
    country: str
    occupation: str
    monthly_income: float
    monthly_expenses: float
    current_savings: float
    debt_amount: float
    debt_is_high_interest: bool  # e.g. credit card debt, not a mortgage/student loan
    emergency_fund_months: float  # months of expenses currently held as a cash buffer
    investment_experience: InvestmentExperience
    monthly_amount_available: float  # what they can put toward investing each month
    risk_tolerance: RiskTolerance
    investment_horizon_years: float

    @property
    def monthly_surplus(self) -> float:
        return self.monthly_income - self.monthly_expenses


@dataclass
class Goal:
    goal_type: GoalType
    horizon_years: float | None = None  # falls back to profile horizon if not set
    target_amount: float | None = None

    def effective_horizon(self, profile: UserProfile) -> float:
        return self.horizon_years if self.horizon_years is not None else profile.investment_horizon_years
