import unittest

from app import _emergency_fund_months, _goal_from_form, _profile_from_form
from engine.profile import GoalType


def make_form(**overrides) -> dict:
    """A plain dict works here: the code only ever uses form[...] and form.get(...),
    both of which a normal dict supports, so no need to pull in Flask's request context
    just to test this parsing logic."""
    defaults = dict(
        age="22",
        country="Spain",
        occupation="Student",
        monthly_income="1200",
        monthly_expenses="900",
        current_savings="1800",
        debt_amount="0",
        investment_experience="beginner",
        monthly_amount_available="150",
        risk_tolerance="comfortable",
        investment_horizon_years="10",
        goal_type="long_term_wealth",
    )
    defaults.update(overrides)
    return defaults


class EmergencyFundMonthsTest(unittest.TestCase):
    def test_computes_months_of_expenses_covered(self):
        self.assertAlmostEqual(_emergency_fund_months(1800, 900), 2.0)

    def test_zero_expenses_does_not_divide_by_zero(self):
        # No ongoing expenses means no burn rate to protect against, so this
        # should not raise ZeroDivisionError or produce a warning-triggering value.
        self.assertGreaterEqual(_emergency_fund_months(500, 0), 3)


class ProfileFromFormTest(unittest.TestCase):
    def test_emergency_fund_is_derived_not_asked(self):
        """The form no longer has an emergency_fund_months field at all —
        confirms the profile still gets a sensible value computed from
        savings and expenses instead of KeyError-ing."""
        form = make_form(current_savings="2700", monthly_expenses="900")
        profile = _profile_from_form(form)

        self.assertAlmostEqual(profile.emergency_fund_months, 3.0)

    def test_missing_debt_amount_defaults_to_zero(self):
        form = make_form(debt_amount="")
        profile = _profile_from_form(form)

        self.assertEqual(profile.debt_amount, 0)


class GoalFromFormTest(unittest.TestCase):
    def test_goal_has_no_standalone_horizon_field_anymore(self):
        """Goal-specific horizon was removed from the form after user testing
        showed it read as a confusing duplicate of the general horizon
        question — the goal should always fall back to the profile's horizon."""
        form = make_form(goal_type="house")
        goal = _goal_from_form(form)

        self.assertEqual(goal.goal_type, GoalType.HOUSE)
        self.assertIsNone(goal.horizon_years)


if __name__ == "__main__":
    unittest.main()
