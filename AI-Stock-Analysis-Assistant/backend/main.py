
import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from stock_tools import (
    get_stock_price,
    get_historical_prices,
    get_company_info,
    get_financials,
)

load_dotenv(Path(__file__).parent / ".env")

app = FastAPI(
    title="AI Stock Analysis Assistant",
    description="AI-powered stock analysis assistant",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@tool
def stock_price(ticker: str) -> dict:
    """Get the latest available daily closing price for a stock ticker."""
    return get_stock_price(ticker.upper())


@tool
def stock_history(ticker: str, period: str = "1mo") -> dict:
    """Get historical stock prices. Period can be 5d, 1mo, 3mo, 6mo, 1y, or 5y."""
    return get_historical_prices(ticker.upper(), period)


@tool
def company_info(ticker: str) -> dict:
    """Get a company's name, sector, industry, and other available details."""
    return get_company_info(ticker.upper())


@tool
def financials(ticker: str) -> dict:
    """Get a company's available income statement and balance sheet data."""
    return get_financials(ticker.upper())


tools = [stock_price, stock_history, company_info, financials]
tools_by_name = {item.name: item for item in tools}


def make_model():
    key = __import__("os").getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing from backend/.env")

    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=key,
        temperature=0,
    ).bind_tools(tools)


@app.get("/")
def home():
    return {"message": "AI Stock Analysis Assistant API is running!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/stock/{ticker}")
def stock_price_endpoint(ticker: str):
    result = get_stock_price(ticker.upper())
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/stock/{ticker}/history")
def historical_prices_endpoint(ticker: str, period: str = "1mo"):
    result = get_historical_prices(ticker.upper(), period)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/stock/{ticker}/company")
def company_info_endpoint(ticker: str):
    result = get_company_info(ticker.upper())
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/stock/{ticker}/financials")
def stock_financials_endpoint(ticker: str):
    result = get_financials(ticker.upper())
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.post("/api/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Please enter a message.")

    try:
        model = make_model()
        messages = [
            HumanMessage(
                content=(
                    "You are an AI stock analysis assistant. Use the provided "
                    "stock tools when current or company-specific data is needed. "
                    "Explain results clearly, distinguish historical data from "
                    "live prices, and do not present financial information as "
                    "personalized investment advice.\n\n"
                    f"User question: {request.message}"
                )
            )
        ]

        for _ in range(5):
            response = model.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                return {"reply": response.content}

            for call in response.tool_calls:
                result = tools_by_name[call["name"]].invoke(call["args"])
                messages.append(
                    ToolMessage(
                        content=json.dumps(result, default=str),
                        tool_call_id=call["id"],
                    )
                )

        return {"reply": "I couldn't finish that analysis in one attempt. Please try a more specific question."}

    except Exception as exc:
        print(f"Chat endpoint error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="The AI request failed. Check the backend Terminal for details.",
        )
