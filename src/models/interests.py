#    Copyright 2022 Menno Hölscher
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

""" This module contains classes for monetary calculations for interest.

The interest calculations are done for periods of days, for calendar periods
and for the period between two dates. 

Remarks:

*   For a period calculation a calculation/capitalization period needs to be
    passed down. The calculation period can not differ from the capitalization
    period
*   the calculation period can be "real" days, "real" days ignoring leap days
    (a year is considered to always have 365 days) or years having 360 days
    with months of 30 days.

The amount over the period need not be the same.
"""

from dateutil.relativedelta import relativedelta


class FromDateAfterToDateError(ValueError):
    """ The to date parameter is before the from date """

    pass


class Interest(object):
    """ Class to handle interest calculations

    The methods of this class are methods that return a value and those that
    set up a value in the class of the present calculation. The routines
    returning a value are in the class because they logically are used
    in interest calculations. E.g. calc_month is used to calculate  interest
    over full months.
    """

    ACTUAL_DAYS = object()
    ACTUAL_PERIODS = object()
    EQUAL_MONTHS = object()

    def __init__(self, from_date, to_date, start_balance, interest_frac,
                 calculation_method=ACTUAL_DAYS):

        self.from_date = from_date
        self.to_date = to_date
        self.start_balance = start_balance
        self.interest_frac = interest_frac
        self.calculation_method = calculation_method
        # Check date order
        if self.from_date > self.to_date:
            raise FromDateAfterToDateError(f"From date {self.from_date}" +
                                           f" > to date {self.to_date}")

    def amount_cents(self):
        """ Return the interest amount """

        if self.calculation_method == self.ACTUAL_DAYS:
            days = (self.to_date - self.from_date).days
            amount_cents = (self.start_balance * self.interest_frac 
                            * days / 365)
        elif self.calculation_method == self.ACTUAL_PERIODS:
            amount_cents = self.calculate_sum_periods()
        return round(amount_cents)
    
    def calculate_sum_periods(self):
        """ Calculate the total amount of interest

        First we split the period in years, months and days. Calculate
        the individual periods and sum the amounts.
        """
        amounts_periods = []
        monthly_amount = self.calc_month(self.start_balance,
                                         self.interest_frac)
        period = relativedelta(self.to_date, self.from_date)
        amounts_periods.append(round(
                               period.years * self.start_balance *
                               self.interest_frac))
        amounts_periods.append(period.months * monthly_amount)
        amounts_periods.append(round(
                               self.start_balance * self.interest_frac 
                               * period.days / 365))
        return sum(amounts_periods)

    @classmethod
    def calc_month(cls, amount_cents, interest_fraction):
        """ Calculate a month worth of interest """

        return round(amount_cents * ((1 + interest_fraction)**(1/12) -1))

    @classmethod
    def calc_year(cls, amount_cents, interest_fraction):
        """ Calculate a year worth of interest """

        return round(amount_cents * interest_fraction)
