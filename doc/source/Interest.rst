.. _interestcalculations:

Interest calculations
=====================

.. _basiccalculations:

Interest calculations: basics
-----------------------------

To be able to calculate interest, several routines are made to calculate the basic amounts.

.. _yearofinterests:

Calculate a year worth of interest
----------------------------------

A year of interest *over a fixed amount* is calculated as:

    the amount in cents * the interest fraction, rounded to the nearest cent

*Remark*: The interest is passed in as a fraction of the amount not a percentage.

.. _monthofinterests:

Calculate a month worth of interest
-----------------------------------

A month of interest *over a fixed amount* is calculated as:

    the amount in cents * ((1 + 100 * the interest fraction)**(1/12) -1) / 100, rounded to the nearest cent

*Remark*: The interest is passed in as a fraction of the amount not a percentage.
This routine does not take into account the actual number of days per month. It calculates an interest amount as the interest due over 1/12th of the yearly period.

.. _interestperiods:

Interest over any period
------------------------

Hardly anytime interest will only be chargeable over full periods and a constant amount. So monetary will facilitate more interest calculation methods, aimed at circumventing these limitations.

For the periods, it was already mentioned in :ref:`basiccalculations` the simple calculation assumes that all months have the same duration. Of course this is not the case. Different ways of fitting the calculation are devised:

    :actual days: Use the actual duration in days of the months and years (including leap days) in the calculation. I will refer to this as the method **366/31**
    :actual periods: Use the duration in months and years, ignore the existence of leap days. Pro rata will be calculated in actual days. I will refer to this as the method **365/31**
    :equal months: Use as the duration of the month always 30 days and (consequently) a year of 360 days. If the month actually 28, 29 or 31 days, this shows up only in the calculation of pro rata periods, not in the amount per day. I will refer to this as the method **360/30**.

.. _actualdayscalculation:

Actual days (366/31)
--------------------

This is the simplest of the calculations. Determine the number of calendar days between the start and end date and calculate the interest as:

    amount in cents * interest fraction * number of days / 365

.. _actualperiodscalculation:

Actual periods (365/31)
-----------------------

Split the duration in years, months and days. Calculate the yearly amount(s) as specified in :ref:`yearofinterests`, the monthly amount(s) as specified in :ref:`monthofinterests` and the daily amounts over the pro rata days at the end of the period:

    amount in cents * interest fraction * number of days / 365

The interest will not be compounded per month, unless explicitly requested. As compounding will be per month, we will split the period only in months and days if compounding is requested.
    
Depending on the calculation type, at the beginning of the period there may also be pro rata days. they bridge the period to the beginning of the next  calendar month:

    amount in cents * interest fraction * remaining number of days in month / 365

As this is rather the exception, the default will be full years and months from the start date.

.. _equalmonthscalculation:

Equal months (360/30)
---------------------

Split the duration in years, months and days. Calculate the yearly amount(s) as specified in :ref:`yearofinterests`, the monthly amount(s) as specified in :ref:`monthofinterests` and the daily amounts over the pro rata days, where any period in a month greater than or equal to 30 days equates to a whole month, with the exception of February, where the cut-off is at the 28th. The calculation of the interest rate is the same as for the :ref:`actualperiodscalculation` method.

.. _compoundinterest:

Compounding interest
--------------------

Each method has the possibility of compounding interest. The interest will be capitalized (i.e. added to the balance) every month. An example of compounding::

    start balance = 50000
    interest fraction = ,05 (5%)
    compounding = monthly

    first month interest = 204
    balance at start of 2nd month = 50204
    second month interest = 205
    balance at start of 3rd month = 50409
    etc.

.. _runninginterest:

Interest over a period with varying amount/interest rate
--------------------------------------------------------

When interest is being calculated over a period where the interest rate or amount will differ for different sub-periods, we use the RunningInterest. We pass is the periods, amounts and interest fractions, and further the other data like the calculation method and whether compounding needs to take place.

For the non-compounding case, things are easy. For each period the interest is calculated. For the compounding case we need to either calculate interest up to the next period or the next interest calculation date. Example::

    start balance = 130000
    interest fraction = ,05 (5%)
    compounding = monthly
    start date = 8th December 2022
    switch date = 12th January 2023, new balance = 135000

    first month interest = 530
    balance at start of 2nd month = 130530
    pro rata interest 8-1 to 12-1 = 72
    new balance at 12-1 = 135000
    pro rata interest 12-1 to 8-2 = 502
    balance at start of third month = 135502

The basic method of passing all data for a period. However, for convenience you can also pass a structure with a start amount and start date, followed by change dates and a function to calculate change amounts and an overall end date. See the technical documentation for :ref:`apiinterestcalculations`.
