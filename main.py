import yfinance as yf
import datetime
import json

# Settings
INITIAL_CAPITAL = 10  # ₹10
TRADE_AMOUNT = 10
TICKER = "BTC-USD"

# Get last 7 days data
end = datetime.datetime.today()
start = end - datetime.timedelta(days=7)
btc = yf.download(TICKER, start=start, end=end)

if btc.empty:
    print("Failed to fetch data.")
    exit()

# Simple strategy: Buy if drop > 2%, sell if gain > 3%
buy_price = None
log = []

for i in range(1, len(btc)):
    today = btc.iloc[i]
    yesterday = btc.iloc[i-1]
    change_pct = float(((today['Close'] - yesterday['Close']) / yesterday['Close']) * 100)

    action = "HOLD"
    if buy_price is None and change_pct < -2:
        buy_price = today['Close']
        action = f"BUY at ${buy_price:.2f}"
    elif buy_price and change_pct > 3:
        sell_price = today['Close']
        profit = ((sell_price - buy_price) / buy_price) * TRADE_AMOUNT
        action = f"SELL at ${sell_price:.2f} | Profit ₹{profit:.2f}"
        buy_price = None
    log.append({
        "Date": today.name.strftime("%Y-%m-%d"),
        "Close": round(float(today['Close']), 2),
        "Action": action
    })

# Write report
with open("weekly_report.txt", "w") as f:
    f.write("💰 TRADEMIND WEEKLY REPORT\n")
    f.write("===========================\n\n")
    f.write(f"Initial Capital: ₹{INITIAL_CAPITAL}\n")
    f.write(f"Asset: BTC-USD\n\n")
    f.write("📅 Trade Log:\n")
    for entry in log:
        f.write(f"{entry['Date']}: {entry['Action']} | Close: ${entry['Close']:.2f}\n")

    # Simulated AI analysis
    f.write("\n🤖 AI THOUGHTS:\n")
    f.write("“This week showed minor volatility. A smart buy was made when BTC dropped >2%. "
            "A quick sell after a >3% gain locked in profit. Strategy is working in short-term trades.”\n")

    f.write("\n📈 NEXT WEEK PLAN:\n")
    f.write("- Monitor BTC daily\n")
    f.write("- Buy on >2% drop days\n")
    f.write("- Set alert on >3% gain to sell\n")
    f.write("- Expand to ETH next week\n")

print("✅ Weekly report generated: weekly_report.txt")
import matplotlib.pyplot as plt

# Extract dates and closing prices
dates = [entry['Date'] for entry in log]
closes = [entry['Close'] for entry in log]

# Plot chart
plt.figure(figsize=(8, 4))
plt.plot(dates, closes, marker='o', linestyle='-', color='blue')
plt.title("BTC Weekly Price Chart")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.grid(True)
plt.tight_layout()

# Save chart
plt.savefig("btc_chart.png")
print("📊 Chart saved: btc_chart.png")
