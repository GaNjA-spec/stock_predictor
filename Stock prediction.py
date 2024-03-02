import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv
from datetime import datetime

common_stock_symbols = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc. (Google)",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla, Inc.",
    # Add more symbols and names as needed
}


def get_stock_data(symbol, period="1mo"):
    try:
        # Create a Ticker object for the stock symbol
        stock = yf.Ticker(symbol)

        # Get historical data
        data = stock.history(period=period)

        return data
    except Exception as e:
        return None


def plot_stock_data(data, symbol):
    if data is not None:
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data["Close"], label=f"{symbol} Closing Price", color='blue')
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.title(f"{symbol} Stock Price Trend")
        plt.legend()

        # Specify the number of subgrids for both x and y axes
        plt.grid(True, which="both", linestyle="--", alpha=0.7)

        # Set the y-axis limits to a smaller range (adjust as needed)
        plt.ylim(data["Close"].min() * 0.9, data["Close"].max() * 1.1)

        # Maximize the graph window
        plt.get_current_fig_manager().window.state('zoomed')

        # Display the graph
        plt.show()
    else:
        print(f"Error fetching data for {symbol}")


def get_next_closing_day(symbol):
    try:
        # Create a Ticker object for the stock symbol
        stock = yf.Ticker(symbol)

        # Get the next closing day
        next_closing_day = stock.calendar.iloc[0]["Earnings Date"]

        return next_closing_day
    except Exception as e:
        return None


def log_data_to_csv(symbol, current_price, next_closing_day):
    log_filename = "stock_data_log.csv"

    # Create the CSV file if it doesn't exist
    if not os.path.exists(log_filename):
        with open(log_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Symbol", "Current Price", "Next Closing Day"])

    # Append the data to the CSV file
    with open(log_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), symbol, current_price, next_closing_day])


if __name__ == "__main__":
    # Display common stock symbols and company names
    print("Common Stock Symbols and Company Names:")
    for symbol, name in common_stock_symbols.items():
        print(f"{symbol}: {name}")

    # Input the stock symbol you want to track
    stock_symbol = input("Enter a stock symbol from the list above: ").upper()

    # Get historical data for the stock
    stock_data = get_stock_data(stock_symbol)

    # Get the current stock price
    current_price = stock_data["Close"].iloc[-1]

    # Get the next closing day
    next_closing_day = get_next_closing_day(stock_symbol)

    # Plot the stock price trend
    plot_stock_data(stock_data, stock_symbol)

    # Log the data to a CSV file
    log_data_to_csv(stock_symbol, current_price, next_closing_day)

    if isinstance(current_price, float):
        print(f"The current price of {stock_symbol} is ${current_price:.2f}")

    if next_closing_day:
        print(f"The next closing day for {stock_symbol} is {next_closing_day}")
    else:
        print(f"Next closing day information not available for {stock_symbol}")

    print("Data has been logged to the CSV file.")
