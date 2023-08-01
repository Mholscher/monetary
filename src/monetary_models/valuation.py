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


class LoanValue():
    """ The class holds the liability value for one or more periods.

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

    """

    def __init__(self, period_data):

        self.period_list = period_data

    def posted_interest(self):
        """ Calculate the total interest from the list of periods """

        posted_periods = [period for period in self.period_list
                          if "interest_posted" in period]
        total_interest = 0
        for period in posted_periods:
            total_interest += period["interest_posted"]
        return total_interest

    def repayment(self):
        """ Calculate repayment of principal for the period """

        posted_periods = [period for period in self.period_list
                          if "principal" in period]
        if posted_periods:
            return (posted_periods[0]["principal"]
                    - posted_periods[-1]["principal"])
        return 0

    def future_interest(self):
        """ Calculate future interest """

        calculation_periods = [period for period in self.period_list
                               if "interest_frac" in period]
        interest_estimate = 0
        for period in calculation_periods:
            interest = Interest(from_date=period["from_date"],
                                to_date=period["to_date"],
                                start_balance=period["start_balance"],
                                interest_frac=period["interest_frac"],
                                calculation_method=Interest.ACTUAL_PERIODS
                                )
            interest_estimate += interest.amount_cents()
        return interest_estimate
