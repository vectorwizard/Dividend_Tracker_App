        lines = [
            "Past Dividends (by Ex-Date):"
        ]
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
                writer = csv.DictWriter(f, fieldnames=['symbol','name','qty','avg_price','fy_div','freq','last_div','next_div'])
                writer.writeheader()
                for row in self.portfolio:
                    writer.writerow(row)
            messagebox.showinfo("Saved", "Portfolio saved to CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV: {e}")

    def export_analytics(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", title="Export Analytics CSV", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Metric", "Value"])
                total_invested = sum(x['qty'] * x['avg_price'] for x in self.portfolio)
                annual_income = sum(x['qty'] * x['fy_div'] for x in self.portfolio)
                monthly_income = annual_income / 12 if annual_income else 0
                writer.writerow(["Total Invested", f"{INR}{total_invested:,.2f}"])
                writer.writerow(["Annual Dividend Income", f"{INR}{annual_income:,.2f}"])
                writer.writerow(["Monthly Avg Income", f"{INR}{monthly_income:,.2f}"])
            messagebox.showinfo("Exported", "Analytics exported to CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export analytics: {e}")

    def show_help(self):
        message = (
            "Usage:\n"
            "1) Add holdings in Portfolio tab, then Save Portfolio CSV.\n"
            "2) Record individual dividends in Dividends tab.\n"
            "3) Use Analytics tab to calculate income, projections, and export summary.\n"
        )
        messagebox.showinfo("Usage Instructions", message)

if __name__ == "__main__":
    app = DividendTrackerApp()
    app.mainloop()
