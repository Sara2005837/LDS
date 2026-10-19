import { useState } from 'react'
import './App.css'

function App() {
  const [ticker, setTicker] = useState('AAPL')
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<string[]>([
    'Hello! I am your AI Stock Analysis Assistant. Ask me about a stock, or use the buttons below to explore stock data.',
  ])
  const [loading, setLoading] = useState(false)

  async function fetchStockData(type: string) {
    const symbol = ticker.trim().toUpperCase()

    if (!symbol) {
      setMessages((previous) => [...previous, 'Please enter a stock ticker first.'])
      return
    }

    setLoading(true)

    try {
      const response = await fetch(
        `http://127.0.0.1:8888/stock/${encodeURIComponent(symbol)}${type}`,
      )
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to retrieve stock data.')
      }

      setMessages((previous) => [
        ...previous,
        `${symbol} ${type === '' ? 'Stock Price' : type === '/history' ? 'Historical Prices' : type === '/company' ? 'Company Information' : 'Financials'}:\n${JSON.stringify(data, null, 2)}`,
      ])
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        `Error: ${error instanceof Error ? error.message : 'Could not connect to the backend. Make sure your FastAPI server is running on port 8888.'}`,
      ])
    } finally {
      setLoading(false)
    }
  }


async function sendMessage() {
  const text = question.trim()
  if (!text) return

  setMessages((previous) => [...previous, `You: ${text}`])
  setQuestion('')

  try {
    const response = await fetch('http://127.0.0.1:8889/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: text }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'The AI request failed.')
    }

    const reply = Array.isArray(data.reply)
      ? data.reply
          .map((item: { text?: string }) => item.text || '')
          .filter(Boolean)
          .join('\n')
      : data.reply

    setMessages((previous) => [...previous, reply || 'The AI returned an empty response.'])
  } catch (error) {
    setMessages((previous) => [
      ...previous,
      `Sorry, I couldn't reach the AI service. ${
        error instanceof Error ? error.message : 'Please try again.'
      }`,
    ])
  }
}
  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-mark">S</div>
        <div>
          <h1>Stock Analyst AI</h1>
          <p>AI-powered market research assistant</p>
        </div>
        <div className="status"><span /> API workspace</div>
      </header>

      <section className="hero">
        <span className="eyebrow">YOUR PERSONAL MARKET RESEARCHER</span>
        <h2>Make smarter moves<br />with <span>market insights.</span></h2>
        <p>Explore stock prices, company information, historical trends, and financial statements in one place.</p>
      </section>

      <section className="workspace">
        <div className="panel stock-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">STOCK EXPLORER</span>
              <h3>Analyze a company</h3>
            </div>
            <span className="sparkle">✳</span>
          </div>

          <label htmlFor="ticker">Stock ticker</label>
          <input
            id="ticker"
            value={ticker}
            onChange={(event) => setTicker(event.target.value.toUpperCase())}
            placeholder="e.g. AAPL"
          />

          <div className="action-grid">
            <button disabled={loading} onClick={() => fetchStockData('')}>Current price <span>↗</span></button>
            <button disabled={loading} onClick={() => fetchStockData('/history')}>Price history <span>↗</span></button>
            <button disabled={loading} onClick={() => fetchStockData('/company')}>Company profile <span>↗</span></button>
            <button disabled={loading} onClick={() => fetchStockData('/financials')}>Financials <span>↗</span></button>
          </div>
          {loading && <p className="loading">Retrieving stock data...</p>}
          <p className="hint">Market data provided by Yahoo Finance through your backend.</p>
        </div>

        <div className="panel chat-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">AI ASSISTANT</span>
              <h3>Your research chat</h3>
            </div>
            <span className="online">● Online</span>
          </div>

          <div className="messages">
            {messages.map((message, index) => (
              <pre className={message.startsWith('You:') ? 'message user-message' : 'message'} key={index}>{message}</pre>
            ))}
          </div>

          <form className="chat-form" onSubmit={(event) => { event.preventDefault(); sendMessage() }}>
            <input
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask about a stock..."
              aria-label="Your question"
            />
            <button type="submit" aria-label="Send message">↑</button>
          </form>
          <p className="hint">Informational use only — not financial advice.</p>
        </div>
      </section>

      <footer>STOCK ANALYST AI <span>•</span> Built for smarter research</footer>
    </main>
  )
}

export default App
