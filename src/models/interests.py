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

class interest(object):

    def calc_month(self, amount_cents, interest_fraction):
        """ Calculate a month worth of interest """

        return round((amount_cents * interest_fraction) ** (1/12))

    def calc_year(self, amount_cents, interest_fraction):
        """ Calculate a month worth of interest """

        return round(amount_cents * interest_fraction)
