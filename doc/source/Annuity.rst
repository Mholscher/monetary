.. _annuitycalculations:

Annuity calculations
=====================

.. _annuityamount:

Calculate the annuity amount per month
--------------------------------------

The first calculation that will be made is the calculation of the amount of the annuity. This is the amount (re-)payable at each month except for the final month. In the final month the amount (re-)payable will be equal to the interest amount plus all of the remaining principal. The latter amount is not the aim of this calculation.

    :r: interest fraction
    :P: principal
    :n: number of periods (months)

The monthly amount is calculated through the formula:

    monthly amount = P * (r/(1-(1+r)⁻n))
