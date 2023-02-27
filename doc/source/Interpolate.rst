.. _interpolation:

Interpolate amounts between dates
=================================

This function enables one to calculate one or more amounts (values) over a period at the beginning and end of which an amount is known.

The interpolation is done along a linear scale.

The calculation is done so:

    the fraction of  until the date of the total period times the difference between the amount at the end date and the start date plus the amount at the start date.

An example:

    beginning of period
        date is 1-1-2023
        amount is 18000
    end of period
        date is 1-2-2023
        amount is 15000
    dates to calculate amount for
        12-1-2023
        24-1-2023

The calculation then is done as:

    12 / 31 * (15000 - 18000) + 18000

    * the fraction of the period is 12/31
    * the change amount is 15000 - 18000
    * the amount at start is 18000

Like wise for the 24th:

    24 / 31 * (15000 - 18000) + 18000

Giving an amount of 16839 resp. 15677.
