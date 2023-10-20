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

A buy-back agreement
--------------------

On a buy back agreement the value of the agreement is the  current value of the amount that is received on a moment in the future. Strictly that value needs to be the discounted value at this moment of the future receipt.

Discounting a future income is dependent on the interest rate and the risk profile of the contract. For a buy-back agreement there is a debtor risk (defaulting of the counterparty) and the risk of the asset that is to be sold not providing the expected returns. Neither of the two risks can be examined without knowledge of the situation of the company. 

A leasing agreement
-------------------

Stocks and bonds
----------------

For stocks and bonds we will calculate the return in dividend or interest and the changes in value of the asset.

A major question here is the uncertainty of the returns on these assets. Dividends are following the performance of the company and the value of stocks and bonds are influenced by the economic outlook as well. We will not take the risks of the assets into account [usediscount]_. Value will be based on the valuation of the asset in the past. We will apply the mean growth over a past periods to estimate the growth in the future and make correcting it for uncertainty possible. The software has no opinion on the amount of data needed to get a reasonable estimate; it will happily base the expectation on a single year. Personally, I would find that nonsense.

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

The amount obtained is discounted with a discount rate.

For the dividend we sum the didvidend amounts and divide by the number of years:

    Expected dividend = (12 + 18 + 3 +20) / 4

For each year from now until the "maturity" date we discount the expected dividend with the applicable discount rate. The sum of the discounted amounts is the value resulting from dividends to be received.

If the "maturity" date is not a full number of years ahead, we will calculate a part of a period with the number of actual days (:ref:`interpolation`), before discounting the amount.

For stocks there is no maturity date. That is why "maturity" is quoted. The calculation needs an end date, like the maturity date for bonds.

.. rubric:: Footnotes

.. [usediscount] You can use a higher discount rate to express the uncertainty
