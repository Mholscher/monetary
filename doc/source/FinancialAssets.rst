Financial asset and liability value
====================================

What is considered a financial asset/liability
----------------------------------------------

In business there are several ways to finance assets and other things your company needs. These ways of finance need to be compared and reported upon. The finance tools are also themselves assets or liabilities, creating a kind of "recursive asset".

"Compared" because choosing the wrong financial instrument may lead to paying to much and loosing opportunities. "Reported" because the cost of finance are of course part of the financial situation of the company.

Below I discuss some kinds of financial assets and liabilities. These discussions are not going tot "the bottom of it", they are meant to identify some fields of calculations that we need to address.

A loan
------

In a loan you take out some money from the lender and pay the lender a fee for the use of the money: the interest. The liability consists of the part of the capital still outstanding (i.e. actually the repayments) and the interest due in the future.

The repayments on the capital are scheduled for a normal loan. It may be scheduled as "repay everything at end", but these loans are considered risky and discouraged by regulatory rules. So we will consider loan repayments at a regular interval, with a repayment of the remainder at the last payment. Future payments will be discounted by a discount rate if requested, otherwise not.

Interest is accounted for in a given period in the future also. Amounts are discounted if a discount rate is supplied. We will not assume that the interest schedule is the same as the repayment schedule, though in practice they usually will be.

For repayments as well as interest payments discount rates may be interpolated. If more than one discount rate is supplied, the discount rates are interpolated between the dates. The interpolation is linear, based on the number of days between the discount dates and the date the payment takes place.

A deposit
---------

The deposit is kind of the mirror image of the loan. It supplies an income stream for the capital and interest.

The repayment will be governed by a schedule and the calculation of the value of future repayments will be by discounting by the discount rate for funds due at the repayment time. Interest will be the same. Here also, repayment schedule and interest schedule may differ. Discounting is optional.

Other than for loans, there is a debtor risk being run. You are not sure the debtor will pay in time or will pay *at all*. This risk will be ignored for now. It does have an influence on the valuation of the deposit.

A leasing agreement
-------------------

According to IFRS16 the calculation of the discount of amounts payable and received on a lease is based on the "interest rate implicit in the lease" or the "lessee's incremental borrowing rate".

Interest rate implicit in the lease is the rate of interest that causes the present value of lease payments and the unguaranteed residual value to equal the sum of the fair value of the underlying asset, and any initial direct costs of the lessor.

The incremental borrowing rate is a interest rate that reflects the rate it would have to pay to borrow over a similar term to the lease term with a similar security to the security (collateral) in the lease, the amount needed to obtain an asset of a similar value to the right-of-use asset arising from the lease in a similar economic environment to that of the lease.

These are based on rates and amounts strongly dependent on the situation of the lessor and lessee. We cannot determine that in this library, so we will expect these to be supplied.

The data required to determine expected cost of such an agreement is:

    :the lease fee: the amount payable per period of the lease term
    :remaining value: the value remaining in the leased good at the end of the lease term
    :incremental borrowing rate: the interest rate payable if the lessee would need to borrow the current value of the item
    :end date: the end date of the lease term

The discounted end value is calculated from the undiscounted value. However, it is not put into the value of the cost of the lease , as it is in a different category.

Stocks and bonds
----------------

For stocks and bonds we will calculate the return in dividend or interest and the changes in value of the asset.

A major question here is the uncertainty of the returns on these assets. Dividends are following the performance of the company and the value of stocks and bonds are influenced by the economic outlook as well. We will not take the risks of the assets into account [usediscount]_. Value will be based on the valuation of the asset in the past. We will apply the mean growth over a past periods to estimate the growth in the future and make correcting it for uncertainty possible. The software has a basic opinion on the amount of data needed to get a reasonable estimate; it will happily base the expectation on two years. Personally, I would find that nonsense. No history periods or one value will cause an error.

To this end the valuation will be accepting a list of dates and corresponding values.

+--------------+--------------+--------------+--------------+--------------+
| Date         |  1-1-2013    |   1-1-2014   |  1-1-2015    |  1-1-2016    |
+--------------+--------------+--------------+--------------+--------------+
| Value        |   200        |     205      |    220       |    203       |
+--------------+--------------+--------------+--------------+--------------+
| Dividend     |   12         |    18        |    3         |    20        |
+--------------+--------------+--------------+--------------+--------------+

The values are used to determine the historic growth of the value, which is interpolated into the future, until the given valuation date: 

    Expected_growth = (5 + 15 -17) / 3

It is the sum of the difference divided by the duration in years.

For the dividend we sum the dividend amounts and divide by the number of years:

    Expected dividend = (12 + 18 + 3 +20) / 4

For each year from now until the "maturity" date we discount the expected dividend with the applicable discount rate. The sum of the discounted amounts is the value resulting from dividends to be received.

For stocks there is no maturity date. The calculation though needs an end date, like the maturity date for bonds. We will name this "maturity" date "expected selling date" from here.

If the expected selling date is not a full number of years ahead, we will calculate a part of a period with the number of actual days (:ref:`interpolation`), before discounting the amount.

The value at the expected selling date is discounted.


.. rubric:: Footnotes

.. [usediscount] You can use a higher discount rate to express the uncertainty
