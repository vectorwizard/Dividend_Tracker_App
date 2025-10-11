import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, date

INR = "\u20B9"  # ₹

class DividendTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dividend Tracker - GUI")
        self.geometry("1000x650")
        self.minsize(900, 580)

        self.portfolio = []  # list of dicts: {symbol, name, qty, avg_price, last_div, next_div, freq, fy_div}
        self.dividends = []  # list of dicts: {symbol, ex_date, pay_date, amount_per_share}

        self._build_menu()
        self._build_tabs()

    # UI builders
    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Portfolio CSV", command=self.load_portfolio)
        file_menu.add_command(label="Save Portfolio CSV", command=self.save_portfolio)
        file_menu.add_separator()
        file_menu.add_command(label="Export Analytics CSV", command=self.export_analytics)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Usage Instructions", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _build_tabs(self):
        nb = ttk.Notebook(self)

        # Portfolio Tab
        self.portfolio_frame = ttk.Frame(nb)
        self._build_portfolio_tab(self.portfolio_frame)
        nb.add(self.portfolio_frame, text="Portfolio")

        # Dividends Tab
        self.div_frame = ttk.Frame(nb)
        self._build_dividends_tab(self.div_frame)
        nb.add(self.div_frame, text="Dividends")

        # Analytics Tab
        self.analytics_frame = ttk.Frame(nb)
        self._build_analytics_tab(self.analytics_frame)
        nb.add(self.analytics_frame, text="Analytics")

        nb.pack(fill=tk.BOTH, expand=True)

    def _build_portfolio_tab(self, parent):
        form = ttk.LabelFrame(parent, text="Add / Update Holding (INR)")
        form.pack(fill=tk.X, padx=10, pady=10)

        labels = ["Symbol", "Name", "Qty", "Avg Price (₹)", "FY Div/Share (₹)", "Freq/yr", "Last Div Date (YYYY-MM-DD)", "Next Div Date (YYYY-MM-DD)"]
        self.p_vars = {k: tk.StringVar() for k in labels}
        for i, key in enumerate(labels):
            ttk.Label(form, text=key).grid(row=0, column=i, padx=5, pady=5)
            ttk.Entry(form, textvariable=self.p_vars[key], width=16).grid(row=1, column=i, padx=5, pady=5)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=len(labels), sticky="w", padx=5, pady=5)
        ttk.Button(btns, text="Add/Update", command=self.add_update_holding).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Remove Selected", command=self.remove_selected_holding).pack(side=tk.LEFT, padx=5)

        # Table
        cols = ("symbol", "name", "qty", "avg_price", "fy_div", "freq", "last_div", "next_div")
        self.portfolio_tv = ttk.Treeview(parent, columns=cols, show="headings", height=12)
        headings = [
            ("symbol", "Symbol"), ("name", "Name"), ("qty", "Qty"), ("avg_price", f"Avg Price ({INR})"),
            ("fy_div", f"FY Div/Share ({INR})"), ("freq", "Freq/yr"), ("last_div", "Last Div"), ("next_div", "Next Div")
        ]
        for cid, text in headings:
            self.portfolio_tv.heading(cid, text=text)
            self.portfolio_tv.column(cid, width=120 if cid != 'name' else 170, anchor=tk.CENTER)
        self.portfolio_tv.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

    def _build_dividends_tab(self, parent):
        form = ttk.LabelFrame(parent, text="Record Dividend (INR)")
        form.pack(fill=tk.X, padx=10, pady=10)
        labels = ["Symbol", "Ex-Date (YYYY-MM-DD)", "Pay-Date (YYYY-MM-DD)", "Amount/Share (₹)"]
        self.d_vars = {k: tk.StringVar() for k in labels}
        for i, key in enumerate(labels):
            ttk.Label(form, text=key).grid(row=0, column=i, padx=5, pady=5)
            ttk.Entry(form, textvariable=self.d_vars[key], width=18).grid(row=1, column=i, padx=5, pady=5)
        ttk.Button(form, text="Add Dividend", command=self.add_dividend).grid(row=1, column=len(labels), padx=8)

        cols = ("symbol", "ex_date", "pay_date", "amount")
        self.div_tv = ttk.Treeview(parent, columns=cols, show="headings", height=12)
        self.div_tv.heading("symbol", text="Symbol")
        self.div_tv.heading("ex_date", text="Ex-Date")
        self.div_tv.heading("pay_date", text="Pay-Date")
        self.div_tv.heading("amount", text=f"Amount/Share ({INR})")
        for cid in cols:
            self.div_tv.column(cid, width=160, anchor=tk.CENTER)
        self.div_tv.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

    def _build_analytics_tab(self, parent):
        action = ttk.Frame(parent)
        action.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(action, text="Calculate Income", command=self.calculate_income).pack(side=tk.LEFT, padx=5)
        ttk.Button(action, text="Yield & Projections", command=self.calculate_yield_projection).pack(side=tk.LEFT, padx=5)
        ttk.Button(action, text="Upcoming Dividends", command=self.show_upcoming).pack(side=tk.LEFT, padx=5)
        ttk.Button(action, text="Past Dividends", command=self.show_past).pack(side=tk.LEFT, padx=5)
        ttk.Button(action, text="Export Output", command=self.export_analytics).pack(side=tk.LEFT, padx=5)

        self.output = tk.Text(parent, height=18)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        self.output.configure(state=tk.DISABLED)

    # Data helpers
    def _refresh_portfolio_table(self):
        for r in self.portfolio_tv.get_children():
            self.portfolio_tv.delete(r)
        for item in self.portfolio:
            self.portfolio_tv.insert("", tk.END, values=(
                item['symbol'], item['name'], item['qty'], f"{item['avg_price']:.2f}",
                f"{item['fy_div']:.2f}", item['freq'], item['last_div'], item['next_div']
            ))

    def add_update_holding(self):
        try:
            symbol = self.p_vars["Symbol"].get().strip().upper()
            if not symbol:
                raise ValueError("Symbol required")
            name = self.p_vars["Name"].get().strip() or symbol
            qty = int(float(self.p_vars["Qty"].get()))
            avg_price = float(self.p_vars["Avg Price (₹)"].get())
            fy_div = float(self.p_vars["FY Div/Share (₹)"].get() or 0)
            freq = int(float(self.p_vars["Freq/yr"].get() or 1))
            last_div = self.p_vars["Last Div Date (YYYY-MM-DD)"].get().strip()
            next_div = self.p_vars["Next Div Date (YYYY-MM-DD)"].get().strip()
            # Basic date validation if provided
            for dv in [last_div, next_div]:
                if dv:
                    datetime.strptime(dv, "%Y-%m-%d")
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Please check values: {e}")
            return

        existing = next((x for x in self.portfolio if x['symbol'] == symbol), None)
        payload = {
            'symbol': symbol, 'name': name, 'qty': qty, 'avg_price': avg_price,
            'fy_div': fy_div, 'freq': freq, 'last_div': last_div, 'next_div': next_div
        }
        if existing:
            existing.update(payload)
        else:
            self.portfolio.append(payload)
        self._refresh_portfolio_table()

    def remove_selected_holding(self):
        sel = self.portfolio_tv.selection()
        if not sel:
            return
        values = self.portfolio_tv.item(sel[0], 'values')
        symbol = values[0]
        self.portfolio = [x for x in self.portfolio if x['symbol'] != symbol]
        self._refresh_portfolio_table()

    def add_dividend(self):
        try:
            symbol = self.d_vars["Symbol"].get().strip().upper()
            ex_date = self.d_vars["Ex-Date (YYYY-MM-DD)"].get().strip()
            pay_date = self.d_vars["Pay-Date (YYYY-MM-DD)"].get().strip()
            amount = float(self.d_vars["Amount/Share (₹)"].get())
            datetime.strptime(ex_date, "%Y-%m-%d")
            datetime.strptime(pay_date, "%Y-%m-%d")
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Please check values: {e}")
            return
        item = {"symbol": symbol, "ex_date": ex_date, "pay_date": pay_date, "amount": amount}
        self.dividends.append(item)
        self._refresh_div_table()

    def _refresh_div_table(self):
        for r in self.div_tv.get_children():
            self.div_tv.delete(r)
        for d in self.dividends:
            self.div_tv.insert("", tk.END, values=(d['symbol'], d['ex_date'], d['pay_date'], f"{d['amount']:.2f}"))

    # Analytics actions
    def calculate_income(self):
        total_invested = sum(x['qty'] * x['avg_price'] for x in self.portfolio)
        annual_income = sum(x['qty'] * x['fy_div'] for x in self.portfolio)
        monthly_income = annual_income / 12 if annual_income else 0
        self._write_output([
            f"Total Invested: {INR}{total_invested:,.2f}",
            f"Annual Dividend Income: {INR}{annual_income:,.2f}",
            f"Monthly Avg Income: {INR}{monthly_income:,.2f}",
        ])

    def calculate_yield_projection(self):
        lines = []
        for x in self.portfolio:
            invested = x['qty'] * x['avg_price']
            income = x['qty'] * x['fy_div']
            yoc = (income / invested * 100) if invested else 0
            lines.append(f"{x['symbol']}: Invested {INR}{invested:,.2f}, Income {INR}{income:,.2f}, YoC {yoc:.2f}%")
        # Simple next 12 months projection using next_div and freq
        today = date.today()
        upcoming = []
        for x in self.portfolio:
            if x['next_div']:
                try:
                    nd = datetime.strptime(x['next_div'], "%Y-%m-%d").date()
                    step = 12 // max(1, x['freq'])
                    amt_each = (x['qty'] * x['fy_div']) / max(1, x['freq'])
                    while nd <= date(today.year, 12, 31):
                        if nd >= today:
                            upcoming.append((nd, x['symbol'], amt_each))
                        # move months forward
                        m = nd.month + step
                        y = nd.year + (m - 1) // 12
                        m = ((m - 1) % 12) + 1
                        d = min(nd.day, 28)  # safe day
                        nd = date(y, m, d)
                except Exception:
                    continue
        upcoming.sort(key=lambda t: t[0])
        lines.append("\nProjection (next payouts):")
        for nd, sym, amt in upcoming[:20]:
            lines.append(f"{nd.isoformat()} - {sym}: {INR}{amt:,.2f}")
        self._write_output(lines)

    def show_upcoming(self):
        today = date.today()
        rows = [d for d in self.dividends if datetime.strptime(d['ex_date'], "%Y-%m-%d").date() >= today]
        rows.sort(key=lambda d: d['ex_date'])
        lines = ["Upcoming Dividends (by Ex-Date):"]
        for d in rows:
            lines.append(f"{d['ex_date']} {d['symbol']} {INR}{d['amount']:.2f} (pay {d['pay_date']})")
        self._write_output(lines or ["No upcoming dividends recorded."])

    def show_past(self):
        today = date.today()
        rows = [d for d in self.dividends if datetime.strptime(d['ex_date'], "%Y-%m-%d").date() < today]
        rows.sort(key=lambda d: d['ex_date'], reverse=True)
        lines = ["Past Dividends (by Ex-Date):"]
        total = 0
        for d in rows:
            total += d['amount'] * next((x['qty'] for x in self.portfolio if x['symbol'] == d['symbol']), 0)
            lines.append(f"{d['ex_date']} {d['symbol']} {INR}{d['amount']:.2f} (paid {d['pay_date']})")
        lines.append(f"Total Collected (recorded): {INR}{total:,.2f}")
        self._write_output(lines)

    def _write_output(self, lines):
        self.output.configure(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        for line in lines:
            self.output.insert(tk.END, line + "\n")
        self.output.configure(state=tk.DISABLED)

    # File operations
    def load_portfolio(self):
        path = filedialog.askopenfilename(title="Open Portfolio CSV", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.portfolio = []
                for r in reader:
                    self.portfolio.append({
                        'symbol': r.get('symbol','').upper(),
                        'name': r.get('name',''),
                        'qty': int(float(r.get('qty',0) or 0)),
                        'avg_price': float(r.get('avg_price',0) or 0),
                        'fy_div': float(r.get('fy_div',0) or 0),
                        'freq': int(float(r.get('freq',1) or 1)),
                        'last_div': r.get('last_div',''),
                        'next_div': r.get('next_div',''),
                    })
            self._refresh_portfolio_table()
            messagebox.showinfo("Loaded", "Portfolio loaded from CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def save_portfolio(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", title="Save Portfolio CSV", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['symbol','name','qty','avg_price','fy_div','freq','
