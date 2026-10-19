# AI Stock Analysis Assistant

## Project Overview

The AI Stock Analysis Assistant is a web application that combines artificial intelligence with stock market data to help users explore companies and understand stock information through a conversational interface.

The project was developed as an educational project to demonstrate how AI models, APIs, backend services, and a modern web frontend can work together.

## Features

- Ask stock-related questions in natural language.
- Retrieve the latest available daily closing price for a stock.
- Explore historical stock prices.
- View company profiles and business information.
- Retrieve available financial statements.
- Use an interactive web dashboard to explore stock information.

## Technologies Used

### Frontend
- React
- TypeScript
- Vite
- CSS

### Backend
- Python
- FastAPI
- yfinance for stock market data

### Artificial Intelligence
- Google Gemini
- LangChain
- LangChain Google GenAI integration

## Why We Chose Gemini

We chose Google Gemini as the AI model because the project needs a language model that can understand natural-language questions and provide clear, conversational explanations about stock market information.

Gemini integrates with our Python backend through LangChain, allowing the application to connect the language model with custom stock-data tools. This means the assistant can retrieve company-specific information when needed and use the returned data to help answer a user's question.

We also considered the project's cost and accessibility. Our initial attempt to use the Thesys service encountered an insufficient-balance error, and we wanted to avoid adding paid service costs to an educational project. Gemini was successfully tested with our application, making it a practical alternative for development.

Using Gemini demonstrates how a language model can be combined with external data tools rather than relying only on information learned during training.

## How the AI Assistant Works

1. A user enters a question in the React frontend.
2. The frontend sends the question to the FastAPI backend.
3. The backend passes the question to Gemini through LangChain.
4. When needed, Gemini can request one of the available stock-data tools.
5. The backend executes the tool and returns its result to the model.
6. Gemini uses the result to formulate a response.
7. The response is displayed in the web interface.

Available tools retrieve stock prices, historical prices, company information, and financial statements.

## Requirements

- Python 3.12 or a compatible version
- Node.js and npm
- A Google Gemini API key

## Configuration

Create a file named `.env` inside the `backend` directory and add:

    GEMINI_API_KEY=your_gemini_api_key_here

Replace the placeholder with your own API key. Never commit a real API key or `.env` file to GitHub.

## How to Run the Backend

From the project directory:

    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install fastapi uvicorn yfinance python-dotenv langchain-core langchain-google-genai
    uvicorn main:app --reload --port 8889

Keep the backend Terminal window open.

## How to Run the Frontend

Open a second Terminal window and run:

    cd frontend
    npm install
    npm run dev

Open the local address shown by Vite, usually:

    http://localhost:5173

## Data Sources and Limitations

Stock market data is retrieved from Yahoo Finance through the yfinance Python library. The displayed price represents the latest available daily closing price and may not be a real-time quote.

AI-generated responses may contain mistakes and should be checked against reliable sources. This project is intended for educational and informational use only and does not provide personalized investment advice.

## Future Improvements

- Add stock price charts and visualizations.
- Improve error handling and loading indicators.
- Add more financial metrics and company comparisons.
- Deploy the application so it can be accessed online.
