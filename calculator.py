"""Calculator functions for dividend tracking and analysis

This module provides functions for calculating dividend income,
yield, projections, and other analytics.
"""

from datetime import date, timedelta
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from calendar import monthrange
from models import Portfolio, Stock, Dividend, DividendSchedule


def calculate_total_dividend_income(
    portfolio: Portfolio,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Decimal:
    """Calculate total dividend income for a given period.
    
    Args:
        portfolio: Portfolio containing dividend history
        start_date: Start date of period (None = all time)
        end_date: End date of period (None = today)
    
    Returns:
        Total dividend income as Decimal
    """
    if end_date is None:
        end_date = date.today()
    
    total = Decimal('0')
    for dividend in portfolio.dividends:
        if start_date and dividend.payment_date < start_date:
            continue
        if dividend.payment_date > end_date:
            continue
        if dividend.payment_status == "paid" or dividend.is_paid:
            total += dividend.total_amount
    
    return total


def calculate_monthly_dividend_income(
    portfolio: Portfolio,
    year: int,
    month: int
) -> Decimal:
    """Calculate dividend income for a specific month.
    
    Args:
        portfolio: Portfolio containing dividend history
        year: Year (e.g., 2025)
        month: Month (1-12)
    
    Returns:
        Total dividend income for the month
    """
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    return calculate_total_dividend_income(portfolio, first_day, last_day)


def calculate_yearly_dividend_income(
    portfolio: Portfolio,
    year: int
) -> Decimal:
    """Calculate dividend income for a specific year.
    
    Args:
        portfolio: Portfolio containing dividend history
        year: Year (e.g., 2025)
    
    Returns:
        Total dividend income for the year
    """
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    return calculate_total_dividend_income(portfolio, start_date, end_date)


def calculate_lifetime_dividend_income(
    portfolio: Portfolio
) -> Decimal:
    """Calculate total dividend income since inception.
    
    Args:
        portfolio: Portfolio containing dividend history
    
    Returns:
        Lifetime dividend income
    """
    return calculate_total_dividend_income(portfolio)


def calculate_dividend_yield(
    stock: Stock,
    annual_dividend_per_share: Decimal
) -> Decimal:
    """Calculate dividend yield for a stock.
    
    Args:
        stock: Stock object
        annual_dividend_per_share: Annual dividend per share
    
    Returns:
        Dividend yield as percentage (e.g., 3.5 for 3.5%)
    """
    if stock.current_price == 0:
        return Decimal('0')
    
    yield_decimal = (annual_dividend_per_share / stock.current_price) * Decimal('100')
    return yield_decimal.quantize(Decimal('0.01'))


def calculate_portfolio_dividend_yield(
    portfolio: Portfolio
) -> Decimal:
    """Calculate weighted average dividend yield for entire portfolio.
    
    Args:
        portfolio: Portfolio containing stocks
    
    Returns:
        Portfolio dividend yield as percentage
    """
    total_value = portfolio.total_portfolio_value
    if total_value == 0:
        return Decimal('0')
    
    weighted_yield = Decimal('0')
    for stock in portfolio.stocks:
        if stock.ticker in portfolio.schedules:
            schedule = portfolio.schedules[stock.ticker]
            annual_dividend = schedule.typical_amount * Decimal(schedule.get_annual_frequency())
            stock_yield = calculate_dividend_yield(stock, annual_dividend)
            weight = stock.total_value / total_value
            weighted_yield += stock_yield * weight
    
    return weighted_yield.quantize(Decimal('0.01'))


def get_upcoming_dividends(
    portfolio: Portfolio,
    days_ahead: int = 30
) -> List[Dividend]:
    """Get list of upcoming dividend payments.
    
    Args:
        portfolio: Portfolio containing dividend history
        days_ahead: Number of days to look ahead
    
    Returns:
        List of upcoming Dividend objects
    """
    today = date.today()
    cutoff_date = today + timedelta(days=days_ahead)
    
    upcoming = [
        div for div in portfolio.dividends
        if div.is_upcoming and div.payment_date <= cutoff_date
    ]
    
    # Sort by payment date
    upcoming.sort(key=lambda d: d.payment_date)
    return upcoming


def get_dividend_history_by_stock(
    portfolio: Portfolio,
    ticker: str
) -> List[Tuple[date, Decimal]]:
    """Get dividend payment history for a specific stock.
    
    Args:
        portfolio: Portfolio containing dividend history
        ticker: Stock ticker symbol
    
    Returns:
        List of (payment_date, amount) tuples
    """
    dividends = portfolio.get_dividends_for_stock(ticker)
    history = [
        (div.payment_date, div.total_amount)
        for div in dividends
        if div.is_paid
    ]
    history.sort(key=lambda x: x[0])
    return history


def calculate_annual_dividend_summary(
    portfolio: Portfolio
) -> Dict[int, Decimal]:
    """Calculate dividend income summary by year.
    
    Args:
        portfolio: Portfolio containing dividend history
    
    Returns:
        Dictionary mapping year -> total income
    """
    summary = {}
    for dividend in portfolio.dividends:
        if dividend.is_paid:
            year = dividend.payment_date.year
            if year not in summary:
                summary[year] = Decimal('0')
            summary[year] += dividend.total_amount
    
    return dict(sorted(summary.items()))


def estimate_future_dividend_income(
    portfolio: Portfolio,
    months_ahead: int = 12
) -> Decimal:
    """Estimate future dividend income based on current holdings and schedules.
    
    Args:
        portfolio: Portfolio with stocks and dividend schedules
        months_ahead: Number of months to project
    
    Returns:
        Estimated future dividend income
    """
    total_estimated = Decimal('0')
    
    for stock in portfolio.stocks:
        if stock.ticker in portfolio.schedules:
            schedule = portfolio.schedules[stock.ticker]
            frequency = schedule.get_annual_frequency()
            payments_in_period = (months_ahead / 12) * frequency
            estimated = schedule.typical_amount * stock.shares * Decimal(payments_in_period)
            total_estimated += estimated
    
    return total_estimated.quantize(Decimal('0.01'))


def calculate_monthly_breakdown(
    portfolio: Portfolio,
    year: int
) -> Dict[int, Decimal]:
    """Calculate dividend income for each month of a year.
    
    Args:
        portfolio: Portfolio containing dividend history
        year: Year to analyze
    
    Returns:
        Dictionary mapping month (1-12) -> income
    """
    breakdown = {}
    for month in range(1, 13):
        breakdown[month] = calculate_monthly_dividend_income(portfolio, year, month)
    
    return breakdown


def get_dividend_growth_rate(
    portfolio: Portfolio,
    ticker: str,
    years: int = 3
) -> Optional[Decimal]:
    """Calculate dividend growth rate for a stock.
    
    Args:
        portfolio: Portfolio containing dividend history
        ticker: Stock ticker symbol
        years: Number of years to analyze
    
    Returns:
        Average annual growth rate as percentage, or None if insufficient data
    """
    dividends = portfolio.get_dividends_for_stock(ticker)
    if not dividends:
        return None
    
    # Group by year
    yearly_totals = {}
    for div in dividends:
        if div.is_paid:
            year = div.payment_date.year
            if year not in yearly_totals:
                yearly_totals[year] = Decimal('0')
            yearly_totals[year] += div.amount_per_share
    
    if len(yearly_totals) < 2:
        return None
    
    # Calculate growth rates
    sorted_years = sorted(yearly_totals.keys())
    if len(sorted_years) < years:
        years = len(sorted_years)
    
    relevant_years = sorted_years[-years:]
    if len(relevant_years) < 2:
        return None
    
    start_amount = yearly_totals[relevant_years[0]]
    end_amount = yearly_totals[relevant_years[-1]]
    
    if start_amount == 0:
        return None
    
    num_years = len(relevant_years) - 1
    growth_rate = ((end_amount / start_amount) ** (Decimal('1') / Decimal(num_years)) - Decimal('1')) * Decimal('100')
    
    return growth_rate.quantize(Decimal('0.01'))
