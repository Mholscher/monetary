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

.. _annuityobject:

Getting more information about the annuity
------------------------------------------

To be able to get more information about the annuity, we can create an annuity instance. The instance supplies us with a list of the payments, divided into interest and principal repayment. Also this of course returns the final payment, which is usually different from the previous payments.

The interest over the previous period is calculated through the monthly interest routines from the package, in :ref:`monthofinterests`. The principal part for all periods but the last one is the annuity amount minus the calculated interest. The last one is the sum of what remains of the principal plus the interest accumulated in this last period.
