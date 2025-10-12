from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timedelta
import os

# Import existing modules
from models import Stock, Portfolio, Dividend, DividendSchedule
from calculator import calculate_annual_dividend_income, project_dividend_income, generate_dividend_summary, format_inr
from sample_data import generate_sample_data

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize portfolio with sample data
portfolio = generate_sample_data()

@app.route('/')
def index():
    """Main dashboard showing overview of portfolio and dividends"""
    
    # Calculate key metrics
    total_value = portfolio.get_total_value()
    total_annual_dividends = portfolio.get_total_annual_dividends()
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
    recent_dividends.sort(key=lambda x: x['date'], reverse=True)
    
    # Get upcoming dividends (next 30 days)
    thirty_days_ahead = datetime.now() + timedelta(days=30)
    upcoming_dividends = []
    
    for stock in portfolio.stocks:
        if stock.dividend_schedule:
            next_payment = stock.dividend_schedule.next_payment_date
            if next_payment and next_payment <= thirty_days_ahead:
                upcoming_dividends.append({
                    'symbol': stock.symbol,
                    'date': next_payment,
                    'amount': stock.dividend_amount * stock.shares
                })
    upcoming_dividends.sort(key=lambda x: x['date'])
    
    return render_template('index.html',
                         total_value=total_value,
                         total_annual_dividends=total_annual_dividends,
                         portfolio_yield=portfolio_yield,
                         recent_dividends=recent_dividends[:5],
                         upcoming_dividends=upcoming_dividends[:5],
                         stock_count=len(portfolio.stocks))

@app.route('/portfolio')
def portfolio_view():
    """Detailed portfolio view showing all stocks"""
    stocks_data = []
    
    for stock in portfolio.stocks:
        annual_dividend = stock.calculate_annual_dividend()
        total_value = stock.shares * stock.current_price
        yield_pct = (annual_dividend / total_value * 100) if total_value > 0 else 0
        
        stocks_data.append({
            'symbol': stock.symbol,
            'name': stock.name,
            'shares': stock.shares,
            'current_price': stock.current_price,
            'total_value': total_value,
            'annual_dividend': annual_dividend,
            'yield': yield_pct,
            'dividend_frequency': stock.dividend_frequency
        })
    
    # Sort by total value descending
    stocks_data.sort(key=lambda x: x['total_value'], reverse=True)
    
    return render_template('portfolio.html',
                         stocks=stocks_data,
                         total_value=portfolio.get_total_value(),
                         total_annual_dividends=portfolio.get_total_annual_dividends())

@app.route('/dividends')
def dividends_view():
    """Dividend tracking and projections view"""
    
    # Get dividend summary
    summary = generate_dividend_summary(portfolio)
    
    # Calculate projections using project_dividend_income
    monthly_projection = project_dividend_income(portfolio, months=1, growth_rate=0.0)
    quarterly_projection = project_dividend_income(portfolio, months=3, growth_rate=0.0)
    annual_projection = calculate_annual_dividend_income(portfolio)
    
    # Get upcoming dividends (next 90 days)
    ninety_days_ahead = datetime.now() + timedelta(days=90)
    upcoming_dividends = []
    
    for stock in portfolio.stocks:
        if stock.dividend_schedule:
            next_payment = stock.dividend_schedule.next_payment_date
            if next_payment and next_payment <= ninety_days_ahead:
                upcoming_dividends.append({
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'date': next_payment,
                    'amount': stock.dividend_amount * stock.shares,
                    'frequency': stock.dividend_frequency
                })
    upcoming_dividends.sort(key=lambda x: x['date'])
    
    return render_template('dividends.html',
                         summary=summary,
                         monthly_projection=monthly_projection,
                         quarterly_projection=quarterly_projection,
                         annual_projection=annual_projection,
                         upcoming_dividends=upcoming_dividends)

@app.route('/stock/<symbol>')
def stock_detail(symbol):
    """Detailed view of a single stock"""
    stock = portfolio.get_stock(symbol)
    
    if not stock:
        flash(f'Stock {symbol} not found', 'error')
        return redirect(url_for('portfolio_view'))
    
    # Calculate metrics
    annual_dividend = stock.calculate_annual_dividend()
    total_value = stock.shares * stock.current_price
    yield_pct = (annual_dividend / total_value * 100) if total_value > 0 else 0
    
    # Get dividend history
    history = [{
        'date': div.payment_date,
        'amount': div.amount,
        'total': div.amount * stock.shares
    } for div in stock.dividend_history]
    history.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('stock_detail.html',
                         stock=stock,
                         annual_dividend=annual_dividend,
                         total_value=total_value,
                         yield_pct=yield_pct,
                         history=history)

@app.route('/stock/add', methods=['GET', 'POST'])
def add_stock():
    """Add a new stock to the portfolio"""
    if request.method == 'POST':
        try:
            symbol = request.form.get('symbol').upper()
            name = request.form.get('name')
            shares = float(request.form.get('shares'))
            current_price = float(request.form.get('current_price'))
            dividend_amount = float(request.form.get('dividend_amount', 0))
            dividend_frequency = request.form.get('dividend_frequency', 'quarterly')
            
            # Create new stock
            stock = Stock(
                symbol=symbol,
                name=name,
                shares=shares,
                current_price=current_price,
                dividend_amount=dividend_amount,
                dividend_frequency=dividend_frequency
            )
            
            portfolio.add_stock(stock)
            flash(f'Successfully added {symbol} to portfolio', 'success')
            return redirect(url_for('portfolio_view'))
            
        except Exception as e:
            flash(f'Error adding stock: {str(e)}', 'error')
    
    return render_template('add_stock.html')

@app.route('/stock/<symbol>/edit', methods=['GET', 'POST'])
def edit_stock(symbol):
    """Edit an existing stock in the portfolio"""
    stock = portfolio.get_stock(symbol)
    
    if not stock:
        flash(f'Stock {symbol} not found', 'error')
        return redirect(url_for('portfolio_view'))
    
    if request.method == 'POST':
        try:
            stock.name = request.form.get('name')
            stock.shares = float(request.form.get('shares'))
            stock.current_price = float(request.form.get('current_price'))
            stock.dividend_amount = float(request.form.get('dividend_amount', 0))
            stock.dividend_frequency = request.form.get('dividend_frequency', 'quarterly')
            
            flash(f'Successfully updated {symbol}', 'success')
            return redirect(url_for('stock_detail', symbol=symbol))
            
        except Exception as e:
            flash(f'Error updating stock: {str(e)}', 'error')
    
    return render_template('edit_stock.html', stock=stock)

@app.route('/stock/<symbol>/delete', methods=['POST'])
def delete_stock(symbol):
    """Delete a stock from the portfolio"""
    try:
        portfolio.remove_stock(symbol)
        flash(f'Successfully removed {symbol} from portfolio', 'success')
    except Exception as e:
        flash(f'Error removing stock: {str(e)}', 'error')
    
    return redirect(url_for('portfolio_view'))

@app.route('/api/portfolio/summary')
def api_portfolio_summary():
    """API endpoint for portfolio summary data"""
    return jsonify({
        'total_value': portfolio.get_total_value(),
        'total_annual_dividends': portfolio.get_total_annual_dividends(),
        'stock_count': len(portfolio.stocks),
        'average_yield': portfolio.get_average_yield()
    })

@app.route('/api/dividends/upcoming')
def api_upcoming_dividends():
    """API endpoint for upcoming dividends"""
    days = request.args.get('days', default=30, type=int)
    target_date = datetime.now() + timedelta(days=days)
    upcoming = []
    
    for stock in portfolio.stocks:
        if stock.dividend_schedule:
            next_payment = stock.dividend_schedule.next_payment_date
            if next_payment and next_payment <= target_date:
                upcoming.append({
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'date': next_payment.isoformat(),
                    'amount': stock.dividend_amount * stock.shares
                })
    
    return jsonify(upcoming)

@app.route('/api/stock/<symbol>')
def api_stock_detail(symbol):
    """API endpoint for individual stock details"""
    stock = portfolio.get_stock(symbol)
    
    if not stock:
        return jsonify({'error': 'Stock not found'}), 404
    
    return jsonify({
        'symbol': stock.symbol,
        'name': stock.name,
        'shares': stock.shares,
        'current_price': stock.current_price,
        'dividend_amount': stock.dividend_amount,
        'dividend_frequency': stock.dividend_frequency,
        'annual_dividend': stock.calculate_annual_dividend(),
        'total_value': stock.shares * stock.current_price
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
