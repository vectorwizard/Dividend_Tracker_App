# Dividend Tracker App - Indian Stock Market Edition

A comprehensive end-to-end application for tracking dividend income, yield, payment dates, payout history, and future dividend estimates for the **Indian Stock Market (NSE/BSE)**. This project provides a complete framework for dividend investors to monitor and analyze their dividend-paying stock portfolio in **Indian Rupees (INR)**.

## Features

### Core Functionality

- **Portfolio Management**: Track multiple Indian stocks with purchase prices, current prices, and share quantities
- **Dividend Income Tracking**: Calculate total dividend income (monthly, yearly, lifetime) in INR
- **Dividend Yield Analysis**: Calculate dividend yield for individual stocks and entire portfolio
- **Payment Date Tracking**: Monitor upcoming dividend payments and track payment history
- **Historical Data**: Store and display complete payout history per stock
- **Future Income Estimation**: Project future dividend income based on current holdings and schedules
- **Dividend Growth Analysis**: Calculate dividend growth rates over time
- **INR Currency Formatting**: Proper formatting with ₹ symbol and Indian numbering conventions

## Project Structure

```
Dividend_Tracker_App/
├── models.py           # Data models for stocks, dividends, and portfolios
├── calculator.py       # Calculation functions for dividend analytics (with INR support)
├── sample_data.py      # Sample dataset with Indian stocks (RELIANCE, TCS, HDFCBANK, INFY)
├── example_usage.py    # Comprehensive usage examples for Indian market
└── README.md          # This file
```

## Data Models

### Stock

Represents a stock in the portfolio with the following attributes:

- `ticker`: Stock ticker symbol (e.g., 'RELIANCE', 'TCS', 'HDFCBANK', 'INFY')
- `name`: Company name (e.g., 'Reliance Industries Limited')
- `shares`: Number of shares owned
- `purchase_price`: Average purchase price per share (in INR)
- `current_price`: Current market price per share (in INR)
- `currency`: Currency for prices (default: INR)

**Calculated Properties:**

- `total_value`: Total value of holdings (shares × current_price) in INR
- `total_cost`: Total cost basis (shares × purchase_price) in INR
- `unrealized_gain`: Unrealized gain/loss in INR
- `unrealized_gain_percentage`: Unrealized gain/loss as percentage

### Dividend

Represents a dividend payment:

- `ticker`: Stock ticker symbol
- `payment_date`: Date dividend was/will be paid
- `amount_per_share`: Dividend amount per share in INR
- `shares`: Number of shares owned at payment

**Calculated Properties:**

- `total_amount`: Total dividend payment (amount_per_share × shares) in INR

### DividendSchedule

Represents expected dividend schedule for a stock:

- `ticker`: Stock ticker symbol
- `frequency`: Payment frequency ('monthly', 'quarterly', 'semi-annual', 'annual')
- `typical_amount`: Typical dividend amount per share in INR
- `last_ex_dividend_date`: Last ex-dividend date
- `next_payment_date`: Next expected payment date

### Portfolio

Container for stocks, dividends, and schedules:

- `name`: Portfolio name
- `stocks`: List of Stock objects
- `dividends`: List of Dividend objects
- `schedules`: Dictionary of DividendSchedule objects

## Calculator Functions

### Currency Formatting

```python
format_inr(amount: Decimal) -> str
```
Format amount in Indian Rupees with ₹ symbol and proper comma separators.

**Example:**
```python
format_inr(Decimal('125000.50'))  # Returns: "₹125,000.50"
```

### Income Calculations

```python
calculate_total_dividend_income(
    portfolio: Portfolio,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Decimal
```
Calculate total dividend income for a given period (in INR).

```python
calculate_annual_dividend_income(portfolio: Portfolio) -> Decimal
```
Calculate expected annual dividend income based on schedules (in INR).

### Yield Calculations

```python
calculate_dividend_yield(
    stock: Stock,
    annual_dividend_per_share: Decimal
) -> Decimal
```
Calculate dividend yield for a stock as percentage.

```python
calculate_portfolio_dividend_yield(portfolio: Portfolio) -> Decimal
```
Calculate weighted average dividend yield for entire portfolio.

### Projections

```python
project_dividend_income(
    portfolio: Portfolio,
    months: int,
    growth_rate: Decimal = Decimal('0')
) -> List[Tuple[date, Decimal]]
```
Project future dividend income month by month with optional growth rate.

### Analysis

```python
calculate_dividend_growth_rate(
    portfolio: Portfolio,
    ticker: str,
    years: int = 3
) -> Optional[Decimal]
```
Calculate historical dividend growth rate for a stock.

```python
generate_dividend_summary(portfolio: Portfolio) -> Dict[str, any]
```
Generate comprehensive dividend summary with all metrics (all amounts in INR).

## Sample Data

The `sample_data.py` module provides pre-configured portfolios with Indian stocks:

### create_sample_portfolio()

Creates a sample portfolio containing:

1. **Reliance Industries (RELIANCE)**
   - 50 shares
   - Purchase price: ₹2,400.00
   - Current price: ₹2,650.00
   - Semi-annual dividends: ₹8.00 per share

2. **Tata Consultancy Services (TCS)**
   - 30 shares
   - Purchase price: ₹3,200.00
   - Current price: ₹3,750.00
   - Quarterly dividends: ₹27.00 per share

3. **HDFC Bank (HDFCBANK)**
   - 40 shares
   - Purchase price: ₹1,550.00
   - Current price: ₹1,680.00
   - Quarterly dividends: ₹19.50 per share

4. **Infosys (INFY)**
   - 60 shares
   - Purchase price: ₹1,420.00
   - Current price: ₹1,580.00
   - Quarterly dividends: ₹20.00 per share

### create_minimal_portfolio()

Creates a minimal portfolio with a single stock (TCS) for basic testing.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vectorwizard/Dividend_Tracker_App.git
cd Dividend_Tracker_App
```

2. Ensure you have Python 3.7+ installed with the required standard libraries:
   - `datetime`
   - `decimal`
   - `dataclasses`
   - `typing`
   - `calendar`

No external dependencies are required.

## Usage

### Basic Example

```python
from sample_data import create_sample_portfolio
from calculator import (
    calculate_annual_dividend_income,
    calculate_portfolio_dividend_yield,
    format_inr
)

# Create a sample portfolio with Indian stocks
portfolio = create_sample_portfolio()

# Calculate annual dividend income
annual_income = calculate_annual_dividend_income(portfolio)
print(f"Expected Annual Income: {format_inr(annual_income)}")

# Calculate portfolio yield
portfolio_yield = calculate_portfolio_dividend_yield(portfolio)
print(f"Portfolio Yield: {portfolio_yield:.2f}%")

# Get total portfolio value
total_value = portfolio.total_portfolio_value
print(f"Total Portfolio Value: {format_inr(total_value)}")
```

### Running the Example Script

```bash
python example_usage.py
```

This will demonstrate all features including:
- Portfolio overview with stock holdings
- Dividend income analysis (YTD, annual, historical)
- Dividend yield by stock
- Recent dividend history
- Future income projections
- Comprehensive summary
- Dividend growth analysis

### Creating Your Own Portfolio

```python
from decimal import Decimal
from datetime import date
from models import Stock, Dividend, DividendSchedule, Portfolio

# Create a new portfolio
my_portfolio = Portfolio(name="My Indian Dividend Portfolio")

# Add a stock (example: ITC)
itc = Stock(
    ticker="ITC",
    name="ITC Limited",
    shares=Decimal('100'),
    purchase_price=Decimal('420.00'),
    current_price=Decimal('445.00'),
    currency="INR"
)
my_portfolio.add_stock(itc)

# Add dividend schedule
itc_schedule = DividendSchedule(
    ticker="ITC",
    frequency="quarterly",
    typical_amount=Decimal('6.25'),  # ₹6.25 per share per quarter
    last_ex_dividend_date=date(2024, 9, 20),
    next_payment_date=date(2025, 1, 5)
)
my_portfolio.add_schedule(itc_schedule)

# Add historical dividend
my_portfolio.add_dividend(Dividend(
    ticker="ITC",
    payment_date=date(2024, 10, 5),
    amount_per_share=Decimal('6.25'),
    shares=Decimal('100')
))
```

## Key Features for Indian Market

1. **INR Currency Support**: All calculations and formatting use Indian Rupees
2. **Indian Stock Tickers**: Pre-configured examples use NSE stock symbols (RELIANCE, TCS, HDFCBANK, INFY)
3. **Realistic Dividend Data**: Sample data uses realistic dividend amounts and frequencies for Indian companies
4. **Local Date Formatting**: Dates formatted for Indian context
5. **Comprehensive Analytics**: Full suite of dividend tracking and analysis tools

## Output Examples

When running `example_usage.py`, you'll see output like:

```
======================================================================
DIVIDEND TRACKER APP - INDIAN STOCK MARKET EDITION
Currency: Indian Rupees (INR)
======================================================================

Portfolio: Sample Indian Dividend Portfolio
Total Portfolio Value: ₹2,95,500.00

======================================================================
STOCK HOLDINGS
======================================================================

Reliance Industries Limited (RELIANCE):
  Shares Owned: 50
  Current Price: ₹2,650.00 per share
  Total Value: ₹1,32,500.00
  Dividend Yield: 0.60%

Tata Consultancy Services Limited (TCS):
  Shares Owned: 30
  Current Price: ₹3,750.00 per share
  Total Value: ₹1,12,500.00
  Dividend Yield: 2.88%

...

Expected Annual Dividend Income: ₹10,840.00
Portfolio Dividend Yield: 3.67%
```

## License

This project is open source and available for personal and educational use.

## Contributing

Contributions are welcome! Feel free to:
- Add more Indian stocks to the sample data
- Improve calculation functions
- Add new analytics features
- Enhance documentation

## Author

vectorwizard

## Currency Note

All amounts throughout this application are in **Indian Rupees (INR)** unless otherwise specified. The ₹ symbol is used consistently for currency formatting.
