import unittest

from engine.profile import (
    Goal,
    GoalType,
    InvestmentExperience,
    RiskTolerance,
    UserProfile,
)
from engine.recommendation import RiskBand, recommend


def make_profile(**overrides) -> UserProfile:
    defaults = dict(
        age=25,
        country="Spain",
        occupation="Analyst",
        monthly_income=2000,
        monthly_expenses=1400,
        current_savings=3000,
        debt_amount=0,
        debt_is_high_interest=False,
        emergency_fund_months=4,
        investment_experience=InvestmentExperience.BEGINNER,
        monthly_amount_available=300,
        risk_tolerance=RiskTolerance.COMFORTABLE,
        investment_horizon_years=10,
    )
    defaults.update(overrides)
    return UserProfile(**defaults)


class HorizonCapsRiskTest(unittest.TestCase):
    def test_short_horizon_caps_aggressive_stated_risk(self):
        """A 2-year horizon should override an 'aggressive' self-rating."""
        profile = make_profile(risk_tolerance=RiskTolerance.AGGRESSIVE, investment_horizon_years=2)
        goal = Goal(goal_type=GoalType.CAR)

        rec = recommend(profile, goal)

        self.assertEqual(rec.portfolio.band, RiskBand.CONSERVATIVE)
        self.assertEqual(rec.governing_factor, "horizon")

    def test_long_horizon_respects_cautious_stated_risk(self):
        """A 20-year horizon should NOT push a self-described cautious investor into Aggressive."""
        profile = make_profile(risk_tolerance=RiskTolerance.VERY_CAUTIOUS, investment_horizon_years=20)
        goal = Goal(goal_type=GoalType.LONG_TERM_WEALTH)

        rec = recommend(profile, goal)

        self.assertEqual(rec.portfolio.band, RiskBand.CONSERVATIVE)
        self.assertEqual(rec.governing_factor, "stated comfort")

    def test_matched_horizon_and_comfort_uses_horizon_band(self):
        profile = make_profile(risk_tolerance=RiskTolerance.COMFORTABLE, investment_horizon_years=10)
        goal = Goal(goal_type=GoalType.LONG_TERM_WEALTH)

        rec = recommend(profile, goal)

        self.assertEqual(rec.portfolio.band, RiskBand.GROWTH)
        self.assertEqual(rec.governing_factor, "horizon")


class GoalOverrideTest(unittest.TestCase):
    def test_emergency_fund_goal_always_conservative(self):
        """Even a young, aggressive, long-horizon user gets Conservative for an emergency fund goal."""
        profile = make_profile(risk_tolerance=RiskTolerance.AGGRESSIVE, investment_horizon_years=30)
        goal = Goal(goal_type=GoalType.EMERGENCY_FUND)

        rec = recommend(profile, goal)

        self.assertEqual(rec.portfolio.band, RiskBand.CONSERVATIVE)
        self.assertEqual(rec.governing_factor, "goal override")


class GuardrailTest(unittest.TestCase):
    def test_high_interest_debt_triggers_warning(self):
        profile = make_profile(debt_amount=2000, debt_is_high_interest=True)
        goal = Goal(goal_type=GoalType.LONG_TERM_WEALTH)

        rec = recommend(profile, goal)

        messages = [g.message for g in rec.guardrails]
        self.assertTrue(any("high-interest debt" in m for m in messages))

    def test_low_emergency_fund_triggers_warning(self):
        profile = make_profile(emergency_fund_months=0.5)
        goal = Goal(goal_type=GoalType.LONG_TERM_WEALTH)

        rec = recommend(profile, goal)

        messages = [g.message for g in rec.guardrails]
        self.assertTrue(any("emergency fund" in m for m in messages))

    def test_healthy_profile_has_no_guardrail_warnings(self):
        profile = make_profile(debt_amount=0, emergency_fund_months=6)
        goal = Goal(goal_type=GoalType.LONG_TERM_WEALTH)

        rec = recommend(profile, goal)

        self.assertEqual(rec.guardrails, [])

    def test_negative_surplus_triggers_warning(self):
        profile = make_profile(monthly_income=1000, monthly_expenses=1200)
        goal = Goal(goal_type=GoalType.LONG_TERM_WEALTH)

        rec = recommend(profile, goal)

        messages = [g.message for g in rec.guardrails]
        self.assertTrue(any("surplus" in m for m in messages))


class GoalHorizonOverrideTest(unittest.TestCase):
    def test_goal_specific_horizon_overrides_profile_horizon(self):
        """A goal with its own horizon (e.g. a car in 2 years) should use that, not the profile default."""
        profile = make_profile(investment_horizon_years=20, risk_tolerance=RiskTolerance.AGGRESSIVE)
        goal = Goal(goal_type=GoalType.CAR, horizon_years=2)

        rec = recommend(profile, goal)

        self.assertEqual(rec.portfolio.band, RiskBand.CONSERVATIVE)


if __name__ == "__main__":
    unittest.main()
