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

""" This module contains the model for deprecation. It supports more than one 
    way to deprecate an asset and also publishes services useful to support
    other ways of deprecating.
    """

import sys
import unittest
from datetime import date
from dateutil.relativedelta import relativedelta

class DeprecationSchedule():
    """ This models the schedule for deprecating an asset

    The parameters must be enough to create the complete schedule, as it
    is constructed at the time that the instance is created.

        :purchase_amount: the original cost of the asset
        :purchase_date: The date the asset was purchased and the start of the deprecation schedule
        :first_reporting_date: The first date deprecation should be performed
        :deprecate_years: the number of years the asset will be deprecated;  after this period a rest value may remain (see next parameter)
        :value_at_end: the monetary value of the asset at the end of the deprecation period.

    These parameters apply to the default deprecation method. They may be
    different for other methods. See the example supplied for the method
    where each year the asset is revalued.
    """

    def __init__(self, purchase_amount, purchase_date=date.today(),
                       first_reporting_date=date.today(), deprecate_years=5,
                       value_at_end=0, **kwargs):

        self.purchase_amount = purchase_amount
        self.purchase_date = purchase_date
        self.first_reporting_date = first_reporting_date
        if (relativedelta(self.first_reporting_date, self.purchase_date).years
            > 0):
            raise ValueError("First reporting date must be within one year")
        self.deprecate_years = deprecate_years
        self.value_at_end = value_at_end
        self._create_schedule()

    def _create_schedule(self):
        """ From the current data create the deprecation schedule """

        self.amounts = []
        self.amounts.append((self.purchase_date, 0))
        next_reporting_date = self.first_reporting_date
        first_period = relativedelta(self.first_reporting_date,
                                     self.purchase_date)
        yearly_deprecation = round((self.purchase_amount -
                                    self.value_at_end) /
                                   self.deprecate_years)
        current_value =  self.purchase_amount

        if first_period.months or first_period.days:
            first_period_deprecation = ((first_period.months + 1) *
                                        yearly_deprecation // 12
                                        if first_period.days != 0
                                        else first_period.months *
                                        yearly_deprecation // 12)
            self.amounts.append(
                (next_reporting_date, first_period_deprecation))
        else:
            first_period_deprecation = 0
        current_value -= first_period_deprecation
        while next_reporting_date < (self.purchase_date +
                                     relativedelta(years=
                                                   self.deprecate_years + 1)):
            next_reporting_date = (next_reporting_date +
                                relativedelta(years=1))
            if yearly_deprecation > current_value - self.value_at_end:
                deprecation_amount = current_value - self.value_at_end
            else:
                deprecation_amount = yearly_deprecation
            self.amounts.append((next_reporting_date,
                                deprecation_amount))
            current_value -= deprecation_amount

    def _value_at(self, requested_date, amounts):
        """ Return the value of the asset at the requested date

        From the purchase amount subtract all deprecation between the
        purchase date and the date passed in. Dates before the purchase date
        are invalid.
        """

       current_value = self.purchase_amount
        if requested_date < self.purchase_date:
            return 0
        for deprecation_period, amount in enumerate(amounts):
            if amount[0] <= requested_date:
                current_value -= amount[1]
            else:
                break
        return current_value

    def value_at(self, requested_date):
        """ Return the value of the asset at the requested date

        From the purchase amount subtract all deprecation between the
        purchase date and the date passed in. Dates before the purchase date
        are invalid.
        """

        return _value_at(requested_date, self.amounts)
