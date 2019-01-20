"""
Mortgage-related tools.

A mortgage is a type of financial loan. The lender offers a sum of money with
a certain interest rate. The loan and interest are repaid over a fixed time
interval with constant payments.

Payments and interest are usually calculated on a montly basis. The payment for
each month first pays off the interest, then the remaining amount is credited
towards paying off the principal loan amount.

The tools in this module are aimed at mortgages with fixed rates and loan
payback periods. Variable-rate mortgages are not covered.

Change log:
  2016/03/19 -- module started; nloomis@gmail.com
  2016/06/01 -- documentation added; nloomis@gmail.com
"""
__authors__ = ('nloomis@gmail.com',)

from collections import namedtuple
import numpy

class Mortgage(object):
  def __init__(self, principal, apr, num_years):
    """Initialize a Mortgage object.

    principal: the total amount of the loan
    apr: the quoted annual percentage rate; for example, if a lender offers
      a rate of 3.25%, use apr=3.25
    num_years: the number of years for the mortgage
    """
    self.principal = principal
    # Convert the apr from "X.YZ%" to 0.0XYZ (a numerical rate vs a quoted rate)
    self.apr = apr / 100.
    self.num_years = num_years
    # Monthly interest rate, assuming twelve payments and re-calculations of
    # interest each year.
    self.rate = self.apr / 12.0
    # Total number of payments, assuming one per month.
    self.num_payments = 12 * num_years
  
  @property
  def payment(self):
    """Returns the per-month payment to pay off the mortage.

    The montly payment will exactly pay off the loan at the end of the mortgage
    term if no additional payments are provided.
    See https://en.wikipedia.org/wiki/Amortization_calculator for discussion of
    the math behind the mortgage annuity payment."""
    # exponential growth over the total period
    exponential = (1 + self.rate) ** self.num_payments
    # fraction of the original principal paid each period
    annuity_rate = self.rate * exponential / (exponential - 1)
    return annuity_rate * self.principal

  MonthlySnapshot = namedtuple("MonthlySnapshot", ["month", "interest",
      "principal_paid", "principal"])

  def Schedule(self, verbose=False, additional_payments=None):
    """Determines the effect of additional payments on the principle.

    A mortgage is designed to be paid off using constant payment amounts over
    the lifetime of the mortgage. Mortgages may allow the borrower to pay more
    than the monthly payment, which reduces the principal faster and pays off
    the loan sooner. The exact time when the loan gets paid off is easier to
    find by simulating the entier set of scheduled and additional payments.

    Schedule() starts by assuming that the borrower submits the exact payment
    required each month to pay off the mortgage in the loan's original time
    period. A vector of additional_payments denotes how much, if any, additional
    amount is paid into the mortgage during each time period. For example, to
    pay an additional $10 in the third time period use:

      additional_payments = numpy.zeros(Mortgage.num_payments)
      additional_payments[2] = 10

    A tuple with (final_period, over_payment) is returned at the end. The
    final_period is the payment period when the loan is considered completely
    paid off. If the last payment is larger than the remaining principle and
    interest, the excess amount is denoted in over_payment. For example, if the
    payment was $100 and exactly $80 in principal and interest remained, the
    over-payment would be $20.

    Set verbose=True to print the schedule and related information to the
    console.
    """
    # TODO(nloomis): update docs, returns for history[]! Also, don't need to
    # explicitly return the time, t, if the entire schedule is returned.
    
    # Make the additional payments vector at least as long as the expected
    # number of payments. NB: be careful if you're using negative numbers in the
    # additional_payments vector (for example, to represent a missed payment):
    # the loan may go beyond its intended num_payments if the missing payment
    # isn't made up for later on. It is OK to pass an additional_payments
    # vector larger than num_payments, however, if going over the loan's time
    # frame is a concern. 
    if additional_payments is None:
      additional_payments = numpy.zeros((self.num_payments,))
    if additional_payments.size < self.num_payments:
      nz = self.num_payments - additional_payments.size
      additional_payments = numpy.concatenate((additional_payments,
                                               numpy.zeros(nz,)))
    # Payment amount per period.
    payment = self.payment

    if verbose:
      # Print the payment and a table header.
      print("Monthly payment = %s" % (payment,))
      print " "
      print("Period      Interest    Principal")
      print("=======================================")

    # Principal remaining just before the payment occurs.
    init_principal = [self.principal]
    # Total amount of interest paid off.
    total_interest = 0;
    # Reset the current time.
    t = 0
 
    # Create a container to hold monthly snapshots of the payments.
    history = []

    # Calculate the interest and remaining principle each month until the
    # mortgage is paid off. The loan is repaid once the initial principle at
    # the start of each month goes below one cent.
    while init_principal[t] > 0.01:
      # Find the interest accrued during this period.
      interest_amount = self.rate * init_principal[t]
      total_interest += interest_amount;
      # Find how much of the payment goes towards interest, and how much goes
      # toward the principal.
      principal_reduction = max(payment - interest_amount, 0) + \
                            additional_payments[t]
      # The mortgage is overpaid if the monthly payment exceeds the amount still
      # due on the mortgage.
      overpayment = principal_reduction - init_principal[t]
      # Keep track of the principal still due at the start of the next payment
      # period.
      principal_remaining = max(init_principal[t] - principal_reduction, 0)
      init_principal.append(principal_remaining)

      history.append(self.MonthlySnapshot(t, interest_amount, principal_reduction,
          principal_remaining))

      # print the schedule
      if verbose:
        print("Period %s:  %6.2f    %6.2f" % \
         (repr(t + 1).ljust(3), interest_amount, init_principal[t+1]))

      # increment the time period.
      t += 1

    if verbose and overpayment > 0.1:
      print "Overpaid: %6.2f" % overpayment
    if verbose:
      print "Total interest paid: %6.2f" % total_interest

    # Return the time period when the last payment occurred and the overpayment
    # on the mortgage during the final period.
    return t, overpayment, history

  def OverpaymentPresentValue(self, amount, payment_period, apr):
    """Finds the value of over-paying a mortgage during one repayment period.

    People generally think that paying off a loan quickly is good. But is it
    always the best financial choice?

    Consider a simple example: you did great this year, and were awarded a nice
    bonus at work. You could do one of two things:
      1) use the bonus to make a larger-than-usual payment on your mortgage,
         decreasing the principal and paying off the mortgage sooner; then, the
         money you would have put towards your monthly mortgage payment could be
         used for investing in the market (stocks, bonds, mutuals, etc)
      2) invest the bonus in the market right away and keep paying your mortgage
         like usual

    At the end of the mortgage term, which option is better?

    One solution is to calculate how much you could expect to make on each
    option, then compare the two. That will tell you which is better, but it may
    not give you a sense for how much better in today's dollars.

    Another appoach is to calculate how much you'd need to invest in the market
    today in order to make the same amount as you'd have at the end of the
    mortgage lifetime using option #1. This is known as the /present value/ of
    your future investment, and it gives us a better sense of the worth of that
    future investment in dollar amounts we can understand.

    amount: the bonus payment on top of the regular mortgage payment, to be
      made during a single period
    payment_period: which period the bonus amount is paid into the mortgage
    apr: the annual percentage rate of the assumed market investments as the
      numerical rate; for example, a 2% APR has apr=0.02
    
    The present value of Option 1 is returned.

    Remember that the present value is the amount you would need to invest now
    to make the same amount as if you invested the series of payments at the end
    of the mortgage. If the present value is MORE than the bonus payment, then
    it indicates that paying off the mortgage early is financially worthwhile.
    If the present value is LESS than the bonus payment amount, then it would
    be better financially to invest in the market now (option 2) instead of
    paying off the mortgage early.

    A few caveats: investments usually have some fees associated with them (for
    example, annual management fees). The APR should be the equivalent growth
    rate after any fees are subtracted. Secondly, we're not looking at the
    tax benefits of paying off the mortgage early (or not). Third, this is a
    purely financial calculation, and you have to add your own consideration for
    the value of having a mortgage paid off (for example, peace of mind).
    Finally, any market will have uncertainty, so this is the expected value
    of any investments.
    """
    # vector of overpayments which would occur if the amount was applied to 
    # the mortgage during a specific payment period
    additional_payments = numpy.zeros((self.num_payments,))
    additional_payments[payment_period - 1] = amount
    num_actual_payments, final_overpayment = self.Schedule(verbose=False,
      additional_payments=additional_payments)
    print "Mortage paid off during period %s, with %6.2f remaining" % \
      (num_actual_payments, final_overpayment)
    # find the number of times the full mortgage amount could be invested
    num_invest = self.num_payments - num_actual_payments
    # find how much could be invested at each period, and at what rate
    period_payment = self.payment
    print "A total of %s investments can be made with the annuity of %6.2f" % \
      (num_invest, period_payment)
    period_rate = apr / 12.0
    # construct the set of payments and how many periods after the overpayment
    # each occurs in
    investment_amounts = numpy.hstack((numpy.array([final_overpayment]),
      numpy.ones((num_invest,)) * period_payment))
    investment_delay = numpy.linspace(0, num_invest, 1 + num_invest) + \
      self.num_payments - payment_period - 1
    print "Investment amounts: %s" % investment_amounts
    print "can be made %s periods after the overpayment" % investment_delay
    # find the present value of each investment
    present_values = [PresentValue(fv, period_rate, p) \
      for fv, p in zip(investment_amounts, investment_delay)]
    print "Present values are: %s" % present_values
    return numpy.array(present_values).sum()

# end of Mortgage class


def PresentValue(future_amount, interest_rate, periods):
  """Returns the present value of some future value.

  interest rate: as a value (ie, 0.02 is the value for 2% per period)
  periods: total number of interest payments which will be made

  For more, see https://en.wikipedia.org/wiki/Present_value
  """
  return future_amount / (1.0 + interest_rate)**periods

# TODO(nloomis): also consider the savings you'd get by reducing your AGI each
# year, given some guesses about the tax brackets. That analysis  might be a
# good part of Schedule().
# For example: if you're in the 25% tax bracket, your net taxes are reduced by
# about 25% of the amount you pay in interest. That means that you're only
# "losing" 75% of the interest in the end.

def PresentValueAnnuity(payment, interest_rate, periods):
  """Foo!"""
  a = (1. - (1. + interest_rate)**(-periods)) / interest_rate
  return payment * a
  