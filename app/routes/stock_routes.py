from fastapi import APIRouter
from ..services import stock_service

router = APIRouter(
    tags=["SMA Strategy Analysis with Backtesting"],
    prefix="/stocks"
)

@router.get("/history/{ticker}", summary="Fetch Stock Price History")
def get_stock_history(ticker: str):
    """
    Retrieve historical stock price data for a given ticker.
    """
    return stock_service.get_stock_history(ticker)


@router.get("/sma/{ticker}/{window}", summary="Calculate Simple Moving Average (SMA)")
def get_moving_average(ticker: str, window: int):
    """
    Compute the Simple Moving Average (SMA) for a stock over a given window size.
    """
    return stock_service.calculate_sma(ticker, window)


@router.get("/chart/{ticker}/{window}", summary="Generate Stock Chart with SMA Overlay")
def get_stock_chart(ticker: str, window: int):
    """
    Generate a stock price chart with an SMA overlay for better trend visualization.
    """
    return stock_service.generate_chart(ticker, window)


@router.get("/signal-sma/{ticker}", summary="Generate Buy/Sell Signals with SMA Strategy")
def get_stock_signal(ticker: str):
    """
    Generate a stock price chart with SMA (short and long) overlays.
    Provides backtesting results and buy/sell signals based on strategy performance.
    """
    return stock_service.generate_signal(ticker)


@router.get("/backtest/{ticker}", summary="Backtest SMA Strategy on Stock Data")
def get_backtest_result(
    ticker: str, 
    initial_balance: int = 10_000, 
    do_trailing_StopLoss: bool = False
):
    """
    Perform backtesting on the SMA strategy for a given stock over the past year.

    - `initial_balance`: Starting capital for backtesting (default: $10,000)
    - `do_trailing_StopLoss`: Enable or disable trailing stop loss (default: False)
    """
    return stock_service.backtest_strategy(ticker, initial_balance, do_trailing_StopLoss)
