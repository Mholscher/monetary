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

""" This file contains functions and classes for annuity calculation.

Calculations are determining the monthly annuity payable, the interest and
repayment amounts per period as well as the "final payment", which makes
the annuity fully repaid.
"""

from models.interests import Interest

class PrincipalRequiredError(ValueError):
    """ The annuity principal is required """

    pass

class InterestRequiredError(ValueError):
    """ The interest fraction is required """

    pass

class NumberPeriodsMustBePositiveError(ValueError):
    """ The number of months is required """

    pass

class Annuity():
    """ This class holds annuity calculations and results """

    def __init__(self, principal=0, interest_frac=0,
                 number_periods=1):

        if not principal:
            raise PrincipalRequiredError()
        if number_periods <= 0:
            raise NumberPeriodsMustBePositiveError()
        self.principal = principal
        self.interest_frac = interest_frac
        self.number_periods = number_periods

    def monthly_payment(self):
        """ The monthly payment for this annuity """

        return self.calc_payment(self.principal,
                                 self.interest_frac,
                                 self.number_periods)

    def payment_schedule(self):
        """ Calculate the principals and interest amount for all months """

        monthly = self.monthly_payment()
        remaining_principal = self.principal
        monthly_interest_frac = self.interest_frac / 12
        monthly_amount_split = []
        for _ in range(self.number_periods - 1):
            interest = Interest.calc_month(remaining_principal,
                                           monthly_interest_frac)
            repayment = monthly - interest
            monthly_amount_split.append((interest, repayment))
            remaining_principal = remaining_principal - repayment
        interest = Interest.calc_month(remaining_principal,
                                       monthly_interest_frac)
        monthly_amount_split.append((interest, 
                                     remaining_principal - interest))
        return monthly_amount_split

    def last_month_payment(self):
        """ Calculate the last month (pro rata) payment """

        last_month_amounts = self.payment_schedule()[-1]
        return sum(last_month_amounts)

    @staticmethod
    def calc_payment(principal=0, interest_frac=0.0, number_periods=1):
        """ Calculate the monthly amount payable for an annuity """

        if not principal:
            raise PrincipalRequiredError("Principal must be an amount > 0")
        if interest_frac is None:
            raise InterestRequiredError(
                "Interest fraction must be a number")
        if not number_periods:
            raise NumberPeriodsMustBePositiveError(
                "Number of periods must be a number > 0")
        if interest_frac == 0:
            return round(principal/number_periods)
        interest_frac = interest_frac / 12
        return round(principal * (interest_frac /
                         (1-(1+interest_frac)**(-number_periods))))
