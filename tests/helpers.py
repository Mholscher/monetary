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

""" The following code is based upon the testing code for WTForms."""

class MultiDict:

    """ WTForms has a "canonical form" for multidicts that will function for most web frameworks. Originally monetary used Werkzeugs multidict, this holds its replacement for testing monetary """

    def __init__(self, tuples):
        self.tuples = tuples

    def __len__(self):
        return len(self.tuples)

    def __iter__(self):
        for k, _ in self.tuples:
            yield k

    def __contains__(self, key):
        for k, _ in self.tuples:
            if k == key:
                return True
        return False

    def getall(self, key):
        result = []
        for k, v in self.tuples:
            if key == k:
                result.append(v)
        return result

def calc_3_tenths(amount):
    """ Test routine to return 3/10th of the amount passed in 

        :amount: an amount in the smallest denomination of the currency

    """

    return round(3 * amount // 10)

def idem(amount):

    return amount
