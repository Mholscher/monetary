#    Copyright 2023 Menno Hölscher
#
#    This file is part of monetary.

#    monetary is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    monetary is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.

#    You should have received a copy of the GNU Lesser General Public License
#    along with monetary.  If not, see <http://www.gnu.org/licenses/>.
""" This module contains code to determine the value of financial instruments.

The IFRS rule 9 gives 2 options for the calculation, the rule to always
use the original and/or latest recognition, or to determine the fair value
based on the expected return. The latter one is for financial institutions,
so here we will always valuate on the latest recognition. See the
individual instrument calculation to see how this pans out for the different
financial instruments.
"""

from monetary_models.interests import Interest


class LoanValue:
    """The class holds the liability value for one or more periods.

    From the input that is very similar to the interest calculation
    input the totals are calculated. It can also be used to project
    a value for a future period.

    The input is a period list, with each period a history period or
    a future period. History periods are formatted:

        :from_date: The start date of this period
        :to_date: The day after the end of the period
        :principal: The amount of the principal in the smallest denomination (like cents or pennies)
        :interest_posted: The interest posted in the period

    Future periods are formatted:

        :from_date: The start date of this period
        :to_date: The day after the end of the period
        :start_balance: The amount of the principal at start of the period in the smallest denomination (like cents or pennies)
        :interest_frac: The interest percentage as a fraction in the period

    For discounting you can enter discount factors. The factors are defined as:

        :date_factor: The date for which the factor is valid
        :factor: A fraction with which an amount is to be discounted on that date

    You can pass in None, than there will be no discounting of future amounts.
    If there is one factor, it will be taken as a constant, and each amount
    to be received after the date_factor will be discounted by the factor.
    You can pass in more factors, the factors will be interpolated between the
    dates and beyond the last date the factor will be constant (i.e. the value
    for the highest date). Before the lowest date, no discounting will be done.
    """

    def __init__(self, period_data, discount_factors=None):
        self.period_list = period_data
        self.discount_factors = discount_factors

    def posted_interest(self):
        """Calculate the total interest from the list of periods"""

        posted_periods = [
            period for period in self.period_list if "interest_posted" in period
        ]
        total_interest = 0
        for period in posted_periods:
            total_interest += period["interest_posted"]
        return total_interest

    def repayment(self):
        """Calculate repayment of principal for the periods

        The repayment is taken as the difference between the principals
        in consecutive periods.
        """

        posted_periods = [
            period for period in self.period_list if "principal" in period
        ]
        if posted_periods:
            if self.discount_factors:
                discounted_sum = 0
                for period_no, calculation_period in enumerate(posted_periods):
                    if period_no > 0:
                        undiscounted = (
                            posted_periods[period_no - 1]["principal"]
                            - posted_periods[period_no]["principal"]
                        )
                        discounted_sum += self._discount_repayment(
                            undiscounted,
                            posted_periods[period_no]["from_date"],
                            posted_periods[period_no],
                        )
            else:
                discounted_sum = (
                    posted_periods[0]["principal"] - posted_periods[-1]["principal"]
                )
            return discounted_sum
        return 0

    def _discount_repayment(self, repayment_amount, at_date, period):
        """Discount a future principal repayment"""

        date_factors = [
            date_factor
            for date_factor in self.discount_factors.keys()
            if date_factor <= period["from_date"]
        ]
        if date_factors:
            applicable_key = max(date_factors)
            if applicable_key == at_date:
                repayment_amount = round(
                    repayment_amount * (1 - self.discount_factors[applicable_key])
                )
            else:
                larger_dates = [
                    date_factor
                    for date_factor in self.discount_factors.keys()
                    if date_factor > period["from_date"]
                ]
                if not larger_dates:
                    repayment_amount = round(
                        repayment_amount * (1 - self.discount_factors[applicable_key])
                    )
                else:
                    next_key = min(larger_dates)
                    factor = self.discount_factors[applicable_key] + (
                        at_date - applicable_key
                    ) * (
                        self.discount_factors[next_key]
                        - self.discount_factors[applicable_key]
                    ) / (
                        next_key - applicable_key
                    )
                    repayment_amount = repayment_amount - round(
                        repayment_amount * factor
                    )
        return repayment_amount

    def _discount_interest(self, interest_amount, at_date, period):
        """Discount an interest amount"""

        date_factors = [
            date_factor
            for date_factor in self.discount_factors.keys()
            if date_factor <= period["from_date"]
        ]
        if date_factors:
            applicable_key = max(date_factors)
            if applicable_key == at_date:
                interest_amount = round(
                    interest_amount * (1 - self.discount_factors[applicable_key])
                )
            else:
                larger_dates = [
                    date_factor
                    for date_factor in self.discount_factors.keys()
                    if date_factor > period["from_date"]
                ]
                if not larger_dates:
                    interest_amount = round(
                        interest_amount * (1 - self.discount_factors[applicable_key])
                    )
                else:
                    next_key = min(larger_dates)
                    factor = self.discount_factors[applicable_key] + (
                        at_date - applicable_key
                    ) * (
                        self.discount_factors[next_key]
                        - self.discount_factors[applicable_key]
                    ) / (
                        next_key - applicable_key
                    )
                    interest_amount = interest_amount - round(interest_amount * factor)
        return interest_amount

    def future_interest(self):
        """Calculate future interest

        For each future period in the period list calculate
        the expected interest. If no discounting is requested,
        return the amount expected, else apply the discount.
        """

        calculation_periods = [
            period for period in self.period_list if "interest_frac" in period
        ]
        interest_estimate = 0
        for period in calculation_periods:
            # print(period)
            interest = Interest(
                from_date=period["from_date"],
                to_date=period["to_date"],
                start_balance=period["start_balance"],
                interest_frac=period["interest_frac"],
                calculation_method=Interest.ACTUAL_PERIODS,
            )
            interest_this_period = interest.amount_cents()
            # apply discounting
            if self.discount_factors:
                interest_this_period = self._discount_interest(
                    interest_this_period, period["from_date"], period
                )
            interest_estimate += interest_this_period
        return interest_estimate
