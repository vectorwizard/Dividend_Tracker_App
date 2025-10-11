# Dividend Tracker App

A comprehensive end-to-end application for tracking dividend income, yield, payment dates, payout history, and future dividend estimates. This project provides a complete framework for dividend investors to monitor and analyze their dividend-paying stock portfolio.

## Features

### Core Functionality
- **Portfolio Management**: Track multiple stocks with purchase prices, current prices, and share quantities
- **Dividend Income Tracking**: Calculate total dividend income (monthly, yearly, lifetime)
- **Dividend Yield Analysis**: Calculate dividend yield for individual stocks and entire portfolio
- **Payment Date Tracking**: Monitor upcoming dividend payments and track payment history
- **Historical Data**: Store and display complete payout history per stock
- **Future Income Estimation**: Project future dividend income based on current holdings and schedules
- **Dividend Growth Analysis**: Calculate dividend growth rates over time

## Project Structure

```
Dividend_Tracker_App/
├── models.py           # Data models for stocks, dividends, and portfolios
├── calculator.py       # Calculation functions for dividend analytics
├── sample_data.py      # Sample dataset for demonstration
├── example_usage.py    # Comprehensive usage examples
└── README.md          # This file
```

## Data Models

### Stock
Represents a stock in the portfolio with the following attributes:
- `ticker`: Stock ticker symbol (e.g., 'AAPL')
- `name`: Company name
- `shares`: Number of shares owned
- `purchase_price`: Average purchase price per share
- `current_price`: Current market price per share
- `currency`: Currency for prices (default: USD)

**Calculated Properties:**
- `total_value`: Total value of holdings (shares × current_price)
- `total_cost`: Total cost basis (shares × purchase_price)
- `unrealized_gain`: Unrealized gain/loss

### Dividend
Represents a dividend payment with:
- `ticker`: Stock ticker symbol
- `payment_date`: Date dividend was/will be paid
- `amount_per_share`: Dividend amount per share
- `shares_owned`: Number of shares owned at ex-dividend date
- `payment_status`: 'paid', 'pending', or 'announced'

**Calculated Properties:**
- `total_amount`: Total dividend payment
- `is_upcoming`: Whether dividend is upcoming
- `is_paid`: Whether dividend has been paid

### DividendSchedule
Represents the dividend schedule for a stock:
- `ticker`: Stock ticker symbol
- `frequency`: 'quarterly', 'monthly', 'annual', or 'semi-annual'
- `typical_amount`: Typical dividend amount per share
- `last_ex_dividend_date`: Last ex-dividend date
- `next_payment_date`: Next expected payment date

### Portfolio
Container for stocks and dividend history:
- `name`: Portfolio name
- `stocks`: List of Stock objects
- `dividends`: List of Dividend objects
- `schedules`: Dictionary of DividendSchedule objects

## Calculator Functions

The `calculator.py` module provides comprehensive functions for dividend analysis:

### Income Calculations
- `calculate_total_dividend_income(portfolio, start_date, end_date)`: Calculate dividend income for any period
- `calculate_monthly_dividend_income(portfolio, year, month)`: Calculate income for a specific month
- `calculate_yearly_dividend_income(portfolio, year)`: Calculate income for a specific year
- `calculate_lifetime_dividend_income(portfolio)`: Calculate total income since inception

### Yield Calculations
- `calculate_dividend_yield(stock, annual_dividend_per_share)`: Calculate yield for a stock
- `calculate_portfolio_dividend_yield(portfolio)`: Calculate weighted average yield for portfolio

### Tracking & Analysis
- `get_upcoming_dividends(portfolio, days_ahead)`: Get list of upcoming dividend payments
- `get_dividend_history_by_stock(portfolio, ticker)`: Get complete payment history for a stock
- `calculate_annual_dividend_summary(portfolio)`: Get dividend income summary by year
- `calculate_monthly_breakdown(portfolio, year)`: Get monthly breakdown for a year

### Projections
- `estimate_future_dividend_income(portfolio, months_ahead)`: Estimate future income
- `get_dividend_growth_rate(portfolio, ticker, years)`: Calculate dividend growth rate

## Installation & Setup

### Requirements
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/vectorwizard/Dividend_Tracker_App.git
cd Dividend_Tracker_App
```

2. Run the example:
```bash
python example_usage.py
```

## Usage Examples

### Basic Usage

```python
from models import Stock, Dividend, DividendSchedule, Portfolio
from calculator import calculate_dividend_yield, calculate_lifetime_dividend_income
from datetime import date
from decimal import Decimal

# Create a portfolio
portfolio = Portfolio(name="My Dividend Portfolio")

# Add a stock
aapl = Stock(
    ticker="AAPL",
    name="Apple Inc.",
    shares=Decimal('100'),
    purchase_price=Decimal('150.00'),
    current_price=Decimal('175.00')
)
portfolio.add_stock(aapl)

# Add dividend schedule
aapl_schedule = DividendSchedule(
    ticker="AAPL",
    frequency="quarterly",
    typical_amount=Decimal('0.24'),
    next_payment_date=date(2025, 11, 14)
)
portfolio.add_schedule(aapl_schedule)

# Record a dividend payment
dividend = Dividend(
    ticker="AAPL",
    payment_date=date(2025, 8, 14),
    amount_per_share=Decimal('0.24'),
    shares_owned=Decimal('100'),
    payment_status="paid"
)
portfolio.add_dividend(dividend)

# Calculate dividend yield
annual_dividend = aapl_schedule.typical_amount * Decimal('4')  # Quarterly * 4
yield_pct = calculate_dividend_yield(aapl, annual_dividend)
print(f"Dividend Yield: {yield_pct:.2f}%")

# Calculate lifetime income
lifetime_income = calculate_lifetime_dividend_income(portfolio)
print(f"Lifetime Dividend Income: ${lifetime_income:.2f}")
```

### Advanced Features

```python
from calculator import (
    get_upcoming_dividends,
    estimate_future_dividend_income,
    calculate_portfolio_dividend_yield,
    get_dividend_growth_rate
)

# Get upcoming dividends in next 30 days
upcoming = get_upcoming_dividends(portfolio, days_ahead=30)
for div in upcoming:
    print(f"{div.ticker}: ${div.total_amount:.2f} on {div.payment_date}")

# Estimate income for next 12 months
future_income = estimate_future_dividend_income(portfolio, months_ahead=12)
print(f"Estimated 12-month income: ${future_income:.2f}")

# Calculate portfolio yield
portfolio_yield = calculate_portfolio_dividend_yield(portfolio)
print(f"Portfolio Yield: {portfolio_yield:.2f}%")

# Calculate dividend growth rate
growth_rate = get_dividend_growth_rate(portfolio, "AAPL", years=3)
if growth_rate:
    print(f"3-Year Dividend Growth: {growth_rate:.2f}%")
```

## Sample Dataset

The `sample_data.py` file provides a complete example portfolio with:

- **4 Stocks**: AAPL, MSFT, KO, JNJ
- **Historical Dividends**: Past year of dividend payments for all stocks
- **Upcoming Dividends**: Pending dividend payments
- **Dividend Schedules**: Payment frequency and amounts for each stock

Run the sample data:
```bash
python sample_data.py
```

## Comprehensive Example

The `example_usage.py` file demonstrates all features:

- Portfolio overview with stock details
- Dividend yield calculations
- Income tracking (lifetime, yearly, monthly)
- Upcoming dividend payments
- Historical dividend tracking
- Future income projections
- Summary statistics and ROI

Run the comprehensive example:
```bash
python example_usage.py
```

Expected output includes:
- Stock holdings with values and gains/losses
- Portfolio-level dividend yield
- Historical dividend income by year and month
- Upcoming payment schedule
- Complete payment history per stock
- Future income estimates (6, 12, 24 months)
- Summary statistics including dividend ROI

## Extension Ideas

This project is designed for easy extension. Consider adding:

### Data Management
- JSON/CSV import/export functionality
- Database integration (SQLite, PostgreSQL)
- Data persistence layer

### Data Sources
- API integration for automatic stock price updates
- Automatic dividend data fetching
- Real-time market data integration

### Reporting & Visualization
- PDF report generation
- Charts and graphs (using matplotlib, plotly)
- Email notifications for upcoming dividends
- Web dashboard (Flask, Django, Streamlit)

### Advanced Features
- Tax tracking and reporting
- Currency conversion for international stocks
- DRIP (Dividend Reinvestment Plan) tracking
- Performance benchmarking
- Multi-portfolio support
- Portfolio optimization suggestions

### User Interface
- Command-line interface (CLI)
- Web interface
- Mobile app
- Desktop GUI (tkinter, PyQt)

## Data Accuracy Note

This is a tracking and calculation framework. Users are responsible for:
- Entering accurate stock purchase prices
- Recording actual dividend payments received
- Updating current stock prices
- Maintaining correct dividend schedules

For real-time data, consider integrating with financial APIs such as:
- Alpha Vantage
- Yahoo Finance (yfinance)
- IEX Cloud
- Polygon.io

## Contributing

Contributions are welcome! Areas for improvement:
- Additional calculator functions
- More comprehensive data validation
- Unit tests
- Documentation enhancements
- Example scripts for specific use cases

## License

This project is open source and available under the MIT License.

## Author

vectorwizard

## Version History

- **v1.0.0** (2025-10-11): Initial release
  - Core data models
  - Comprehensive calculator functions
  - Sample data and usage examples
  - Complete documentation

## Support

For questions, issues, or suggestions, please open an issue on the GitHub repository.

---

**Happy Dividend Tracking!** 📈💰
