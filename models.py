"""Data models for Dividend Tracker App

This module defines the core data structures for tracking stocks and dividends.
"""

from datetime import datetime, date
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Stock:
    """Represents a stock in the portfolio."""
    ticker: str  # Stock ticker symbol (e.g., 'AAPL')
    name: str  # Company name
    shares: Decimal  # Number of shares owned
    purchase_price: Decimal  # Average purchase price per share
    current_price: Decimal  # Current market price per share
    currency: str = "USD"  # Currency for prices
    
    @property
    def total_value(self) -> Decimal:
        """Calculate total value of holdings."""
        return self.shares * self.current_price
    
    @property
    def total_cost(self) -> Decimal:
        """Calculate total cost basis."""
        return self.shares * self.purchase_price
    
    @property
    def unrealized_gain(self) -> Decimal:
        """Calculate unrealized gain/loss."""
        return self.total_value - self.total_cost


@dataclass
class Dividend:
    """Represents a dividend payment."""
    ticker: str  # Stock ticker symbol
    payment_date: date  # Date dividend was/will be paid
    amount_per_share: Decimal  # Dividend amount per share
    shares_owned: Decimal  # Number of shares owned at ex-dividend date
    payment_status: str = "pending"  # 'paid', 'pending', 'announced'
    
    @property
    def total_amount(self) -> Decimal:
        """Calculate total dividend payment."""
        return self.amount_per_share * self.shares_owned
    
    @property
    def is_upcoming(self) -> bool:
        """Check if dividend is upcoming."""
        return self.payment_date > date.today() and self.payment_status != "paid"
    
    @property
    def is_paid(self) -> bool:
        """Check if dividend has been paid."""
        return self.payment_status == "paid" or self.payment_date < date.today()


@dataclass
class DividendSchedule:
    """Represents the dividend schedule for a stock."""
    ticker: str  # Stock ticker symbol
    frequency: str  # 'quarterly', 'monthly', 'annual', 'semi-annual'
    typical_amount: Decimal  # Typical dividend amount per share
    last_ex_dividend_date: Optional[date] = None  # Last ex-dividend date
    next_payment_date: Optional[date] = None  # Next expected payment date
    
    def get_annual_frequency(self) -> int:
        """Get number of payments per year."""
        frequency_map = {
            'monthly': 12,
            'quarterly': 4,
            'semi-annual': 2,
            'annual': 1
        }
        return frequency_map.get(self.frequency.lower(), 4)


@dataclass
class Portfolio:
    """Represents a portfolio of stocks and dividend history."""
    name: str  # Portfolio name
    stocks: List[Stock] = field(default_factory=list)
    dividends: List[Dividend] = field(default_factory=list)
    schedules: Dict[str, DividendSchedule] = field(default_factory=dict)
    
    def add_stock(self, stock: Stock) -> None:
        """Add a stock to the portfolio."""
        self.stocks.append(stock)
    
    def add_dividend(self, dividend: Dividend) -> None:
        """Add a dividend to the history."""
        self.dividends.append(dividend)
    
    def add_schedule(self, schedule: DividendSchedule) -> None:
        """Add a dividend schedule."""
        self.schedules[schedule.ticker] = schedule
    
    def get_stock(self, ticker: str) -> Optional[Stock]:
        """Get a stock by ticker symbol."""
        for stock in self.stocks:
            if stock.ticker == ticker:
                return stock
        return None
    
    def get_dividends_for_stock(self, ticker: str) -> List[Dividend]:
        """Get all dividends for a specific stock."""
        return [d for d in self.dividends if d.ticker == ticker]
    
    @property
    def total_portfolio_value(self) -> Decimal:
        """Calculate total portfolio value."""
        return sum(stock.total_value for stock in self.stocks)
