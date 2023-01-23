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

class PrincipalRequiredError(ValueError):
    """ The annuity principal is required """

    pass

class InterestRequiredError(ValueError):
    """ The interest fraction is required """

    pass

class NumberPeriodsRequiredError(ValueError):
    """ The number of months is required """

    pass

class Annuity():
    """ This class holds annuity calculations and results """

    def __init__():

        pass

    @staticmethod
    def calc_payment(principal=0, interest_frac=0.0, number_periods=1):
        """ Calculate the monthly amount payable for an annuity """

        if not principal:
            raise PrincipalRequiredError("Principal must be an amount > 0")
        if interest_frac is None:
            raise InterestRequiredError(
                "Interest fraction must be a number")
        if not number_periods:
            raise NumberPeriodsRequiredError(
                "Number of periods must be a number > 0")
        if interest_frac == 0:
            return round(principal/number_periods)
        return round(principal * (interest_frac /
                         (1-(1+interest_frac)**(-number_periods))))
