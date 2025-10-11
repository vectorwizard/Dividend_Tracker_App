# Dividend Tracker App - Indian Stock Market Edition

A simple GUI to track dividend income, yield, payment dates, payout history, and future dividend estimates for Indian stocks (NSE/BSE) in INR (₹).

## New: Tkinter GUI
The repository now includes a desktop GUI built with Tkinter.
- File: gui.py
- Currency: INR (₹)
- OS: Windows/Linux/macOS (Python 3.8+)

### Features in GUI
- Portfolio tab: add/update Indian stock holdings with symbol, qty, average price, FY dividend per share, frequency, and last/next dividend dates.
- Dividends tab: record dividend events with ex-date, pay-date, and amount per share.
- Analytics tab: buttons for Total/Annual/Monthly income, Yield on Cost per holding, upcoming/past dividends lists, and a 12-month payout projection.
- Export: save portfolio to CSV and export analytics text to CSV/plain text.

## Quick Start
1) Install Python 3.8+.
2) Clone the repo and open a terminal in the project folder.
3) Run the GUI:
   - Windows: py gui.py
   - macOS/Linux: python3 gui.py

## Data Format (Portfolio CSV)
Columns expected when loading/saving portfolio.csv:
- symbol, name, qty, avg_price, fy_div, freq, last_div, next_div

Example:
```
symbol,name,qty,avg_price,fy_div,freq,last_div,next_div
RELIANCE,Reliance Industries,10,2550.00,40.0,1,2025-05-01,2026-05-01
TCS,Tata Consultancy Services,5,3900.00,90.0,2,2025-06-10,2025-12-10
```

## Using the GUI
- Portfolio tab:
  - Enter details and click "Add/Update". Select a row and click "Remove Selected" to delete.
  - Use File > Save Portfolio CSV to persist your portfolio.
- Dividends tab:
  - Record each dividend with ex/pay dates and amount per share.
- Analytics tab:
  - Calculate Income: Shows Total Invested, Annual, and Monthly dividend income in ₹.
  - Yield & Projections: Shows YoC per stock and the next payouts projection.
  - Upcoming Dividends: Uses recorded dividends by ex-date ≥ today.
  - Past Dividends: Uses recorded dividends by ex-date < today and totals collected.
  - Export Output: Save the analytics text to a file.

## Notes and Assumptions
- All amounts are treated as INR (₹).
- Frequency (freq/yr) is used for next 12-month projection with the next_div date as a starting point.
- Dates must be YYYY-MM-DD.
- The GUI does not fetch live market data; values are user-supplied.

## Troubleshooting
- If the window is too small, resize; the tables and text area are responsive.
- CSV load errors: check column names and numeric formats.

## License
MIT
