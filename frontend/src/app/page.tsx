"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "bot";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", content: "Hello! I'm your Discord RAG Assistant. I can help you understand the project documentation and answer technical questions. How can I assist you today?" },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: "web-user", query: userMsg }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages((prev) => [...prev, { role: "bot", content: data.answer }]);
      } else {
        setMessages((prev) => [...prev, { role: "bot", content: "Error: Unable to reach the backend service. Make sure the FastAPI server is running." }]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { role: "bot", content: "Error: Connection failed. Please check your local network." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="main-container">
      {/* Sidebar for Showcase Info */}
      <aside className="sidebar">
        <div>
          <div className="logo" style={{ marginBottom: '40px' }}>Discord RAG</div>
          
          <section style={{ marginBottom: '30px' }}>
            <h2>Project Overview</h2>
            <p style={{ fontSize: '14px', opacity: 0.7, lineHeight: '1.6', marginTop: '10px' }}>
              A state-of-the-art Retrieval-Augmented Generation system designed for Discord integration.
            </p>
          </section>

          <section style={{ marginBottom: '30px' }}>
            <h2>Technologies</h2>
            <div style={{ marginTop: '10px' }}>
              <span className="feature-tag">FastAPI</span>
              <span className="feature-tag">MongoDB Atlas</span>
              <span className="feature-tag">Gemini Pro</span>
              <span className="feature-tag">Discord.py</span>
              <span className="feature-tag">Next.js</span>
              <span className="feature-tag">Vector Search</span>
            </div>
          </section>

          <section>
            <h2>Core Features</h2>
            <ul style={{ fontSize: '13px', opacity: 0.7, paddingLeft: '20px', marginTop: '10px' }}>
              <li>Semantic Document Retrieval</li>
              <li>Real-time Chat via Discord</li>
              <li>Web-based Admin Dashboard</li>
              <li>Feedback-driven Optimization</li>
            </ul>
          </section>
        </div>

        <div style={{ marginTop: 'auto', fontSize: '12px', opacity: 0.4 }}>
          v1.0.0 Build • 2026
        </div>
      </aside>

      {/* Main Chat Section */}
      <div className="chat-section">
        <header className="header">
          <div>
            <h1 style={{ fontSize: '18px', fontWeight: '700', margin: 0 }}>Interactive Showcase</h1>
            <p style={{ fontSize: '13px', opacity: 0.5 }}>Test the RAG engine in real-time</p>
          </div>
          <div className="status-badge">
            <span style={{ width: '8px', height: '8px', background: '#43b581', borderRadius: '50%' }}></span>
            System Online
          </div>
        </header>

        <main className="chat-window">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}-message`}>
              {msg.content}
            </div>
          ))}
          {isLoading && (
            <div className="message bot-message" style={{ opacity: 0.6 }}>
              <span className="typing-indicator">Analyzing knowledge base...</span>
            </div>
          )}
          <div ref={chatEndRef} />
        </main>

        <div className="input-area">
          <input
            type="text"
            placeholder="Ask anything about the project documents..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
          />
          <button onClick={handleSend} disabled={isLoading}>
            {isLoading ? "Processing..." : "Send Query"}
          </button>
        </div>
      </div>
    </div>
  );
}
