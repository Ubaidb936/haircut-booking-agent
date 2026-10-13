import { useState, useEffect, useRef } from 'react'
import './App.css'

function getOrCreate(key) {
  const existing = localStorage.getItem(key)
  if (existing) return existing
  const value = crypto.randomUUID()
  localStorage.setItem(key, value)
  return value
}

const USER_ID = getOrCreate('haircut_user_id')

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [threadId, setThreadId] = useState(localStorage.getItem('haircut_thread_id'))
  const [loading, setLoading] = useState(false)
  const [booked, setBooked] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    startChat()
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function startChat() {
    setLoading(true)
    try {
      const res = await fetch('/start', {
        method: 'POST',
        headers: { 'x-user-id': USER_ID }
      })
      const data = await res.json()
      setThreadId(data.thread_id)
      localStorage.setItem('haircut_thread_id', data.thread_id)
      setMessages([{ role: 'agent', text: data.message }])
      if (data.booked) setBooked(true)
    } finally {
      setLoading(false)
    }
  }

  async function sendMessage() {
    if (!input.trim() || loading || booked) return
    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: userMessage }])
    setLoading(true)
    try {
      const res = await fetch('/resume', {
        method: 'POST',
        headers: {
          'x-user-id': USER_ID,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ thread_id: threadId, message: userMessage })
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'agent', text: data.message }])
      if (data.booked) setBooked(true)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Haircut Booking</h1>
      </div>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <span>{msg.text}</span>
          </div>
        ))}
        {loading && (
          <div className="message agent">
            <span className="typing">...</span>
          </div>
        )}
        {booked && (
          <div className="booked-banner">Appointment booked!</div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={booked ? 'Booking complete!' : 'Type a message...'}
          disabled={loading || booked}
          rows={1}
        />
        <button onClick={sendMessage} disabled={loading || booked || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}

export default App
