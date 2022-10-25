The monetary library
====================

The uses of the library
-----------------------

The monetary library is meant for the development of systems that have a monetary component. The scope is:

    * amount conversions 
    * incorporating formatting according to the locale of the running program
    * formatting of amounts according to the rules of the currency.
    * :ref:`interestcalculations`
    

In general the formatting of the amount follows the rule of the locale. Formatting according to currency defaults is optional as in :ref:`AmountEditing`.

For use in forms, there is a WTForms formfield (see :ref:`WTFormsIntegration`) that shows the amounts formatted following the rules above and validates amounts input in the field.

.. _AmountEditing:

Amount editing
==============

.. _stringconversions:

String conversions
------------------

Amounts are supposed to be stored as integers in the smallest unit available. So for Euro amounts, the amount is stored in cents, for Yen in yen. The number of decimal places (precision, both terms are used in the documentation) is gotten from the ISO table 4217.

Amounts are formatted according to the rules of the locale. If your machine is running in the locale en-US, the decimal position is the decimal point and the amount has space as its thousand separator.

There is code to check amount input as strings. In the end, the amount is cleared from special characters "brute force" and parsed to an integer. A sign is left on the amount, though if it is in a unexpected place conversion will fail. Expected places are at the start and the end of the amount.

.. _WTFormsIntegration:

Integration of WTForms: AmountField
-----------------------------------

If you are using WTForms to process web input from forms, the package comes with an AmountField that enables you to put amounts on the web page and validate those. The field is fully compliant with WTForms, where a StringField can be used, the AmountField can be used. Formatting is done by the routines mentioned in :ref:`stringconversions`.

The formatting of the decimal separator depends on the currency. E.g. Euro and US Dollar have two decimal positions, Yen has none. We can pass the currency in the following ways:

  + when instantiating the field, pass the currency in in the currency field        ("currency='EUR'")

  + after the instance is created, set the instance variable currency to the value desired

  + before instantiating, set the get_currency method of the class to a function that accepts the field (as self) and returns the currency. If present, the field will call the method when it needs/could use the currency. Remove the function after instantiating the amount field(s)

The preferred ways are the first two. The function is a hack that carries risks. 

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

Each method has the possibility of compounding interest. The interest will be capitalized (i.e. added to the balance) every month or year, chosen by the caller. An example of compounding::

    start balance = 50000
    interest fraction = ,05 (5%)
    compounding = monthly

    first month interest = 204
    balance at start of 2nd month = 50204
    second month interest = 205
    balance at start of 3rd month = 50409
    etc.
