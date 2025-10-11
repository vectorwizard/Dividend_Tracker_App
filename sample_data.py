"""Sample data for demonstrating the Dividend Tracker App

This module provides example data to help users understand
how to use the dividend tracking system.
"""

from datetime import date, timedelta
from decimal import Decimal
from models import Stock, Dividend, DividendSchedule, Portfolio


def create_sample_portfolio() -> Portfolio:
    """Create a sample portfolio with example stocks and dividend data.
    
    Returns:
        Portfolio object populated with sample data
    """
    portfolio = Portfolio(name="Sample Dividend Portfolio")
    
    # Sample Stock 1: Apple (AAPL)
    aapl = Stock(
        ticker="AAPL",
        name="Apple Inc.",
        shares=Decimal('100'),
        purchase_price=Decimal('150.00'),
        current_price=Decimal('175.00'),
        currency="USD"
    )
    portfolio.add_stock(aapl)
    
    # Sample Stock 2: Microsoft (MSFT)
    msft = Stock(
        ticker="MSFT",
        name="Microsoft Corporation",
        shares=Decimal('50'),
        purchase_price=Decimal('300.00'),
        current_price=Decimal('350.00'),
        currency="USD"
    )
    portfolio.add_stock(msft)
    
    # Sample Stock 3: Coca-Cola (KO)
    ko = Stock(
        ticker="KO",
        name="The Coca-Cola Company",
        shares=Decimal('200'),
        purchase_price=Decimal('55.00'),
        current_price=Decimal('60.00'),
        currency="USD"
    )
    portfolio.add_stock(ko)
    
    # Sample Stock 4: Johnson & Johnson (JNJ)
    jnj = Stock(
        ticker="JNJ",
        name="Johnson & Johnson",
        shares=Decimal('75'),
        purchase_price=Decimal('160.00'),
        current_price=Decimal('165.00'),
        currency="USD"
    )
    portfolio.add_stock(jnj)
    
    # Add dividend schedules
    aapl_schedule = DividendSchedule(
        ticker="AAPL",
        frequency="quarterly",
        typical_amount=Decimal('0.24'),
        last_ex_dividend_date=date(2025, 8, 12),
        next_payment_date=date(2025, 11, 14)
    )
    portfolio.add_schedule(aapl_schedule)
    
    msft_schedule = DividendSchedule(
        ticker="MSFT",
        frequency="quarterly",
        typical_amount=Decimal('0.75'),
        last_ex_dividend_date=date(2025, 8, 15),
        next_payment_date=date(2025, 11, 7)
    )
    portfolio.add_schedule(msft_schedule)
    
    ko_schedule = DividendSchedule(
        ticker="KO",
        frequency="quarterly",
        typical_amount=Decimal('0.46'),
        last_ex_dividend_date=date(2025, 9, 15),
        next_payment_date=date(2025, 12, 15)
    )
    portfolio.add_schedule(ko_schedule)
    
    jnj_schedule = DividendSchedule(
        ticker="JNJ",
        frequency="quarterly",
        typical_amount=Decimal('1.13'),
        last_ex_dividend_date=date(2025, 8, 26),
        next_payment_date=date(2025, 12, 10)
    )
    portfolio.add_schedule(jnj_schedule)
    
    # Add historical dividends (past year)
    today = date.today()
    
    # AAPL historical dividends
    for i in range(4):
        payment_date = date(2024, 11, 14) + timedelta(days=i*91)
        if payment_date < today:
            div = Dividend(
                ticker="AAPL",
                payment_date=payment_date,
                amount_per_share=Decimal('0.24'),
                shares_owned=Decimal('100'),
                payment_status="paid"
            )
            portfolio.add_dividend(div)
    
    # MSFT historical dividends
    for i in range(4):
        payment_date = date(2024, 11, 7) + timedelta(days=i*91)
        if payment_date < today:
            div = Dividend(
                ticker="MSFT",
                payment_date=payment_date,
                amount_per_share=Decimal('0.75'),
                shares_owned=Decimal('50'),
                payment_status="paid"
            )
            portfolio.add_dividend(div)
    
    # KO historical dividends
    for i in range(4):
        payment_date = date(2024, 12, 15) + timedelta(days=i*91)
        if payment_date < today:
            div = Dividend(
                ticker="KO",
                payment_date=payment_date,
                amount_per_share=Decimal('0.46'),
                shares_owned=Decimal('200'),
                payment_status="paid"
            )
            portfolio.add_dividend(div)
    
    # JNJ historical dividends
    for i in range(4):
        payment_date = date(2024, 12, 10) + timedelta(days=i*91)
        if payment_date < today:
            div = Dividend(
                ticker="JNJ",
                payment_date=payment_date,
                amount_per_share=Decimal('1.13'),
                shares_owned=Decimal('75'),
                payment_status="paid"
            )
            portfolio.add_dividend(div)
    
    # Add upcoming dividends
    upcoming_aapl = Dividend(
        ticker="AAPL",
        payment_date=date(2025, 11, 14),
        amount_per_share=Decimal('0.24'),
        shares_owned=Decimal('100'),
        payment_status="pending"
    )
    portfolio.add_dividend(upcoming_aapl)
    
    upcoming_msft = Dividend(
        ticker="MSFT",
        payment_date=date(2025, 11, 7),
        amount_per_share=Decimal('0.75'),
        shares_owned=Decimal('50'),
        payment_status="pending"
    )
    portfolio.add_dividend(upcoming_msft)
    
    upcoming_ko = Dividend(
        ticker="KO",
        payment_date=date(2025, 12, 15),
        amount_per_share=Decimal('0.46'),
        shares_owned=Decimal('200'),
        payment_status="pending"
    )
    portfolio.add_dividend(upcoming_ko)
    
    upcoming_jnj = Dividend(
        ticker="JNJ",
        payment_date=date(2025, 12, 10),
        amount_per_share=Decimal('1.13'),
        shares_owned=Decimal('75'),
        payment_status="pending"
    )
    portfolio.add_dividend(upcoming_jnj)
    
    return portfolio


if __name__ == "__main__":
    # Example usage
    portfolio = create_sample_portfolio()
    
    print(f"\n{'='*60}")
    print(f"Portfolio: {portfolio.name}")
    print(f"{'='*60}\n")
    
    print("Stocks in Portfolio:")
    print("-" * 60)
    for stock in portfolio.stocks:
        print(f"{stock.ticker:6} {stock.name:30} {stock.shares:>6} shares")
        print(f"       Purchase: ${stock.purchase_price:>8.2f}  Current: ${stock.current_price:>8.2f}")
        print(f"       Total Value: ${stock.total_value:>10.2f}  Gain/Loss: ${stock.unrealized_gain:>10.2f}\n")
    
    print(f"\nTotal Portfolio Value: ${portfolio.total_portfolio_value:,.2f}")
    print(f"\n{'='*60}\n")
