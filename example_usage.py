"""Example usage of the Dividend Tracker App
This script demonstrates how to use all the features of the dividend tracking system
for tracking Indian stock market dividends in INR.
"""
from datetime import date
from decimal import Decimal
from sample_data import create_sample_portfolio
from calculator import (
    calculate_total_dividend_income,
    calculate_annual_dividend_income,
    calculate_dividend_yield,
    calculate_portfolio_dividend_yield,
    project_dividend_income,
    calculate_dividend_growth_rate,
    generate_dividend_summary,
    format_inr
)

def print_separator():
    """Print a visual separator."""
    print("\n" + "="*70)

def main():
    """Main function demonstrating all dividend tracking features for Indian stocks."""
    
    # Create sample portfolio with Indian stocks
    print_separator()
    print("DIVIDEND TRACKER APP - INDIAN STOCK MARKET EDITION")
    print("Currency: Indian Rupees (INR)")
    print_separator()
    
    portfolio = create_sample_portfolio()
    
    print(f"\nPortfolio: {portfolio.name}")
    print(f"Number of stocks: {len(portfolio.stocks)}")
    print(f"Total Portfolio Value: {format_inr(portfolio.total_portfolio_value)}")
    
    # Display individual stock holdings
    print_separator()
    print("STOCK HOLDINGS")
    print_separator()
    
    for stock in portfolio.stocks:
        print(f"\n{stock.name} ({stock.ticker}):")
        print(f"  Shares Owned: {stock.shares}")
        print(f"  Purchase Price: {format_inr(stock.purchase_price)} per share")
        print(f"  Current Price: {format_inr(stock.current_price)} per share")
        print(f"  Total Value: {format_inr(stock.total_value)}")
        print(f"  Unrealized Gain/Loss: {format_inr(stock.unrealized_gain)} ({stock.unrealized_gain_percentage:.2f}%)")
    
    # Calculate and display dividend income
    print_separator()
    print("DIVIDEND INCOME ANALYSIS")
    print_separator()
    
    # Year-to-date dividend income
    year_start = date(date.today().year, 1, 1)
    ytd_income = calculate_total_dividend_income(portfolio, year_start)
    print(f"\nYear-to-Date Dividend Income: {format_inr(ytd_income)}")
    
    # Last 12 months dividend income
    last_year = date.today().replace(year=date.today().year - 1)
    last_12_months = calculate_total_dividend_income(portfolio, last_year)
    print(f"Last 12 Months Dividend Income: {format_inr(last_12_months)}")
    
    # Expected annual dividend income
    annual_income = calculate_annual_dividend_income(portfolio)
    print(f"Expected Annual Dividend Income: {format_inr(annual_income)}")
    
    # Portfolio dividend yield
    portfolio_yield = calculate_portfolio_dividend_yield(portfolio)
    print(f"Portfolio Dividend Yield: {portfolio_yield:.2f}%")
    
    # Display dividend yield by stock
    print_separator()
    print("DIVIDEND YIELD BY STOCK")
    print_separator()
    
    for ticker, schedule in portfolio.schedules.items():
        stock = portfolio.get_stock(ticker)
        if stock:
            annual_dividend_per_share = (schedule.typical_amount * 
                                        Decimal(str(schedule.get_annual_frequency())))
            stock_yield = calculate_dividend_yield(stock, annual_dividend_per_share)
            annual_income_stock = annual_dividend_per_share * stock.shares
            
            print(f"\n{stock.name} ({ticker}):")
            print(f"  Dividend Frequency: {schedule.frequency.capitalize()}")
            print(f"  Typical Payment: {format_inr(schedule.typical_amount)} per share")
            print(f"  Annual Dividend (per share): {format_inr(annual_dividend_per_share)}")
            print(f"  Annual Dividend Income: {format_inr(annual_income_stock)}")
            print(f"  Dividend Yield: {stock_yield:.2f}%")
            if schedule.next_payment_date:
                print(f"  Next Payment Date: {schedule.next_payment_date.strftime('%d %B %Y')}")
    
    # Display dividend history
    print_separator()
    print("RECENT DIVIDEND HISTORY")
    print_separator()
    
    recent_dividends = sorted(portfolio.dividends, key=lambda d: d.payment_date, reverse=True)[:10]
    for dividend in recent_dividends:
        stock = portfolio.get_stock(dividend.ticker)
        stock_name = stock.name if stock else dividend.ticker
        print(f"\n{dividend.payment_date.strftime('%d %b %Y')} - {stock_name} ({dividend.ticker}):")
        print(f"  Amount per share: {format_inr(dividend.amount_per_share)}")
        print(f"  Shares: {dividend.shares}")
        print(f"  Total payment: {format_inr(dividend.total_amount)}")
    
    # Project future dividend income
    print_separator()
    print("DIVIDEND INCOME PROJECTION (Next 12 Months)")
    print_separator()
    
    projections = project_dividend_income(portfolio, months=12, growth_rate=Decimal('5'))
    quarterly_totals = {}
    
    for proj_date, proj_income in projections:
        quarter = (proj_date.month - 1) // 3 + 1
        year = proj_date.year
        key = f"Q{quarter} {year}"
        quarterly_totals[key] = quarterly_totals.get(key, Decimal('0')) + proj_income
    
    print("\nProjected Quarterly Dividend Income (assuming 5% annual growth):")
    for quarter, total in quarterly_totals.items():
        print(f"  {quarter}: {format_inr(total)}")
    
    total_projected = sum(proj_income for _, proj_income in projections)
    print(f"\nTotal Projected (12 months): {format_inr(total_projected)}")
    
    # Generate comprehensive summary
    print_separator()
    print("COMPREHENSIVE DIVIDEND SUMMARY")
    print_separator()
    
    summary = generate_dividend_summary(portfolio)
    
    print(f"\nTotal Portfolio Value: {summary['total_portfolio_value_formatted']}")
    print(f"Expected Annual Dividend Income: {summary['annual_dividend_income_formatted']}")
    print(f"Year-to-Date Dividend Income: {summary['ytd_dividend_income_formatted']}")
    print(f"Portfolio Dividend Yield: {summary['portfolio_yield']:.2f}%")
    print(f"Number of Stocks: {summary['number_of_stocks']}")
    print(f"Total Dividends Received: {summary['total_dividends_received']}")
    print(f"Currency: {summary['currency']}")
    
    # Calculate dividend growth rates
    print_separator()
    print("DIVIDEND GROWTH ANALYSIS")
    print_separator()
    
    for ticker in portfolio.schedules.keys():
        stock = portfolio.get_stock(ticker)
        if stock:
            growth_rate = calculate_dividend_growth_rate(portfolio, ticker)
            if growth_rate is not None:
                print(f"\n{stock.name} ({ticker}):")
                print(f"  Average Dividend Growth Rate: {growth_rate:.2f}%")
            else:
                print(f"\n{stock.name} ({ticker}):")
                print(f"  Insufficient data for growth rate calculation")
    
    print_separator()
    print("\nExample usage completed successfully!")
    print("All calculations are in Indian Rupees (INR)")
    print_separator()

if __name__ == "__main__":
    main()
