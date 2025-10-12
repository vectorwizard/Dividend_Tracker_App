from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timedelta
import os

# Import existing modules
from models import Stock, Portfolio, Dividend, DividendSchedule
from calculator import DividendCalculator
from sample_data import generate_sample_data

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize portfolio with sample data
portfolio = generate_sample_data()
calculator = DividendCalculator(portfolio)

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
    
    # Get upcoming dividends
    upcoming = calculator.get_upcoming_dividends(days=30)
    
    return render_template('index.html',
                         total_value=total_value,
                         total_annual_dividends=total_annual_dividends,
                         portfolio_yield=portfolio_yield,
                         stock_count=len(portfolio.stocks),
                         recent_dividends=recent_dividends[:5],
                         upcoming_dividends=upcoming[:5])

@app.route('/portfolio')
def portfolio_view():
    """Detailed portfolio view showing all stocks"""
    stocks_data = []
    for stock in portfolio.stocks:
        annual_dividend = stock.calculate_annual_dividend()
        dividend_yield = (annual_dividend / stock.current_price * 100) if stock.current_price > 0 else 0
        
        stocks_data.append({
            'symbol': stock.symbol,
            'name': stock.name,
            'shares': stock.shares,
            'current_price': stock.current_price,
            'total_value': stock.shares * stock.current_price,
            'dividend_amount': stock.dividend_amount,
            'dividend_frequency': stock.dividend_frequency,
            'annual_dividend': annual_dividend,
            'dividend_yield': dividend_yield,
            'total_annual_income': annual_dividend * stock.shares
        })
    
    total_value = portfolio.get_total_value()
    total_annual_income = portfolio.get_total_annual_dividends()
    
    return render_template('portfolio.html',
                         stocks=stocks_data,
                         total_value=total_value,
                         total_annual_income=total_annual_income)

@app.route('/dividend-history')
def dividend_history():
    """View all historical dividend payments"""
    all_dividends = []
    
    for stock in portfolio.stocks:
        for div in stock.dividend_history:
            all_dividends.append({
                'symbol': stock.symbol,
                'name': stock.name,
                'date': div.payment_date,
                'amount_per_share': div.amount,
                'shares': stock.shares,
                'total_amount': div.amount * stock.shares,
                'ex_date': div.ex_dividend_date
            })
    
    # Sort by date, most recent first
    all_dividends.sort(key=lambda x: x['date'], reverse=True)
    
    # Calculate summary statistics
    total_received = sum(d['total_amount'] for d in all_dividends)
    
    # Monthly breakdown
    monthly_totals = {}
    for div in all_dividends:
        month_key = div['date'].strftime('%Y-%m')
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + div['total_amount']
    
    return render_template('dividend_history.html',
                         dividends=all_dividends,
                         total_received=total_received,
                         monthly_totals=monthly_totals)

@app.route('/projections')
def projections():
    """View dividend projections for upcoming periods"""
    # Get projections for different time periods
    monthly_projection = calculator.calculate_monthly_projection()
    quarterly_projection = calculator.calculate_quarterly_projection()
    annual_projection = calculator.calculate_annual_projection()
    
    # Get upcoming dividends for next 90 days
    upcoming = calculator.get_upcoming_dividends(days=90)
    
    # Calculate growth scenarios
    current_annual = portfolio.get_total_annual_dividends()
    growth_scenarios = [
        {'rate': 0, 'year_1': current_annual, 'year_3': current_annual, 'year_5': current_annual},
        {'rate': 3, 'year_1': current_annual * 1.03, 'year_3': current_annual * (1.03**3), 'year_5': current_annual * (1.03**5)},
        {'rate': 5, 'year_1': current_annual * 1.05, 'year_3': current_annual * (1.05**3), 'year_5': current_annual * (1.05**5)},
        {'rate': 7, 'year_1': current_annual * 1.07, 'year_3': current_annual * (1.07**3), 'year_5': current_annual * (1.07**5)},
    ]
    
    return render_template('projections.html',
                         monthly_projection=monthly_projection,
                         quarterly_projection=quarterly_projection,
                         annual_projection=annual_projection,
                         upcoming_dividends=upcoming,
                         growth_scenarios=growth_scenarios)

@app.route('/stock/add', methods=['GET', 'POST'])
def add_stock():
    """Add a new stock to the portfolio"""
    if request.method == 'POST':
        try:
            symbol = request.form['symbol'].upper()
            name = request.form['name']
            shares = float(request.form['shares'])
            current_price = float(request.form['current_price'])
            dividend_amount = float(request.form['dividend_amount'])
            dividend_frequency = request.form['dividend_frequency']
            
            new_stock = Stock(
                symbol=symbol,
                name=name,
                shares=shares,
                current_price=current_price,
                dividend_amount=dividend_amount,
                dividend_frequency=dividend_frequency
            )
            
            portfolio.add_stock(new_stock)
            flash(f'Successfully added {symbol} to portfolio!', 'success')
            return redirect(url_for('portfolio_view'))
        except Exception as e:
            flash(f'Error adding stock: {str(e)}', 'error')
            return redirect(url_for('add_stock'))
    
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
            stock.name = request.form['name']
            stock.shares = float(request.form['shares'])
            stock.current_price = float(request.form['current_price'])
            stock.dividend_amount = float(request.form['dividend_amount'])
            stock.dividend_frequency = request.form['dividend_frequency']
            
            flash(f'Successfully updated {symbol}!', 'success')
            return redirect(url_for('portfolio_view'))
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
    upcoming = calculator.get_upcoming_dividends(days=days)
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
