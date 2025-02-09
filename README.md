# SMA Strategy Analysis with Backtesting

## Overview

This is **My First FastAPI-based project** that provides various endpoints for analyzing stock market trends using the Simple Moving Average (SMA) strategy. The application allows users to fetch historical stock data, compute SMA values, generate stock charts with SMA overlays, and backtest trading strategies using SMA crossovers.

## Live Demo

- Check out the live version of the API at: Live API[https://fastapi-stock-analysis.onrender.com/docs#/]

## Features

- Fetch historical stock price data for any given ticker.
- Compute Simple Moving Averages (SMA) over customizable time windows.
- Generate stock price charts with SMA overlays for trend analysis.
- Identify Buy/Sell signals based on SMA crossovers.
- Backtest the SMA strategy on historical data, with optional trailing stop-loss functionality.

## Technologies Used

- **FastAPI** - Web framework for API development.
- **yFinance** - Fetching stock market data.
- **Matplotlib & Seaborn** - Data visualization for stock charts.
- **NumPy & Pandas** - Data processing and analysis.
- **Uvicorn** - ASGI server for running FastAPI.

## Installation

### Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the API Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

This will start the API at `http://127.0.0.1:8000`

### API Endpoints

#### 1. Fetch Stock Price History

**GET /stocks/history/{ticker}**

- Retrieves historical stock price data for the specified ticker.

#### 2. Compute Simple Moving Average (SMA)

**GET /stocks/sma/{ticker}/{window}**

- Computes SMA for a given stock over the specified window size.

#### 3. Generate Stock Chart with SMA Overlay

**GET /stocks/chart/{ticker}/{window}**

- Generates a stock price chart with an SMA overlay.

#### 4. Generate Buy/Sell Signals using SMA Strategy

**GET /stocks/signal-sma/{ticker}**

- Identifies buy/sell signals based on SMA crossover strategy.

#### 5. Backtest SMA Strategy on Stock Data

**GET /stocks/backtest/{ticker}?initial\_balance=10000&do\_trailing\_StopLoss=False**

- Simulates trades based on SMA strategy and calculates the performance over the past year.
- Optional parameters:
  - `initial_balance`: Starting capital (default: \$10,000)
  - `do_trailing_StopLoss`: Enables trailing stop-loss (default: False)

## Example Usage

```bash
# Fetch stock history for Apple (AAPL)
curl http://127.0.0.1:8000/stocks/history/AAPL

# Calculate 20-day SMA for AAPL
curl http://127.0.0.1:8000/stocks/sma/AAPL/20

# Generate stock chart with 50-day SMA
curl http://127.0.0.1:8000/stocks/chart/AAPL/50

# Get Buy/Sell signals for AAPL
curl http://127.0.0.1:8000/stocks/signal-sma/AAPL

# Backtest strategy for AAPL with $20,000 starting balance
curl http://127.0.0.1:8000/stocks/backtest/AAPL?initial_balance=20000
```

## Future Enhancements

- Implement Exponential Moving Average (EMA) strategy.
- Add support for additional technical indicators (RSI, MACD, Bollinger Bands).
- Build a frontend dashboard for visualizing stock analysis interactively.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to improve the project.

---

**Author:** Shivansh Rajdehl | [GitHub](https://github.com/Shivansh-Raj)

