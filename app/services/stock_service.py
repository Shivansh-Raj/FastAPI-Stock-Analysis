import yfinance as yf
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse, JSONResponse
from ..Schemas import schemas
import os

STATIC_DIR = "app/static"
os.makedirs(STATIC_DIR, exist_ok=True)  #Ensure that directory exists

def get_stock_history(ticker: str):
    stock = yf.Ticker(ticker)
    data = stock.history(period ="1y")
    return data.to_dict()

def calculate_sma(ticker: str, window: str):
    stock = yf.Ticker(ticker)
    data = stock.history(period = "1y")
    data["SMA"] = data["Close"].rolling(window = window).mean()
    return data[["Close", "SMA"]].dropna().to_dict()

def generate_chart(ticker: str, window: str):
    stock = yf.Ticker(ticker)
    data = stock.history(period = "1y")
    data["SMA"] = data["Close"].rolling(window=window).mean()

    plt.figure(figsize = (10, 5))
    sns.lineplot(data = data, x = data.index, y = "Close", label = "Closing Price")
    sns.lineplot(data = data, x = data.index, y = "SMA", label = f"{window}-Day SMA")
    plt.title(f"{ticker} Stock Price with SMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    file_path = f"{STATIC_DIR}/{ticker}_chart.png"
    plt.savefig(file_path)
    plt.close()

    return FileResponse(file_path)


def generate_signal(ticker: str, short_window: int = 10, long_window: int = 50):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")

    # Calculate Short & Long SMAs
    data["SMA_short"] = data["Close"].rolling(window=short_window).mean()
    data["SMA_long"] = data["Close"].rolling(window=long_window).mean()

    data["Signal"] = np.where(
        (data["SMA_short"].shift(2) < data["SMA_long"].shift(2)) 
        & ((data["SMA_short"].shift(1) > data["SMA_long"].shift(1)) 
        & (data["SMA_short"].shift(2) > data["SMA_long"].shift(2))),
        "BUY",
        np.where(
            (data["SMA_short"].shift(1) > data["SMA_long"].shift(1)) & (data["SMA_short"] < data["SMA_long"]),
            "SELL",
            "HOLD"
        )
    )

    last_signal = data["Signal"].iloc[-1]
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x=data.index, y="Close", label="Stock Price", color="black")
    sns.lineplot(data=data, x=data.index, y="SMA_short", label=f"{short_window}-Day SMA", color="blue")
    sns.lineplot(data=data, x=data.index, y="SMA_long", label=f"{long_window}-Day SMA", color="orange")

    plt.fill_between(data.index, data["SMA_short"], data["SMA_long"], 
                     where=(data["SMA_short"] > data["SMA_long"]), color="green", alpha=0.3, label="BUY Zone")
    
    plt.fill_between(data.index, data["SMA_short"], data["SMA_long"], 
                     where=(data["SMA_short"] < data["SMA_long"]), color="red", alpha=0.3, label="SELL Zone")
    plt.text(
        0.95, 0.95, f"Last Signal: {last_signal}", 
        horizontalalignment='right', verticalalignment='top', 
        transform=plt.gca().transAxes,
        fontsize=12, color="purple", fontweight='bold', bbox=dict(facecolor="white", edgecolor="purple", boxstyle="round,pad=0.3")
    )

    # Title, Labels, and Legend
    plt.title(f"{ticker} Stock Price with SMA Strategy")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    
    # Save Chart
    file_path = f"{STATIC_DIR}/{ticker}_chart.png"
    plt.savefig(file_path)
    plt.close()

    return FileResponse(file_path)


def backtest_strategy(ticker: str, initial_balance: int = 10000, traling_on: bool = False, short_window: int = 10, long_window: int = 50):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")

    # Calculating short and long SMAs
    data["SMA_short"] = data["Close"].rolling(window=short_window).mean()
    data["SMA_long"] = data["Close"].rolling(window=long_window).mean()

    balance = initial_balance
    position = 0
    buy_price = 0
    trade_log = []
    target_price = 0
    stop_loss = 0
    last_balance = initial_balance  

    for i in range(52, len(data)):  
        current_price = data["Close"].iloc[i]

        # BUY condition (Confirm SMA crossover for 2 consecutive days)
        if position == 0:
            if (data["SMA_short"].iloc[i - 1] > data["SMA_long"].iloc[i - 1] and
                data["SMA_short"].iloc[i] > data["SMA_long"].iloc[i]):

                buy_price = current_price
                target_price = buy_price * 1.1
                stop_loss = buy_price * 0.95  
                position = balance / buy_price
                balance = 0
                trade_log.append(f"BUY at {buy_price:.2f} on {data.index[i].date()}")

        # Holding a position -> Check for SL/Target updates
        elif position > 0:
            if current_price <= stop_loss:
                balance = position * stop_loss
                trade_log.append(f"SELL at {current_price:.2f} (Stop Loss) on {data.index[i].date()}")
                position = 0
                last_balance = balance

            elif current_price >= target_price and traling_on:
                target_price = current_price * 1.10  
                stop_loss = target_price * 0.95
                trade_log.append(f"TARGET UPDATED: New Target {target_price:.2f}, Stop Loss {stop_loss:.2f} on {data.index[i].date()}")

            elif current_price >= target_price:
                balance = position * current_price
                trade_log.append(f"SELL at {current_price:.2f} (Stop Loss) on {data.index[i].date()}")
                position = 0
                last_balance = balance

    # If still holding a position, sell at the last available price
    if position > 0:
        balance = position * data["Close"].iloc[-1]
        trade_log.append(f"Final SELL at {data['Close'].iloc[-1]:.2f} on {data.index[-1].date()}")
        last_balance = balance

    return schemas.BacktestResult(status="success", final_balance=round(last_balance, 2), trades=trade_log)
