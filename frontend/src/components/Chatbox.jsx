import { useRef, useEffect } from "react";
import Message from "./Message";
import "./Chatbox.css";

const suggestions = [
  { title: "Tell me about Vishnu", subtitle: "Search your indexed resume" },
  { title: "Summarize experience", subtitle: "Quick overview of skills" },
  { title: "What is RAG?", subtitle: "Uses web search when docs don't match" },
  { title: "Latest AI trends", subtitle: "Answers from the web when needed" },
];

export default function Chatbox({
  messages,
  loading,
  onSuggestionClick,
  onRegenerate,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  if (messages.length === 0 && !loading) {
    return (
      <div className="welcome-screen">
        <h1>How can I help you today?</h1>
        <p>
          Ask about your resume and documents, or general questions — the
          assistant uses your files first and searches the web when needed.
        </p>
        <div className="suggestion-grid">
          {suggestions.map((item) => (
            <button
              key={item.title}
              type="button"
              className="suggestion-card"
              onClick={() => onSuggestionClick(item.title)}
            >
              <span>{item.title}</span>
              <small>{item.subtitle}</small>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="messages-container">
      {messages.map((msg, index) => (
        <Message
          key={msg.id}
          role={msg.role}
          content={msg.content}
          sources={msg.sources}
          sourceType={msg.sourceType}
          onRegenerate={
            msg.role === "assistant" && index === messages.length - 1 && !loading
              ? () => onRegenerate(index)
              : undefined
          }
        />
      ))}

      {loading && (
        <div className="message message--assistant">
          <div className="typing-indicator">
            <span />
            <span />
            <span />
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
