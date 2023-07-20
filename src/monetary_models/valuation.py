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

from datetime import date
from dateutil.relativedelta import relativedelta

class LoanValue():
    """ The class holds the value information for a period.

    From the input that is very similar to the interest calculation
    input the totals are calculated. It can also be used to project
    a value for a (partially) future period.
    """

    def __init__(self, period_data):

        self.period_list = period_data

    def interest(self):
        """ Calculate the total interest from the list of periods """

        total_interest = 0
        for period in self.period_list:
            total_interest += period["interest_posted"]
        return total_interest

    def repayment(self):
        """ Calculate repayment of principal for the period """

        if self.period_list:
            return (self.period_list[0]["principal"] 
                    - self.period_list[-1]["principal"])
        return 0
