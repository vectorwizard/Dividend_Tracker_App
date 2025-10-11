"""Sample data for demonstrating the Dividend Tracker App
This module provides example data to help users understand
how to use the dividend tracking system.
"""
from datetime import date, timedelta
from decimal import Decimal
from models import Stock, Dividend, DividendSchedule, Portfolio

def create_sample_portfolio() -> Portfolio:
    """Create a sample portfolio with example Indian stocks and dividend data.
    
    Returns:
        Portfolio object populated with sample data from Indian Stock Market (NSE)
    """
    portfolio = Portfolio(name="Sample Indian Dividend Portfolio")
    
    # Sample Stock 1: Reliance Industries (RELIANCE)
    reliance = Stock(
        ticker="RELIANCE",
        name="Reliance Industries Limited",
        shares=Decimal('50'),
        purchase_price=Decimal('2400.00'),
        current_price=Decimal('2650.00'),
        currency="INR"
    )
    portfolio.add_stock(reliance)
    
    # Sample Stock 2: Tata Consultancy Services (TCS)
    tcs = Stock(
        ticker="TCS",
        name="Tata Consultancy Services Limited",
        shares=Decimal('30'),
        purchase_price=Decimal('3200.00'),
        current_price=Decimal('3750.00'),
        currency="INR"
    )
    portfolio.add_stock(tcs)
    
    # Sample Stock 3: HDFC Bank (HDFCBANK)
    hdfcbank = Stock(
        ticker="HDFCBANK",
        name="HDFC Bank Limited",
        shares=Decimal('40'),
        purchase_price=Decimal('1550.00'),
        current_price=Decimal('1680.00'),
        currency="INR"
    )
    portfolio.add_stock(hdfcbank)
    
    # Sample Stock 4: Infosys (INFY)
    infy = Stock(
        ticker="INFY",
        name="Infosys Limited",
        shares=Decimal('60'),
        purchase_price=Decimal('1420.00'),
        current_price=Decimal('1580.00'),
        currency="INR"
    )
    portfolio.add_stock(infy)
    
    # Add dividend schedules for each stock
    # Reliance typically pays semi-annual dividends
    reliance_schedule = DividendSchedule(
        ticker="RELIANCE",
        frequency="semi-annual",
        typical_amount=Decimal('8.00'),  # ₹8 per share per payment
        last_ex_dividend_date=date(2024, 9, 12),
        next_payment_date=date(2025, 3, 15)
    )
    portfolio.add_schedule(reliance_schedule)
    
    # TCS typically pays quarterly dividends
    tcs_schedule = DividendSchedule(
        ticker="TCS",
        frequency="quarterly",
        typical_amount=Decimal('27.00'),  # ₹27 per share per quarter
        last_ex_dividend_date=date(2024, 10, 10),
        next_payment_date=date(2025, 1, 15)
    )
    portfolio.add_schedule(tcs_schedule)
    
    # HDFC Bank typically pays quarterly dividends
    hdfcbank_schedule = DividendSchedule(
        ticker="HDFCBANK",
        frequency="quarterly",
        typical_amount=Decimal('19.50'),  # ₹19.50 per share per quarter
        last_ex_dividend_date=date(2024, 9, 18),
        next_payment_date=date(2025, 1, 10)
    )
    portfolio.add_schedule(hdfcbank_schedule)
    
    # Infosys typically pays quarterly dividends
    infy_schedule = DividendSchedule(
        ticker="INFY",
        frequency="quarterly",
        typical_amount=Decimal('20.00'),  # ₹20 per share per quarter
        last_ex_dividend_date=date(2024, 10, 15),
        next_payment_date=date(2025, 1, 20)
    )
    portfolio.add_schedule(infy_schedule)
    
    # Add historical dividend payments
    today = date.today()
    
    # Reliance historical dividends (past year, semi-annual)
    portfolio.add_dividend(Dividend(
        ticker="RELIANCE",
        payment_date=today - timedelta(days=90),
        amount_per_share=Decimal('8.00'),
        shares=Decimal('50')
    ))
    portfolio.add_dividend(Dividend(
        ticker="RELIANCE",
        payment_date=today - timedelta(days=270),
        amount_per_share=Decimal('7.50'),
        shares=Decimal('50')
    ))
    
    # TCS historical dividends (past year, quarterly)
    for i, days_ago in enumerate([30, 120, 210, 300]):
        portfolio.add_dividend(Dividend(
            ticker="TCS",
            payment_date=today - timedelta(days=days_ago),
            amount_per_share=Decimal('27.00'),
            shares=Decimal('30')
        ))
    
    # HDFC Bank historical dividends (past year, quarterly)
    for i, days_ago in enumerate([45, 135, 225, 315]):
        portfolio.add_dividend(Dividend(
            ticker="HDFCBANK",
            payment_date=today - timedelta(days=days_ago),
            amount_per_share=Decimal('19.50'),
            shares=Decimal('40')
        ))
    
    # Infosys historical dividends (past year, quarterly)
    for i, days_ago in enumerate([25, 115, 205, 295]):
        portfolio.add_dividend(Dividend(
            ticker="INFY",
            payment_date=today - timedelta(days=days_ago),
            amount_per_share=Decimal('20.00'),
            shares=Decimal('60')
        ))
    
    return portfolio

def create_minimal_portfolio() -> Portfolio:
    """Create a minimal portfolio for basic testing.
    
    Returns:
        Portfolio object with minimal sample data
    """
    portfolio = Portfolio(name="Minimal Indian Portfolio")
    
    # Single stock: TCS
    tcs = Stock(
        ticker="TCS",
        name="Tata Consultancy Services Limited",
        shares=Decimal('10'),
        purchase_price=Decimal('3500.00'),
        current_price=Decimal('3750.00'),
        currency="INR"
    )
    portfolio.add_stock(tcs)
    
    # Single dividend schedule
    tcs_schedule = DividendSchedule(
        ticker="TCS",
        frequency="quarterly",
        typical_amount=Decimal('27.00'),
        last_ex_dividend_date=date(2024, 10, 10),
        next_payment_date=date(2025, 1, 15)
    )
    portfolio.add_schedule(tcs_schedule)
    
    # Single dividend payment
    portfolio.add_dividend(Dividend(
        ticker="TCS",
        payment_date=date.today() - timedelta(days=30),
        amount_per_share=Decimal('27.00'),
        shares=Decimal('10')
    ))
    
    return portfolio
