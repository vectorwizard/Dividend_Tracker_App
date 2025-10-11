"""Example usage of the Dividend Tracker App

This script demonstrates how to use all the features of the dividend tracking system.
"""

from datetime import date
from decimal import Decimal
from sample_data import create_sample_portfolio
from calculator import (
    calculate_total_dividend_income,
    calculate_monthly_dividend_income,
    calculate_yearly_dividend_income,
    calculate_lifetime_dividend_income,
    calculate_dividend_yield,
    calculate_portfolio_dividend_yield,
    get_upcoming_dividends,
    get_dividend_history_by_stock,
    calculate_annual_dividend_summary,
    estimate_future_dividend_income,
    calculate_monthly_breakdown,
    get_dividend_growth_rate
)


def main():
    """Main function demonstrating all dividend tracking features."""
    
    # Create sample portfolio
    print("\n" + "="*70)
    print("DIVIDEND TRACKER APP - EXAMPLE USAGE")
    print("="*70 + "\n")
    
    portfolio = create_sample_portfolio()
    
    print(f"Portfolio: {portfolio.name}")
    print(f"Total Portfolio Value: ${portfolio.total_portfolio_value:,.2f}")
    print("\n" + "-"*70 + "\n")
    
    # Display all stocks in portfolio
    print("STOCKS IN PORTFOLIO:")
    print("-"*70)
    for stock in portfolio.stocks:
        print(f"\n{stock.ticker} - {stock.name}")
        print(f"  Shares: {stock.shares}")
        print(f"  Purchase Price: ${stock.purchase_price:.2f}")
        print(f"  Current Price: ${stock.current_price:.2f}")
        print(f"  Total Value: ${stock.total_value:,.2f}")
        print(f"  Unrealized Gain/Loss: ${stock.unrealized_gain:,.2f}")
        
        # Display dividend yield if schedule exists
        if stock.ticker in portfolio.schedules:
            schedule = portfolio.schedules[stock.ticker]
            annual_dividend = schedule.typical_amount * Decimal(schedule.get_annual_frequency())
            div_yield = calculate_dividend_yield(stock, annual_dividend)
            print(f"  Dividend Yield: {div_yield:.2f}%")
            print(f"  Annual Dividend: ${annual_dividend * stock.shares:.2f}")
    
    print("\n" + "="*70 + "\n")
    
    # Calculate portfolio dividend yield
    portfolio_yield = calculate_portfolio_dividend_yield(portfolio)
    print(f"PORTFOLIO DIVIDEND YIELD: {portfolio_yield:.2f}%")
    print("\n" + "="*70 + "\n")
    
    # Display lifetime dividend income
    lifetime_income = calculate_lifetime_dividend_income(portfolio)
    print(f"LIFETIME DIVIDEND INCOME: ${lifetime_income:,.2f}")
    print("\n" + "-"*70 + "\n")
    
    # Display yearly dividend summary
    print("ANNUAL DIVIDEND SUMMARY:")
    print("-"*70)
    annual_summary = calculate_annual_dividend_summary(portfolio)
    for year, amount in annual_summary.items():
        print(f"  {year}: ${amount:,.2f}")
    
    print("\n" + "="*70 + "\n")
    
    # Display current year dividend income
    current_year = date.today().year
    current_year_income = calculate_yearly_dividend_income(portfolio, current_year)
    print(f"DIVIDEND INCOME FOR {current_year}: ${current_year_income:,.2f}")
    
    # Display monthly breakdown for current year
    print(f"\nMonthly Breakdown for {current_year}:")
    print("-"*70)
    monthly_breakdown = calculate_monthly_breakdown(portfolio, current_year)
    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    for month, amount in monthly_breakdown.items():
        if amount > 0:
            print(f"  {month_names[month-1]}: ${amount:,.2f}")
    
    print("\n" + "="*70 + "\n")
    
    # Display upcoming dividends
    print("UPCOMING DIVIDENDS (Next 60 days):")
    print("-"*70)
    upcoming = get_upcoming_dividends(portfolio, days_ahead=60)
    if upcoming:
        for div in upcoming:
            print(f"\n  {div.ticker}:")
            print(f"    Payment Date: {div.payment_date}")
            print(f"    Amount per Share: ${div.amount_per_share:.2f}")
            print(f"    Total Amount: ${div.total_amount:.2f}")
            print(f"    Status: {div.payment_status}")
    else:
        print("  No upcoming dividends in the next 60 days.")
    
    print("\n" + "="*70 + "\n")
    
    # Display dividend history for each stock
    print("DIVIDEND PAYMENT HISTORY BY STOCK:")
    print("-"*70)
    for stock in portfolio.stocks:
        history = get_dividend_history_by_stock(portfolio, stock.ticker)
        if history:
            print(f"\n{stock.ticker}:")
            total_received = Decimal('0')
            for payment_date, amount in history:
                print(f"  {payment_date}: ${amount:.2f}")
                total_received += amount
            print(f"  Total Received: ${total_received:.2f}")
            
            # Calculate dividend growth rate
            growth_rate = get_dividend_growth_rate(portfolio, stock.ticker, years=3)
            if growth_rate:
                print(f"  3-Year Dividend Growth Rate: {growth_rate:.2f}%")
    
    print("\n" + "="*70 + "\n")
    
    # Estimate future dividend income
    print("FUTURE DIVIDEND INCOME PROJECTIONS:")
    print("-"*70)
    for months in [6, 12, 24]:
        estimated = estimate_future_dividend_income(portfolio, months)
        years = months / 12
        print(f"  Next {months} months ({years:.1f} year{'s' if years != 1 else ''}): ${estimated:,.2f}")
    
    print("\n" + "="*70 + "\n")
    
    # Display summary statistics
    print("SUMMARY STATISTICS:")
    print("-"*70)
    total_stocks = len(portfolio.stocks)
    total_dividends_recorded = len([d for d in portfolio.dividends if d.is_paid])
    total_upcoming = len(get_upcoming_dividends(portfolio, days_ahead=365))
    
    print(f"  Total Stocks: {total_stocks}")
    print(f"  Total Historical Dividend Payments: {total_dividends_recorded}")
    print(f"  Upcoming Dividend Payments (Next Year): {total_upcoming}")
    print(f"  Portfolio Value: ${portfolio.total_portfolio_value:,.2f}")
    print(f"  Lifetime Dividend Income: ${lifetime_income:,.2f}")
    print(f"  Portfolio Yield: {portfolio_yield:.2f}%")
    
    # Calculate return on investment from dividends
    total_cost = sum(stock.total_cost for stock in portfolio.stocks)
    if total_cost > 0:
        dividend_roi = (lifetime_income / total_cost) * Decimal('100')
        print(f"  Dividend ROI: {dividend_roi:.2f}%")
    
    print("\n" + "="*70 + "\n")
    print("\nExample usage complete!")
    print("\nTo extend this app, you can:")
    print("  - Add more stocks to your portfolio")
    print("  - Update stock prices regularly")
    print("  - Record new dividend payments")
    print("  - Generate reports and visualizations")
    print("  - Export data to CSV or JSON formats")
    print("  - Add tax tracking features")
    print("  - Implement automatic data fetching from APIs")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
