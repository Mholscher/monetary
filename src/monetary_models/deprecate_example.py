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

""" This module contains a recalculating model for deprecation.  It supports
    a way to deprecate an asset by yearly revaluing an asset and recalculate
    the deprecation based on this new amount.
    """

from datetime import date
from dateutil.relativedelta import relativedelta
from monetary_models.deprecate import DeprecationSchedule


class ReplacementValueAtPurchaseDateError(ValueError):
    """ Cannot have a separate replacement value at purchase date """

    pass


class PreviousDeprecationAtPurchaseDateError(ValueError):
    """ Cannot have previous deprecation at purchase date """

    pass


class RecalcDeprecationSchedule(DeprecationSchedule):
    """ The schedule for a deprecation with revaluing each report date

    We revalue each reporting date and not only calculate the new deprecation
    amount, but also the correction over previous periods.

    The schedule entries are made up from:

        :reporting_date: The date for which the new deprecations are calculated
        :deprecation_amount: The new deprecation amount
        :delta_deprecation: difference with previous amount of deprecation, for periods before the current reporting date

    """

    def __init__(self, purchase_amount, purchase_date=date.today(),
                 first_reporting_date=date.today(), deprecate_years=5,
                 value_at_end=0, **kwargs):
        super().__init__(purchase_amount, purchase_date,
                         first_reporting_date=first_reporting_date,
                         deprecate_years=deprecate_years,
                         value_at_end=value_at_end, **kwargs)
        self.calculation_date = (kwargs["calculation_date"]
                                 if  "calculation_date" in kwargs
                                 else purchase_date)
        self.replacement_value = (kwargs["replacement_value"]
                                  if "replacement_value"in kwargs
                                  else 0)
        self.previous_yearly_deprecation = (kwargs["previous_yearly_deprecation"]
                                     if "previous_yearly_deprecation"in kwargs
                                     else 0)
        if (self.calculation_date == self.purchase_date
            and self.replacement_value):
            raise ReplacementValueAtPurchaseDateError(
                "Cannot have replacement value at purchase date")
        if (self.calculation_date == self.purchase_date
            and self.previous_yearly_deprecation):
            raise PreviousDeprecationAtPurchaseDateError(
                "Cannot have previous deprecation at purchase date")
        self._recalculate_amount()
        #print(self.new_amounts)

    def _recalculate_amount(self):
        """ Recalculate the deprecation and calculate the correction """

        self.new_amounts = []
        self.new_amounts.append((self.purchase_date, 0, 0))
        current_value = self.purchase_amount
        first_period = relativedelta(self.first_reporting_date,
                                     self.purchase_date)
        yearly_deprecation_new = round((self.replacement_value -
                                        self.value_at_end) /
                                        self.deprecate_years)
        if first_period.months or first_period.days:
            first_period_deprecation = ((first_period.months + 1) *
                                        yearly_deprecation_new // 12
                                        if first_period.days != 0
                                        else first_period.months *
                                        yearly_deprecation_new // 12)
        else:
            first_period_deprecation = 0
        period_1 = first_period_deprecation - self.amounts[0][1]
        self.new_amounts.append((self.purchase_date, period_1,
                                 first_period_deprecation))
        current_value -= first_period_deprecation
        next_reporting_date = self.first_reporting_date
        while next_reporting_date < (self.purchase_date +
                                     relativedelta(years=
                                                   self.deprecate_years + 1)):
            next_reporting_date = (next_reporting_date +
                                relativedelta(years=1))
            if yearly_deprecation_new > current_value - self.value_at_end:
                deprecation_amount = current_value - self.value_at_end
            else:
                deprecation_amount = yearly_deprecation_new
            self.new_amounts.append((next_reporting_date,
                                deprecation_amount))
            current_value -= deprecation_amount
        return self.new_amounts

    def value_at(self, requested_date):
        """ Get the value at the date for the changed schedule """

        if requested_date < self.purchase_date:
            return 0
        return self._value_at(requested_date, self.new_amounts)

    def correction(self):
        """ Return the correction for the whole deprecation period  """

        periods = relativedelta(self.calculation_date, self.purchase_date)
        if self.replacement_value != self.purchase_amount:
            return round((((self.replacement_value -self.value_at_end) /
                        self.deprecate_years) - self.previous_yearly_deprecation)
                        * (periods.years + periods.months / 12))
        else:
            return 0
