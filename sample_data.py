"""Sample data for demonstrating the Dividend Tracker App
This module provides example data to help users understand
how to use the dividend tracking system.
"""
from datetime import date, timedelta
from decimal import Decimal
from models import Stock, Dividend, DividendSchedule, Portfolio
from calculator import DividendCalculator

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

if __name__ == "__main__":
    print("="*70)
    print("DIVIDEND TRACKER APP - SAMPLE DATA DEMONSTRATION")
    print("="*70)
    print()
    
    # Create and display sample portfolio
    print("Creating Sample Indian Dividend Portfolio...")
    print()
    portfolio = create_sample_portfolio()
    
    # Display Portfolio Summary
    print("\n" + "="*70)
    print(f"PORTFOLIO: {portfolio.name}")
    print("="*70)
    
    # Display stocks
    print("\n📊 STOCKS IN PORTFOLIO:")
    print("-" * 70)
    for stock in portfolio.stocks.values():
        print(f"\n{stock.name} ({stock.ticker})")
        print(f"  Shares: {stock.shares}")
        print(f"  Purchase Price: ₹{stock.purchase_price}")
        print(f"  Current Price: ₹{stock.current_price}")
        gain_loss = (stock.current_price - stock.purchase_price) * stock.shares
        gain_loss_pct = ((stock.current_price - stock.purchase_price) / stock.purchase_price) * 100
        print(f"  Gain/Loss: ₹{gain_loss:.2f} ({gain_loss_pct:.2f}%)")
        print(f"  Total Value: ₹{stock.current_price * stock.shares:.2f}")
    
    # Display dividend schedules
    print("\n\n💰 DIVIDEND SCHEDULES:")
    print("-" * 70)
    for schedule in portfolio.schedules.values():
        print(f"\n{schedule.ticker}:")
        print(f"  Frequency: {schedule.frequency}")
        print(f"  Typical Amount: ₹{schedule.typical_amount} per share")
        print(f"  Last Ex-Dividend Date: {schedule.last_ex_dividend_date}")
        print(f"  Next Payment Date: {schedule.next_payment_date}")
    
    # Calculate and display analytics
    print("\n\n📈 PORTFOLIO ANALYTICS:")
    print("-" * 70)
    
    calc = DividendCalculator(portfolio)
    
    # Total dividends received
    total_dividends = calc.total_dividends_received()
    print(f"\nTotal Dividends Received (All Time): ₹{total_dividends:.2f}")
    
    # Annual dividend income
    annual_income = calc.annual_dividend_income()
    print(f"Projected Annual Dividend Income: ₹{annual_income:.2f}")
    
    # Portfolio value
    total_invested = sum(stock.purchase_price * stock.shares for stock in portfolio.stocks.values())
    total_current_value = sum(stock.current_price * stock.shares for stock in portfolio.stocks.values())
    print(f"\nTotal Amount Invested: ₹{total_invested:.2f}")
    print(f"Current Portfolio Value: ₹{total_current_value:.2f}")
    print(f"Total Gain/Loss: ₹{total_current_value - total_invested:.2f}")
    
    # Dividend yield
    if total_current_value > 0:
        dividend_yield = (annual_income / total_current_value) * 100
        print(f"Portfolio Dividend Yield: {dividend_yield:.2f}%")
    
    # Display historical dividends summary
    print("\n\n📜 HISTORICAL DIVIDENDS (Recent):")
    print("-" * 70)
    
    # Sort dividends by date (most recent first)
    sorted_dividends = sorted(portfolio.dividends, key=lambda d: d.payment_date, reverse=True)
    
    print(f"\n{'Date':<15} {'Ticker':<12} {'Amount/Share':<15} {'Shares':<10} {'Total':<10}")
    print("-" * 70)
    
    for div in sorted_dividends[:10]:  # Show last 10 dividends
        total = div.amount_per_share * div.shares
        print(f"{div.payment_date} {div.ticker:<12} ₹{div.amount_per_share:<14.2f} {div.shares:<10} ₹{total:.2f}")
    
    print("\n" + "="*70)
    print("END OF SAMPLE DATA DEMONSTRATION")
    print("="*70)
    print("\nTo use this data in your own code, import and call:")
    print("  from sample_data import create_sample_portfolio")
    print("  portfolio = create_sample_portfolio()")
    print()
