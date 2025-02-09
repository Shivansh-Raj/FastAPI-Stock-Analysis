from fastapi import FastAPI
from .routes import stock_routes

app = FastAPI(title="Stock Analysis API", description="API to analyze stock prices using moving averages")


@app.get("/", tags = ["HOME URL"])
def home():
    return {
        "message": "Welcome to the Stock Analysis API! 🚀",
        "usage": "Visit the Swagger UI at /docs to explore available endpoints.",
        "instructions": "Use NASDAQ ticker symbols (e.g., AAPL, TSLA) as input to fetch stock data and analyze trends.",
        "example": "Try GET /data?ticker=AAPL to retrieve historical stock data."
    }


app.include_router(stock_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

