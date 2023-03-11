.. _deprecation:

Deprecating capital goods
=========================

.. _deprecationscope:

Scope of the routines in this software
--------------------------------------

Deprecation of capital goods is a large and complex subject. It would be a lot of work to even find all parts there are to deprecation, so we need to choose what we want to incorporate in these routines. The choice will be built on

    * we will do the basics
    * we will only incorporate a few of the calculations or different methods
    * my understanding and knowledge of the subject

Especially the last one you may want to challenge to help the software grow and get better ;=)

.. _deprecationoverview:

High level overview of deprecating
----------------------------------

Capital goods are an asset to companies over a long period. When you buy a machine, it will serve you for many years to come, charging the amount paid to the current period would not be reasonable. So you need a way to spread the cost over the period the asset is used for production.

Deprecation is the term pointing at this process. At the time of purchase the capital good appears in the books valued at the purchase price. Later, usually at the closing of the reporting year, it is revalued, the difference between the "new" value and the "previous" value being the deprecation. At the end there is a remaining value, which is not deprecated further. 

Deprecation can be done on different bases, using different schemata. You may deprecate linearly, departing from the purchase price. Also you may determine the cost of replacing the asset with a new one, and base the deprecation on that price. Also you can deprecate fast in the beginning and slower towards the end of the period, to take into account the higher chances of needing to replace it near the end  of the period.

.. _lineardeprecation:

Deprecating linearly over a fixed period
----------------------------------------

The linear deprecation will be the default method. To be able to do that we need the purchase price (value at start), the schema (over what periods the deprecation will be done) and the remaining value of the asset at the end of the period.

The deprecation will be done in the following way:

    - from the purchase date to the first closing the value of the asset is the purchase price
    - at the reporting date the value is deprecated by the number of months (rounded up to full months) divided by 12 times the yearly deprecation
    - from then on each reporting date the yearly deprecation takes places until the en of the period. From then on the value is reported as the rest value.

