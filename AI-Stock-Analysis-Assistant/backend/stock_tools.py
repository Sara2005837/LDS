import yfinance as yf


def get_stock_price(ticker: str) -> dict:
    """Get the latest available price for a stock ticker, such as AAPL."""

    ticker = ticker.strip().upper()

    if not ticker:
        return {"error": "Please provide a stock ticker."}

    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="5d")

        if history.empty:
            return {
                "ticker": ticker,
                "error": "No recent price data found. Check the ticker symbol."
            }

        latest = history.dropna(subset=["Close"]).iloc[-1]

        return {
            "ticker": ticker,
            "date": str(history.dropna(subset=["Close"]).index[-1].date()),
            "price": round(float(latest["Close"]), 2),
            "currency": stock.fast_info.get("currency", "Unknown"),
            "source": "Yahoo Finance via yfinance",
            "note": "Latest available daily closing price; may not be real-time."
        }

    except Exception as exc:
        return {
            "ticker": ticker,
            "error": f"Could not retrieve stock data: {exc}"
        }


def get_historical_prices(ticker: str, period: str = "1mo") -> dict:
    """Get historical daily closing prices."""

    ticker = ticker.strip().upper()

    allowed_periods = {
        "5d", "1mo", "3mo", "6mo",
        "1y", "2y", "5y", "10y", "ytd", "max"
    }

    if not ticker:
        return {"error": "Please provide a stock ticker."}

    if period not in allowed_periods:
        return {"error": "Invalid period. Try 5d, 1mo, 3mo, 6mo, or 1y."}

    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)

        if history.empty:
            return {
                "ticker": ticker,
                "error": "No historical data found. Check the ticker symbol."
            }

        prices = []

        for date, row in history.iterrows():
            if row["Close"] == row["Close"]:
                prices.append({
                    "date": str(date.date()),
                    "close": round(float(row["Close"]), 2)
                })

        return {
            "ticker": ticker,
            "period": period,
            "currency": stock.fast_info.get("currency", "Unknown"),
            "prices": prices,
            "source": "Yahoo Finance via yfinance"
        }

    except Exception as exc:
        return {
            "ticker": ticker,
            "error": f"Could not retrieve historical data: {exc}"
        }

def get_company_info(ticker: str) -> dict:
    """Get basic company information."""

    ticker = ticker.strip().upper()

    if not ticker:
        return {"error": "Please provide a stock ticker."}

    try:
        stock = yf.Ticker(ticker)
        info = stock.get_info()

        company_name = info.get("longName") or info.get("shortName")

        if not company_name:
            return {
                "ticker": ticker,
                "error": "No company information found. Check the ticker symbol."
            }

        return {
            "ticker": ticker,
            "company_name": company_name,
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "website": info.get("website"),
            "country": info.get("country"),
            "currency": info.get("currency"),
            "source": "Yahoo Finance via yfinance"
        }

    except Exception as exc:
        return {
            "ticker": ticker,
            "error": f"Could not retrieve company information: {exc}"
        }

def get_financials(ticker: str) -> dict:
    """Get annual and quarterly financial statements."""

    ticker = ticker.strip().upper()

    if not ticker:
        return {"error": "Please provide a stock ticker."}

    try:
        stock = yf.Ticker(ticker)

        annual = stock.financials
        quarterly = stock.quarterly_financials
        balance = stock.balance_sheet

        if annual.empty and quarterly.empty and balance.empty:
            return {
                "ticker": ticker,
                "error": "No financial statements found for this ticker."
            }

        def statement_to_dict(statement):
            result = {}

            if statement.empty:
                return result

            for date in statement.columns:
                result[str(date.date())] = {
                    str(metric): (
                        float(value) if value == value else None
                    )
                    for metric, value in statement[date].items()
                }

            return result

        return {
            "ticker": ticker,
            "annual_income_statement": statement_to_dict(annual),
            "quarterly_income_statement": statement_to_dict(quarterly),
            "balance_sheet": statement_to_dict(balance),
            "currency": stock.fast_info.get("currency", "Unknown"),
            "source": "Yahoo Finance via yfinance"
        }

    except Exception as exc:
        return {
            "ticker": ticker,
            "error": f"Could not retrieve financial data: {exc}"
        }

if __name__ == "__main__":
    print(get_stock_price("AAPL"))
