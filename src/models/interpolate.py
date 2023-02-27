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
""" This module contains a linear interpolation function for amounts
over a fixed period and for one or more dates
"""
from datetime import date, timedelta

def interpolate(start_from, end_to, requested_dates):
    """Interpolate amounts for one or more dates

        :start_from: a tuple with the start date and amount in the smallest denomination
        :end_to: a tuple with the end date and amount
        :requested_dates: an iterable which returns the dates for which an interplated amount is requested.

    """

    result = []
    start_date = start_from[0]
    start_amount = start_from[1]
    end_date = end_to[0]
    end_amount = end_to[1]
    full_period = (end_date - start_date).days
    if start_date >= end_date:
        raise ValueError(f"Start date {start_date} must be smaller than"
                         f" end date  { end_date}")
    for calculation_date in requested_dates:
        if calculation_date < start_date or calculation_date >= end_date:
            raise ValueError(f"Date {calculation_date} outside period")
        period = (calculation_date - start_date).days
        result.append((calculation_date,
                       round(period / full_period * (end_amount - start_amount)
                       + start_amount)))
    return result
