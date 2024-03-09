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
from itertools import pairwise
from dateutil.relativedelta import relativedelta
from monetary_models.interests import Interest
from monetary_models.interpolate import interpolate


class CannotCalculateValueAt(ValueError):
    """ A value cannot be calculated with the current input """

    pass


class HistoryListTooShort(ValueError):
    """ A history list has a minimum number of values """

    pass


class UnknownPeriodError(ValueError):
    """ A period in a Fee has an unknown value """

    pass

class KeyOrderError(ValueError):
    """ Keys in discount factors must be in ascending order """

    pass


def discount_amount(undiscounted_amount, at_date, discount_factors):
    """ Discount an amount at a given date with discount factor(s) """

    # Find the applicable discount factor(s)
    applicable_factors = None
    for factor in pairwise(discount_factors):
        if (factor[0] <= at_date
          and factor[1] >= at_date):
            applicable_factors = factor
            break
    # Zero or one discount factor:
    if applicable_factors is None:
        if discount_factors:
            choosen_factor = 0
            for start_date, factor in discount_factors.items():
                if start_date <= at_date:
                    choosen_factor = factor
            return undiscounted_amount - round(undiscounted_amount
                                               * choosen_factor)
        return undiscounted_amount

    # Otherwise more discount factors => interpolate
    factor = discount_factors[applicable_factors[0]] + (
        at_date - applicable_factors[0]
    ) * (
        discount_factors[applicable_factors[1]]
        - discount_factors[applicable_factors[0]]
    ) / (
        applicable_factors[1] - applicable_factors[0]
    )

    return (undiscounted_amount - round(
        undiscounted_amount * factor
    ))


class DiscountFactors(dict):
    """ This class holds a group of discount factors.

    A discount factor consists of a date and the associated factor.
    The factor is the discount factor to be used for an amount evaluation on
    said date. The factor is the fraction of the amount that should be discounted.

    The mapping must be a data structure that has the
    collections.abc.MutableMapping interface. The most common structure is dict.
    """

    def __init__(self, mapping):

        for first_date, second_date in pairwise(mapping):
            if first_date > second_date:
                raise KeyOrderError("Dates must be in order")
        super().__init__(mapping)

    def __setitem__(self, key, value):

        keys_reversed = reversed(self.keys())
        if next(keys_reversed) > key:
            raise ValueError("Keys must be added in order")
        super().__setitem__(key, value)

class LoanValue:
    """The class holds the liability value for one or more periods.

    From the input that is very similar to the interest calculation
    input the totals are calculated. It can also be used to project
    a value for a future period.

    The input is a period list, with each period a history period or
    a future period. History periods are formatted:

        :from_date: The start date of this period
        :to_date: The day after the end of the period
        :principal: The amount of the principal in the smallest denomination (like cents or pennies)
        :interest_posted: The interest posted in the period

    Future periods are formatted:

        :from_date: The start date of this period
        :to_date: The day after the end of the period
        :start_balance: The amount of the principal at start of the period in the smallest denomination (like cents or pennies)
        :interest_frac: The interest percentage as a fraction in the period

    For discounting you can enter discount factors. The factors are defined as:

        :date_factor: The date for which the factor is valid
        :factor: A fraction with which an amount is to be discounted on that date

    You can pass in None, than there will be no discounting of future amounts.
    If there is one factor, it will be taken as a constant, and each amount
    to be received after the date_factor will be discounted by the factor.
    You can pass in more factors, the factors will be interpolated between the
    dates and beyond the last date the factor will be constant (i.e. the value
    for the highest date). Before the lowest date, no discounting will be done.
    """

    def __init__(self, period_data, discount_factors=None):
        self.period_list = period_data
        self.discount_factors = discount_factors

    def posted_interest(self):
        """Calculate the total interest from the list of periods"""

        posted_periods = [
            period for period in self.period_list
            if "interest_posted" in period
        ]
        total_interest = 0
        for period in posted_periods:
            total_interest += period["interest_posted"]
        return total_interest

    def repayment(self):
        """Calculate repayment of principal for the periods

        The repayment is taken as the difference between the principals
        in consecutive periods.
        """

        posted_periods = [
            period for period in self.period_list if "principal" in period
        ]
        if posted_periods:
            if self.discount_factors:
                discounted_sum = 0
                for period_no, calculation_period in enumerate(posted_periods):
                    if period_no > 0:
                        undiscounted = (
                            posted_periods[period_no - 1]["principal"]
                            - posted_periods[period_no]["principal"]
                        )
                        discounted_sum += self._discount_repayment(
                            undiscounted,
                            posted_periods[period_no]["from_date"],
                            posted_periods[period_no],
                        )
            else:
                discounted_sum = (
                    posted_periods[0]["principal"]
                    - posted_periods[-1]["principal"]
                )
            return discounted_sum
        return 0

    def _discount_repayment(self, repayment_amount, at_date, period):
        """Discount a future principal repayment"""

        date_factors = [
            date_factor
            for date_factor in self.discount_factors.keys()
            if date_factor <= period["from_date"]
        ]

        if date_factors:
            repayment_amount = discount_amount(repayment_amount,
                                               at_date,
                                               self.discount_factors)
        return repayment_amount

    def future_interest(self):
        """Calculate future interest

        For each future period in the period list calculate
        the expected interest. If no discounting is requested,
        return the amount expected, else apply the discount.
        """

        calculation_periods = [
            period for period in self.period_list if "interest_frac" in period
        ]
        interest_estimate = 0
        for period in calculation_periods:
            # print(period)
            interest = Interest(
                from_date=period["from_date"],
                to_date=period["to_date"],
                start_balance=period["start_balance"],
                interest_frac=period["interest_frac"],
                calculation_method=Interest.ACTUAL_PERIODS,
            )
            interest_this_period = interest.amount_cents()
            # apply discounting
            if self.discount_factors:
                interest_this_period = discount_amount(interest_this_period,
                                                       period["from_date"],
                                                       self.discount_factors)
            interest_estimate += interest_this_period
        return interest_estimate


class DepositValue(LoanValue):
    """ The class holds the asset value for one or more periods.

    From the input that is very similar to the interest calculation
    input the totals are calculated. It can also be used to project
    a value for a future period.

    The input is a period list, with each period a history period or
    a future period. History periods are formatted:

        :from_date: The start date of this period
        :to_date: The day after the end of the period
        :principal: The amount of the principal in the smallest denomination (like cents or pennies)
        :interest_posted: The interest posted in the period

    Future periods are formatted:

        :from_date: The start date of this period
        :to_date: The day after the end of the period
        :start_balance: The amount of the principal at start of the period in the smallest denomination (like cents or pennies)
        :interest_frac: The interest percentage as a fraction in the period

    For discounting you can enter discount factors. The factors are defined as:

        :date_factor: The date for which the factor is valid
        :factor: A fraction with which an amount is to be discounted on that date

    You can pass in None, than there will be no discounting of future amounts.
    If there is one factor, it will be taken as a constant, and each amount
    to be received after the date_factor will be discounted by the factor.
    You can pass in more factors, the factors will be interpolated between the
    dates and beyond the last date the factor will be constant (i.e. the value
    for the highest date). Before the lowest date, no discounting will be done. """

    pass


class CommonStockValue():
    """ This class holds the value of one share.

    From the input the value of a share of common stock is calculated. The
    value of the stock at market and the expected dividends. The value of the
    stock is discounted at the date of the "expected sale" of the asset. See
    the documentation for more information.

    The input is the historic value of the share and the dividends paid in the
    past. Further we need the expected sales date. It is a list/tuple of:

        :value_date: The date the value/dividend applies_to
        :share_value: The value of shares in the smallest denomination (like cents or pennies)
        :dividend_paid: The dividend paid at or for the period denoted by the value date

    For discounting the discount factors are passed in. See the :py:class:`~LoanValue` documentation 
    for the format these are in.
    """

    date_measured = "date_measured"
    share_price = "share_price"
    dividend = "dividend"

    def __init__(self, history_list, discount_factors=None):

        if len(history_list) < 2:
            raise HistoryListTooShort("A history should contain at least 2 years")
        self.history_list = history_list
        if discount_factors:
            self.discount_factors = discount_factors
        else:
            self.discount_factors = dict()

    def growth_share_value(self):
        """ From the history list we calculate the mean value increase
            per share """

        sum_values = 0
        for older_item, newer_item in pairwise(self.history_list):
             sum_values += (newer_item[self.share_price]
                           - older_item[self.share_price])
        return sum_values // (len(self.history_list) - 1)

    def mean_dividend(self):
        """ From the history list we calculate the mean dividend """

        return round(sum([history_item[self.dividend]
                     for history_item in self.history_list])
                     / len(self.history_list))

    def value(self, at_date=None):
        """ Calculate the estimated value at at_date

        Contrary to the comment in this module, asking for a valuation
        of a share on a date before the first history date will fail.

        Dates that are beyond the last date in the history, cannot be processed
        by this method, see :py:meth:`~CommonStockValue.estimated_value`.
        """

        if at_date is None:
            self.at_date = date.now()
        else:
            self.at_date = at_date
        result_price = None
        for item in self.history_list:
            if item[self.date_measured] == at_date:
                result_price = item[self.share_price]
                return result_price
        # print("list is", self.history_list, "at date", at_date)
        for item_no, history_item in enumerate(self.history_list):
            if item_no == 0:
                continue
            if at_date < history_item[self.date_measured]:
                at_start = (self.history_list[item_no - 1][self.date_measured],
                            self.history_list[item_no - 1][self.share_price])
                at_end = (item[self.date_measured],
                          item[self.share_price])
                dates = [at_date]
                result_price = interpolate(at_start, at_end, dates)[0][1]
                # print("Price is", result_price)
        if result_price is None:
            raise CannotCalculateValueAt("No price could be determined "
                                         f"for {at_date}")
        return result_price

    def estimated_value(self, at_date):
        """ Calculate the estimated value based on experience 

        Dates that are before the last date in the history, cannot be processed
        by this method, see :py:meth:`~CommonStockValue.value`.

        """

        share_price_growth = self.growth_share_value()
        estimated_dividend = self.mean_dividend()
        if at_date <= self.history_list[-1][self.date_measured]:
            raise CannotCalculateValueAt("Cannot calculate estimate" 
                                         f" for {at_date}: in history")
        since_last_measured = relativedelta(at_date, 
                                            self.history_list[-1]
                                            [self.date_measured])
        value_growth = since_last_measured.years * share_price_growth
        value_growth += round(share_price_growth * 
                              since_last_measured.months / 12)
        value_growth += round(share_price_growth *  
                              since_last_measured.days / 365)
        value_growth = discount_amount(value_growth, at_date, self.discount_factors)
        dividends = since_last_measured.years * estimated_dividend
        dividends = discount_amount(dividends, at_date, self.discount_factors)
        # print("value change: ", value_growth, "Dividends", dividends)
        # print("returns", (value_growth + dividends + self.history_list[-1]
        #                                     [self.share_price]))
        return (value_growth + dividends + self.history_list[-1]
                                            [self.share_price])


class Fee():
    """ A fee consists of an amount, a period (year, month etc.) and end date """

    FEE_YEARLY = 1
    FEE_MONTHLY = 12

    def __init__(self, amount, period=None, end_date=None):

        self.amount = amount
        if period:
            self.period = period
        else:
            self.period = 1  # Yearly
        self.end_date = end_date

class LeaseCostValue():
    """ The current cost of a lease to the company.

    the cost of the lease is the sum of the discounted value of all lease
    payments, minus the remaining discounted value of the good at the end
    of the lease term.
    """

    def __init__(self, lease_fee, current_asset_value, borrowing_rate,
                 remaining_value=0,at_date=None):

        self.lease_fee = lease_fee
        self.asset_value = current_asset_value
        self.borrowing_rate = borrowing_rate
        self.at_date = at_date
        self.remaining_value = remaining_value

    def estimated_value(self):
        """ An estimate of the current cost of the good """

        period = relativedelta(self.lease_fee.end_date, self.at_date)
        # print(period)
        if self.lease_fee.period == Fee.FEE_YEARLY:
            num_month_payments = period.months
            if period.days:
                num_month_payments += 1
            num_year_payments = period.years + 1
        elif self.lease_fee.period == Fee.FEE_MONTHLY:
            if period.days > 0:
                num_month_payments = period.years *12 + period.months +  1
            else:
                num_month_payments = period.years *12 + period.months
            num_year_payments = 0
        else:
            raise UnknownPeriodError("Unknown period"
                                     f" {self.lease_fee.period}")
        if self.borrowing_rate:
            next_interest = (self.lease_fee.end_date -
                            relativedelta(years=period.years))
            discounted = 0
            # First calculate pro-rata period
            discounted += (self.lease_fee.amount *
                              (1 - self.borrowing_rate)
                              * period.months / 12)
            # print("Discounted amount: ", discounted)
            for period_no in range(1, period.years + 1):
                if period.months == 0:
                    discounted += (self.lease_fee.amount *
                                  (1 - self.borrowing_rate) ** period_no)
                else:
                    discounted += (self.lease_fee.amount *
                                  ((1 - self.borrowing_rate) ** (period_no + 1)
                                  * (12 - period.months)/12 +
                                  (1 - self.borrowing_rate) ** (period_no)
                                  * period.months/12))
                # print("Discounted period:", period_no, discounted)
            return round(discounted)
        else:
            return (self.lease_fee.amount * num_year_payments
                    if self.lease_fee.period == Fee.FEE_YEARLY
                    else self.lease_fee.amount * num_month_payments)

    def discounted_end_value(self):
        """ Discount the end value of the item 

        The value of the asset at end of the lease period is not put into
        the liability of the cost of the lease. It needs to be accounted
        for separately.
        """

        discount_factors = self.end_value_discount_factors()
        return (self.remaining_value -
            round(discount_amount(self.remaining_value,
                                  self.lease_fee.end_date,
                                  discount_factors)))

    def end_value_discount_factors(self):
        """ Create the discount factors from the borrowing rate """

        discount_factors = dict()
        for next_factor in self._date_and_factor():
            discount_factors.update(next_factor)
        return discount_factors

    def _date_and_factor(self):
        """ Return discount factors """

        yield {self.at_date : 1}
        last_date = self.at_date
        last_factor = 1
        while last_date <= self.lease_fee.end_date:
            last_date = last_date + relativedelta(years=1)
            last_factor = round(last_factor * (1 - self.borrowing_rate), 2)
            yield {last_date :  last_factor}
