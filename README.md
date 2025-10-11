# Dividend Tracker App - Indian Stock Market Edition

A command-line Python application to track dividend income, yield, payment dates, payout history, and future dividend estimates for Indian stocks (NSE/BSE) in INR (₹).

## Features

- Track multiple stock holdings with purchase price and quantity
- Record dividend payments with dates and amounts
- Calculate portfolio metrics:
  - Total invested amount
  - Annual dividend income
  - Monthly average dividend income
  - Yield on cost per holding
- Track upcoming and past dividend payments
- Project future dividend income based on historical data
- Export portfolio data to CSV

## Installation

1. Ensure you have Python 3.8+ installed
2. Clone this repository:
   ```bash
   git clone https://github.com/vectorwizard/Dividend_Tracker_App.git
   cd Dividend_Tracker_App
   ```

## Usage

The application provides a command-line interface through `example_usage.py`. You can also use the core modules to build your own tools:

### Quick Start

```bash
python example_usage.py
```

### Core Modules

- **models.py**: Defines the `Stock` and `Dividend` data models
- **calculator.py**: Contains calculation logic for portfolio analytics
- **sample_data.py**: Provides sample data for testing
- **example_usage.py**: Demonstrates how to use the modules

## Data Format

### Stock Holdings

Each stock holding contains:
- `symbol`: Stock ticker symbol (e.g., "RELIANCE", "TCS")
- `name`: Full company name
- `qty`: Number of shares owned
- `avg_price`: Average purchase price per share (INR)
- `fy_div`: Annual dividend per share (INR)
- `freq`: Dividend payment frequency per year
- `last_div`: Last dividend payment date (YYYY-MM-DD)
- `next_div`: Next expected dividend date (YYYY-MM-DD)

### Dividend Events

Each dividend event contains:
- `symbol`: Stock ticker symbol
- `ex_date`: Ex-dividend date
- `pay_date`: Payment date
- `amount`: Dividend amount per share (INR)

## Example

```python
from models import Stock, Dividend
from calculator import Calculator

# Create stock holdings
stocks = [
    Stock(
        symbol="RELIANCE",
        name="Reliance Industries",
        qty=10,
        avg_price=2550.00,
        fy_div=40.0,
        freq=1,
        last_div="2025-05-01",
        next_div="2026-05-01"
    ),
    Stock(
        symbol="TCS",
        name="Tata Consultancy Services",
        qty=5,
        avg_price=3900.00,
        fy_div=90.0,
        freq=2,
        last_div="2025-06-10",
        next_div="2025-12-10"
    )
]

# Create calculator instance
calc = Calculator(stocks)

# Calculate metrics
total_invested = calc.total_invested()
annual_income = calc.annual_dividend_income()
monthly_income = calc.monthly_dividend_income()

print(f"Total Invested: ₹{total_invested:,.2f}")
print(f"Annual Dividend Income: ₹{annual_income:,.2f}")
print(f"Monthly Average: ₹{monthly_income:,.2f}")
```

## Portfolio CSV Format

You can save and load portfolios using CSV format:

```csv
symbol,name,qty,avg_price,fy_div,freq,last_div,next_div
RELIANCE,Reliance Industries,10,2550.00,40.0,1,2025-05-01,2026-05-01
TCS,Tata Consultancy Services,5,3900.00,90.0,2,2025-06-10,2025-12-10
HDFC,HDFC Bank,20,1600.00,16.5,1,2025-04-15,2026-04-15
```

## Currency

All monetary values are in Indian Rupees (₹/INR).

## License

This project is open source and available for personal use.
