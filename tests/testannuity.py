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
                         800078, "Cannot calculate payment amount")

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
