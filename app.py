from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timedelta
import os

# Import existing modules
from models import Stock, Portfolio, Dividend, DividendSchedule
from calculator import calculate_annual_dividend_income, project_dividend_income, generate_dividend_summary, format_inr, calculate_portfolio_dividend_yield
from sample_data import create_sample_portfolio

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize portfolio with sample data
portfolio = create_sample_portfolio()

@app.route('/')
def index():
    """Main dashboard showing overview of portfolio and dividends"""
    
    # Calculate key metrics
    total_value = portfolio.total_portfolio_value
    total_annual_dividends = calculate_annual_dividend_income(portfolio)
    portfolio_yield = (total_annual_dividends / total_value * 100) if total_value > 0 else 0
    
    # Get recent dividend payments (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_dividends = []
    
    for stock in portfolio.stocks:
        for div in stock.dividend_history:
            if div.payment_date >= thirty_days_ago:
                recent_dividends.append({
                    'symbol': stock.symbol,
                    'date': div.payment_date,
                    'amount': div.amount * stock.shares
                })
    
    # Sort by date descending
    recent_dividends.sort(key=lambda x: x['date'], reverse=True)
    
    # Get upcoming dividends (next 90 days)
    ninety_days_ahead = datetime.now() + timedelta(days=90)
    upcoming = []
    
    for stock in portfolio.stocks:
        if stock.dividend_schedule:
            next_date = stock.dividend_schedule.get_next_ex_dividend_date()
            if next_date and next_date <= ninety_days_ahead:
                upcoming.append({
                    'symbol': stock.symbol,
                    'ex_date': next_date,
                    'estimated_amount': stock.dividend_schedule.amount * stock.shares
                })
    
    upcoming.sort(key=lambda x: x['ex_date'])
    
    return render_template('index.html',
                         total_value=total_value,
                         total_annual_dividends=total_annual_dividends,
                         portfolio_yield=portfolio_yield,
                         stocks_count=len(portfolio.stocks),
                         recent_dividends=recent_dividends[:5],
                         upcoming_dividends=upcoming[:5])

@app.route('/portfolio')
def show_portfolio():
    """Display portfolio holdings"""
    stocks_data = []
    
    for stock in portfolio.stocks:
        annual_dividend = calculate_annual_dividend_income(Portfolio([stock]))
        stock_value = stock.shares * stock.price
        stock_yield = (annual_dividend / stock_value * 100) if stock_value > 0 else 0
        
        stocks_data.append({
            'symbol': stock.symbol,
            'name': stock.name,
            'shares': stock.shares,
            'price': stock.price,
            'value': stock_value,
            'annual_dividend': annual_dividend,
            'yield': stock_yield
        })
    
    return render_template('portfolio.html',
                         stocks=stocks_data,
                         total_value=portfolio.total_portfolio_value)

@app.route('/dividends')
def show_dividends():
    """Display dividend analysis and projections"""
    
    # Calculate projections using project_dividend_income
    monthly_projection = project_dividend_income(portfolio, months=1, growth_rate=0.0)
    quarterly_projection = project_dividend_income(portfolio, months=3, growth_rate=0.0)
    annual_projection = calculate_annual_dividend_income(portfolio)
    
    # Generate summary statistics
    total_annual_dividends = calculate_annual_dividend_income(portfolio)
    average_yield = calculate_portfolio_dividend_yield(portfolio)
    monthly_average = total_annual_dividends / 12
    total_stocks = len(portfolio.stocks)
    
    # Calculate monthly projections (array of 12 months)
    monthly_projections = []
    for month in range(1, 13):
        month_name = datetime(2024, month, 1).strftime('%B')
        month_amount = project_dividend_income(portfolio, months=1, growth_rate=0.0)
        monthly_projections.append({'month': month_name, 'amount': month_amount})
    
    # Calculate quarterly projections (array of 4 quarters)
    quarterly_projections = []
    for quarter in range(1, 5):
        quarter_name = f'Q{quarter}'
        quarter_amount = project_dividend_income(portfolio, months=3, growth_rate=0.0)
        quarterly_projections.append({'quarter': quarter_name, 'amount': quarter_amount})
    
    # Get upcoming dividends
    upcoming_dividends = []
    ninety_days_ahead = datetime.now() + timedelta(days=90)
    
    for stock in portfolio.stocks:
        if stock.dividend_schedule:
            next_date = stock.dividend_schedule.get_next_ex_dividend_date()
            if next_date and next_date <= ninety_days_ahead:
                upcoming_dividends.append({
                    'symbol': stock.symbol,
                    'ex_date': next_date,
                    'estimated_amount': stock.dividend_schedule.amount * stock.shares
                })
    
    upcoming_dividends.sort(key=lambda x: x['ex_date'])
    
    return render_template('dividends.html',
                         total_annual_dividends=total_annual_dividends,
                         average_yield=average_yield,
                         monthly_average=monthly_average,
                         total_stocks=total_stocks,
                         monthly_projections=monthly_projections,
                         quarterly_projections=quarterly_projections,
                         annual_projection=annual_projection,
                         upcoming_dividends=upcoming_dividends)

@app.route('/add-stock', methods=['GET', 'POST'])
def add_stock():
    """Add a new stock to portfolio"""
    if request.method == 'POST':
        try:
            # Get form data
            symbol = request.form.get('symbol', '').upper()
            name = request.form.get('name', '')
            shares = int(request.form.get('shares', 0))
            price = float(request.form.get('price', 0.0))
            
            # Create new stock
            new_stock = Stock(
                symbol=symbol,
                name=name,
                shares=shares,
                price=price
            )
            
            # Add dividend schedule if provided
            if request.form.get('dividend_amount'):
                amount = float(request.form.get('dividend_amount', 0.0))
                frequency = request.form.get('frequency', 'quarterly')
                next_date_str = request.form.get('next_date')
                
                if next_date_str:
                    next_date = datetime.strptime(next_date_str, '%Y-%m-%d')
                    schedule = DividendSchedule(
                        amount=amount,
                        frequency=frequency,
                        next_ex_dividend_date=next_date
                    )
                    new_stock.dividend_schedule = schedule
            
            # Add to portfolio
            portfolio.add_stock(new_stock)
            flash(f'Successfully added {symbol} to portfolio!', 'success')
            return redirect(url_for('show_portfolio'))
            
        except ValueError as e:
            flash(f'Error adding stock: {str(e)}', 'error')
            return redirect(url_for('add_stock'))
    
    return render_template('add_stock.html')

@app.route('/edit-stock/<symbol>', methods=['GET', 'POST'])
def edit_stock(symbol):
    """Edit an existing stock"""
    stock = None
    for s in portfolio.stocks:
        if s.symbol == symbol:
            stock = s
            break
    
    if not stock:
        flash(f'Stock {symbol} not found', 'error')
        return redirect(url_for('show_portfolio'))
    
    if request.method == 'POST':
        try:
            # Update stock data
            stock.name = request.form.get('name', stock.name)
            stock.shares = int(request.form.get('shares', stock.shares))
            stock.price = float(request.form.get('price', stock.price))
            
            # Update dividend schedule if provided
            if request.form.get('dividend_amount'):
                amount = float(request.form.get('dividend_amount', 0.0))
                frequency = request.form.get('frequency', 'quarterly')
                next_date_str = request.form.get('next_date')
                
                if next_date_str:
                    next_date = datetime.strptime(next_date_str, '%Y-%m-%d')
                    if stock.dividend_schedule:
                        stock.dividend_schedule.amount = amount
                        stock.dividend_schedule.frequency = frequency
                        stock.dividend_schedule.next_ex_dividend_date = next_date
                    else:
                        schedule = DividendSchedule(
                            amount=amount,
                            frequency=frequency,
                            next_ex_dividend_date=next_date
                        )
                        stock.dividend_schedule = schedule
            
            flash(f'Successfully updated {symbol}!', 'success')
            return redirect(url_for('show_portfolio'))
            
        except ValueError as e:
            flash(f'Error updating stock: {str(e)}', 'error')
    
    return render_template('edit_stock.html', stock=stock)

@app.route('/delete-stock/<symbol>', methods=['POST'])
def delete_stock(symbol):
    """Delete a stock from portfolio"""
    stock = None
    for s in portfolio.stocks:
        if s.symbol == symbol:
            stock = s
            break
    
    if stock:
        portfolio.remove_stock(stock)
        flash(f'Successfully removed {symbol} from portfolio', 'success')
    else:
        flash(f'Stock {symbol} not found', 'error')
    
    return redirect(url_for('show_portfolio'))

@app.route('/api/dividend-summary')
def api_dividend_summary():
    """API endpoint for dividend summary"""
    summary = generate_dividend_summary(portfolio)
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
