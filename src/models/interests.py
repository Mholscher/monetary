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

from datetime import date
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
    The initialization supports the following parameters:

        :from_date: The start date of the interest period (no default)
        :to_date: the end date of the interest period (no default)
        :start_balanc: The balance of funds at the from_date (no default)
        :interest_frac: The fractional interest rate. It is equal to interest percentage / 100 (no default)
        :calculation_method: The method of calculation, actual days, actual periods (yearly and monthly) and equal monts (30 day month, 360 day year) (default: actual days)
        :calendar_month: The months are equal to calendar months or not, i.e. if a pro rata period may be present at the start of the period (default: False)

    """

    ACTUAL_DAYS = object()
    ACTUAL_PERIODS = object()
    EQUAL_MONTHS = object()

    def __init__(self, from_date, to_date, start_balance, interest_frac,
                 calculation_method=ACTUAL_DAYS, calendar_months=False):

        self.from_date = from_date
        self.to_date = to_date
        self.start_balance = start_balance
        self.interest_frac = interest_frac
        self.calculation_method = calculation_method
        self.calendar_months = calendar_months
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
        elif (self.calculation_method == self.ACTUAL_PERIODS
              or self.calculation_method == self.EQUAL_MONTHS):
            amount_cents = self.calculate_sum_periods()
        return round(amount_cents)
    
    def calculate_sum_periods(self):
        """ Calculate the total amount of interest

        First we split the period in years, months and days. Calculate
        the individual periods and sum the amounts.
        """
        amounts_periods = []
        if self.calendar_months:
            amounts_periods.append(self.calculate_prorata_at_start())
            from_date = self._som(self.from_date)
        else:
            from_date = self.from_date
        monthly_amount = self.calc_month(self.start_balance,
                                         self.interest_frac)
        period = relativedelta(self.to_date, from_date)
        amounts_periods.append(round(
                               period.years * self.start_balance *
                               self.interest_frac))
        amounts_periods.append(period.months * monthly_amount)
        days = (period.days - 1 if (self.calculation_method == self.EQUAL_MONTHS
                                   and self.to_date.day > 30)
                                else period.days)
        amounts_periods.append(round(
                               self.start_balance * self.interest_frac 
                               * days / 365))
        return sum(amounts_periods)

    def _som(self, for_date):
        """ Calculate the start of month after for_date """

        if for_date.month >= 12:
            month = 1
            year = year + 1
        else:
            month = for_date.month + 1
            year = for_date.year
        day = 1
        return date(year, month, day)

    def calculate_prorata_at_start(self):
        """ Calculate the interest until the start of next month """

        start_next_month = self._som(self.from_date)
        if start_next_month > self.to_date:
            period = relativedelta(self.to_date, self.from_date)
        else:
            period = relativedelta(start_next_month, self.from_date)
            if self.calculation_method == self.EQUAL_MONTHS:
                if self.from_date.day < 30:
                    prorata_days = 30 - self.from_date.day
                else:
                    prorata_days = 0
            else:
                prorata_days = period.days
        #print(prorata_days)
        return round(prorata_days * self.interest_frac *
                     self.start_balance / 365)

    @classmethod
    def calc_month(cls, amount_cents, interest_fraction):
        """ Calculate a month worth of interest 

        Parameters are:

            :amount_cents: The amount in the smallest denomination of the currency, so for Euro and dollar cents (hence the name)
            :interest_fraction: The interest rate as a fraction, i.e. interest percentage / 100

        """

        return round(amount_cents * ((1 + interest_fraction)**(1/12) -1))

    @classmethod
    def calc_year(cls, amount_cents, interest_fraction):
        """ Calculate a year worth of interest 

        Parameters are:

            :amount_cents: The amount in the smallest denomination of the currency, so for Euro and dollar cents (hence the name)
            :interest_fraction: The interest rate as a fraction, i.e. interest percentage / 100

        """

        return round(amount_cents * interest_fraction)
