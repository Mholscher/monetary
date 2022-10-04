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
    ACTUAL_MONTHS = object()

    def __init__(self, from_date, to_date, start_balance, interest_frac):

        self.from_date = from_date
        self.to_date = to_date
        self.start_balance = start_balance
        self.interest_frac = interest_frac

    def amount_cents(self):
        """ Return the interest amount """

        days = (self.to_date - self.from_date).days
        amount_cents = (self.start_balance * self.interest_frac / 100
            * days / 365)
        return round(amount_cents)

    @classmethod
    def calc_month(cls, amount_cents, interest_fraction):
        """ Calculate a month worth of interest """

        #print(amount_cents * ((1 + 100 *interest_fraction)**(1/12) -1))
        return round(amount_cents * ((1 + interest_fraction)**(1/12) -1))

    @classmethod
    def calc_year(cls, amount_cents, interest_fraction):
        """ Calculate a year worth of interest """

        return round(amount_cents * interest_fraction)
