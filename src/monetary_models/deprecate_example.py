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

class RecalcDeprecationSchedule(DeprecationSchedule):

    pass
