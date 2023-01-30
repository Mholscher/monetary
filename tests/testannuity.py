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

import sys
import unittest
from models.annuity import Annuity

class TestMonthlyPayment(unittest.TestCase):

    def setUp(self):

        pass

    def test_calculate_payment_1(self):
        """ Calculate some annuity payment """

        principal = 10_000_000
        interest_frac = .08
        number_periods = 120
        self.assertEqual(Annuity.calc_payment(principal=principal,
                                              interest_frac=interest_frac,
                                              number_periods=number_periods),
                         121328, "Cannot calculate payment amount")

    def test_parms_required(self):
        """ All parameters are required """

        with self.assertRaises(ValueError):
            Annuity.calc_payment(principal=0,
                                 interest_frac=.01,
                                 number_periods=85)
        with self.assertRaises(ValueError):
            Annuity.calc_payment(principal=10000,
                                 interest_frac=.01,
                                 number_periods=0)

    def test_interest_frac_none(self):
        """ If interest fraction is none, abort """

        with self.assertRaises(ValueError):
            Annuity.calc_payment(principal=10000,
                                 interest_frac=None,
                                 number_periods=85)

    def test_interest_zero_accepted(self):
        """ Interest zero is acceptable """

        payment = Annuity.calc_payment(principal=10000,
                             interest_frac=0,
                             number_periods=85)
        self.assertEqual(payment, 118, "Incorrect amount")

    def test_single_period_annuity(self):
        """ Calculate the payable for a single period annuity """

        payment = Annuity.calc_payment(principal=10000,
                             interest_frac=0.04,
                             number_periods=1)
        self.assertEqual(payment, 10033, "Incorrect amount")

class TestAnnuityClass(unittest.TestCase):

    def setUp(self):

        self.principal = 15_000_000
        self.interest_frac = .06
        self.number_periods = 96
        self.annuity = Annuity(principal=self.principal,
                               interest_frac=self.interest_frac,
                               number_periods=self.number_periods)

    def test_setup_object(self):
        """ Create annuity object """

        annuity = Annuity(principal=self.principal,
                          interest_frac=self.interest_frac,
                          number_periods=self.number_periods)
        self.assertTrue(annuity, "No annuity created")

    def test_no_zero_principal(self):
        """ Cannot create an annuity without principal """

        with self.assertRaises(ValueError):
            annuity = Annuity(principal=0,
                              interest_frac=self.interest_frac,
                              number_periods=self.number_periods)

    def test_no_zero_periods(self):
        """ An annuity must have positive duration """

        with self.assertRaises(ValueError):
            annuity = Annuity(principal=self.principal,
                              interest_frac=self.interest_frac,
                              number_periods=0)
        with self.assertRaises(ValueError):
            annuity = Annuity(principal=self.principal,
                              interest_frac=self.interest_frac,
                              number_periods=-5)

    def test_return_monthly_payment(self):
        """ The monthly payment can be calculated """

        self.assertEqual(self.annuity.monthly_payment(), 197121,
                         "Payment not correctly calculated")

class TestCalculateHistory(unittest.TestCase):

    def setUp(self):

        self.principal = 15_000_000
        self.interest_frac = .06
        self.number_periods = 96
        self.annuity = Annuity(principal=self.principal,
                               interest_frac=self.interest_frac,
                               number_periods=self.number_periods)

    def test_return_interest_principals(self):
        """ Return the interest and principals """

        annuity = Annuity(principal=120000,
                          interest_frac=0.03,
                          number_periods=20)
        self.assertEqual(annuity.payment_schedule()[6],
                         (17, 6142), "Incorrect amount")
        self.assertEqual(annuity.payment_schedule()[19],
                         (1, 3234), "Incorrect last month")

    def test_last_installment(self):
        """ Return the last installment """

        annuity = Annuity(principal=1350000,
                          interest_frac=0.09,
                          number_periods=12)
        self.assertEqual(annuity.last_month_payment(),
                         56579, "Incorrect last month")
