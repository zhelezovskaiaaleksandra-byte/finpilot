import unittest

from engine.recommendation import MODEL_PORTFOLIOS, RiskBand
from engine.simulator import project_growth, run_scenarios


class ProjectGrowthTest(unittest.TestCase):
    def test_zero_return_and_zero_contribution_leaves_balance_unchanged(self):
        points = project_growth(initial_amount=1000, monthly_contribution=0, annual_return_rate=0, years=5)

        self.assertEqual(points[0].balance, 1000)
        self.assertEqual(points[-1].balance, 1000)

    def test_zero_return_with_contributions_is_simple_sum(self):
        # No growth, so after 2 years of €100/month the balance should just be principal + contributions.
        points = project_growth(initial_amount=500, monthly_contribution=100, annual_return_rate=0, years=2)

        expected = 500 + 100 * 24
        self.assertAlmostEqual(points[-1].balance, expected, places=2)

    def test_positive_return_beats_zero_return(self):
        flat = project_growth(1000, 100, 0.0, 10)
        growing = project_growth(1000, 100, 0.07, 10)

        self.assertGreater(growing[-1].balance, flat[-1].balance)

    def test_known_lump_sum_compound_formula(self):
        # No monthly contribution: should match the standard annual compounding formula
        # FV = P * (1+r)^n at whole-year points.
        principal = 1000
        rate = 0.05
        points = project_growth(principal, 0, rate, 10)

        expected_final = principal * (1 + rate) ** 10
        self.assertAlmostEqual(points[-1].balance, expected_final, delta=1.0)

    def test_partial_final_year_is_included(self):
        points = project_growth(1000, 50, 0.05, 4.5)

        self.assertEqual(points[-1].year, 4.5)


class RunScenariosTest(unittest.TestCase):
    def test_optimistic_beats_expected_beats_pessimistic(self):
        portfolio = MODEL_PORTFOLIOS[RiskBand.GROWTH]
        results = run_scenarios(portfolio, initial_amount=1000, monthly_contribution=200, years=15)

        by_label = {r.label: r.final_balance for r in results}
        self.assertGreater(by_label["optimistic"], by_label["expected"])
        self.assertGreater(by_label["expected"], by_label["pessimistic"])

    def test_returns_three_scenarios(self):
        portfolio = MODEL_PORTFOLIOS[RiskBand.BALANCED]
        results = run_scenarios(portfolio, initial_amount=0, monthly_contribution=100, years=5)

        self.assertEqual({r.label for r in results}, {"pessimistic", "expected", "optimistic"})


if __name__ == "__main__":
    unittest.main()
