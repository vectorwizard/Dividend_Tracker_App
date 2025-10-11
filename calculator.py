"""Calculator functions for dividend tracking and analysis
This module provides functions for calculating dividend income,
yield, projections, and other analytics.
"""
from datetime import date, timedelta
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from calendar import monthrange
from models import Portfolio, Stock, Dividend, DividendSchedule

def format_inr(amount: Decimal) -> str:
    """Format amount in Indian Rupees (INR) with proper currency symbol.
    
    Args:
        amount: Amount to format
    
    Returns:
        Formatted string with ₹ symbol and comma separators
    """
    return f"₹{amount:,.2f}"

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
        Total dividend income as Decimal (in INR)
    """
    if end_date is None:
        end_date = date.today()
    
    total = Decimal('0')
    for dividend in portfolio.dividends:
        if start_date and dividend.payment_date < start_date:
            continue
        if dividend.payment_date > end_date:
            continue
        total += dividend.total_amount
    
    return total

def calculate_annual_dividend_income(portfolio: Portfolio) -> Decimal:
    """Calculate expected annual dividend income based on schedules.
    
    Args:
        portfolio: Portfolio containing stocks and dividend schedules
    
    Returns:
        Expected annual dividend income as Decimal (in INR)
    """
    total_annual = Decimal('0')
    
    for ticker, schedule in portfolio.schedules.items():
        stock = portfolio.get_stock(ticker)
        if stock:
            annual_frequency = schedule.get_annual_frequency()
            annual_dividend_per_share = schedule.typical_amount * Decimal(str(annual_frequency))
            annual_total = annual_dividend_per_share * stock.shares
            total_annual += annual_total
    
    return total_annual

def calculate_dividend_yield(stock: Stock, annual_dividend_per_share: Decimal) -> Decimal:
    """Calculate dividend yield for a stock.
    
    Args:
        stock: Stock to calculate yield for
        annual_dividend_per_share: Annual dividend per share (in INR)
    
    Returns:
        Dividend yield as percentage (e.g., 3.5 for 3.5%)
    """
    if stock.current_price == 0:
        return Decimal('0')
    
    yield_value = (annual_dividend_per_share / stock.current_price) * Decimal('100')
    return yield_value

def calculate_portfolio_dividend_yield(portfolio: Portfolio) -> Decimal:
    """Calculate weighted average dividend yield for entire portfolio.
    
    Args:
        portfolio: Portfolio to calculate yield for
    
    Returns:
        Portfolio dividend yield as percentage
    """
    total_value = portfolio.total_portfolio_value
    if total_value == 0:
        return Decimal('0')
    
    annual_income = calculate_annual_dividend_income(portfolio)
    yield_value = (annual_income / total_value) * Decimal('100')
    return yield_value

def project_dividend_income(
    portfolio: Portfolio,
    months: int,
    growth_rate: Decimal = Decimal('0')
) -> List[Tuple[date, Decimal]]:
    """Project future dividend income month by month.
    
    Args:
        portfolio: Portfolio to project from
        months: Number of months to project
        growth_rate: Annual dividend growth rate as percentage (e.g., 10 for 10%)
    
    Returns:
        List of tuples (date, projected_income)
    """
    projections = []
    current_date = date.today()
    monthly_growth = (Decimal('1') + (growth_rate / Decimal('100'))) ** (Decimal('1') / Decimal('12'))
    
    for month_offset in range(months):
        # Calculate the target month
        target_month = current_date.month + month_offset
        target_year = current_date.year + (target_month - 1) // 12
        target_month = ((target_month - 1) % 12) + 1
        
        # Get last day of target month
        last_day = monthrange(target_year, target_month)[1]
        month_end = date(target_year, target_month, last_day)
        
        # Calculate expected income for this month
        monthly_income = Decimal('0')
        growth_factor = monthly_growth ** Decimal(str(month_offset))
        
        for ticker, schedule in portfolio.schedules.items():
            stock = portfolio.get_stock(ticker)
            if stock:
                frequency = schedule.get_annual_frequency()
                # Distribute annual dividends across expected payment months
                monthly_expected = (schedule.typical_amount * stock.shares * 
                                  Decimal(str(frequency)) / Decimal('12'))
                monthly_income += monthly_expected * growth_factor
        
        projections.append((month_end, monthly_income))
    
    return projections

def calculate_dividend_growth_rate(
    portfolio: Portfolio,
    ticker: str,
    years: int = 3
) -> Optional[Decimal]:
    """Calculate historical dividend growth rate for a stock.
    
    Args:
        portfolio: Portfolio containing dividend history
        ticker: Stock ticker to analyze
        years: Number of years to look back
    
    Returns:
        Average annual growth rate as percentage, or None if insufficient data
    """
    dividends = portfolio.get_dividends_for_stock(ticker)
    if len(dividends) < 2:
        return None
    
    # Sort by payment date
    sorted_dividends = sorted(dividends, key=lambda d: d.payment_date)
    
    # Calculate year-over-year growth rates
    growth_rates = []
    for i in range(1, len(sorted_dividends)):
        if sorted_dividends[i-1].amount_per_share > 0:
            rate = ((sorted_dividends[i].amount_per_share - 
                    sorted_dividends[i-1].amount_per_share) / 
                   sorted_dividends[i-1].amount_per_share) * Decimal('100')
            growth_rates.append(rate)
    
    if not growth_rates:
        return None
    
    # Return average growth rate
    return sum(growth_rates) / Decimal(str(len(growth_rates)))

def generate_dividend_summary(portfolio: Portfolio) -> Dict[str, any]:
    """Generate comprehensive dividend summary for portfolio.
    
    Args:
        portfolio: Portfolio to summarize
    
    Returns:
        Dictionary containing various metrics and summaries (all amounts in INR)
    """
    today = date.today()
    year_start = date(today.year, 1, 1)
    
    summary = {
        'total_portfolio_value': portfolio.total_portfolio_value,
        'total_portfolio_value_formatted': format_inr(portfolio.total_portfolio_value),
        'annual_dividend_income': calculate_annual_dividend_income(portfolio),
        'annual_dividend_income_formatted': format_inr(calculate_annual_dividend_income(portfolio)),
        'ytd_dividend_income': calculate_total_dividend_income(portfolio, year_start, today),
        'ytd_dividend_income_formatted': format_inr(calculate_total_dividend_income(portfolio, year_start, today)),
        'portfolio_yield': calculate_portfolio_dividend_yield(portfolio),
        'number_of_stocks': len(portfolio.stocks),
        'total_dividends_received': len(portfolio.dividends),
        'currency': 'INR',
        'stocks': []
    }
    
    # Add per-stock details
    for stock in portfolio.stocks:
        schedule = portfolio.schedules.get(stock.ticker)
        if schedule:
            annual_dividend_per_share = (schedule.typical_amount * 
                                        Decimal(str(schedule.get_annual_frequency())))
            stock_yield = calculate_dividend_yield(stock, annual_dividend_per_share)
            annual_income = annual_dividend_per_share * stock.shares
        else:
            stock_yield = Decimal('0')
            annual_income = Decimal('0')
        
        stock_info = {
            'ticker': stock.ticker,
            'name': stock.name,
            'shares': stock.shares,
            'current_price': stock.current_price,
            'current_price_formatted': format_inr(stock.current_price),
            'total_value': stock.total_value,
            'total_value_formatted': format_inr(stock.total_value),
            'annual_dividend_income': annual_income,
            'annual_dividend_income_formatted': format_inr(annual_income),
            'dividend_yield': stock_yield,
            'unrealized_gain': stock.unrealized_gain,
            'unrealized_gain_formatted': format_inr(stock.unrealized_gain),
            'unrealized_gain_percentage': stock.unrealized_gain_percentage
        }
        summary['stocks'].append(stock_info)
    
    return summary
