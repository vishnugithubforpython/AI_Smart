import { useState } from "react";
import {
  ThumbsUp,
  ThumbsDown,
  Copy,
  RotateCcw,
  MoreHorizontal,
  Check,
} from "lucide-react";
import "./Message.css";

function CodeBlock({ language, code }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="code-block">
      <div className="code-block__header">
        <span>{language || "code"}</span>
        <button type="button" onClick={handleCopy} aria-label="Copy code">
          {copied ? <Check size={14} /> : <Copy size={14} />}
          <span>{copied ? "Copied" : "Copy"}</span>
        </button>
      </div>
      <pre>
        <code>{code}</code>
      </pre>
    </div>
  );
}

function renderContent(content) {
  const text = typeof content === "string" ? content : String(content ?? "");

  if (!text.trim()) {
    return <p className="message__text message__text--empty">No response.</p>;
  }

  const parts = text.split(/(```[\s\S]*?```)/g);

  return parts.map((part, index) => {
    if (part.startsWith("```")) {
      const match = part.match(/```(\w*)\n?([\s\S]*?)```/);
      if (match) {
        return (
          <CodeBlock key={index} language={match[1]} code={match[2].trim()} />
        );
      }
    }

    const lines = part.split("\n");
    return (
      <div key={index} className="message__text">
        {lines.map((line, lineIndex) => {
          if (line.trim().startsWith("- ") || line.trim().startsWith("* ")) {
            return (
              <p key={lineIndex} className="message__list-item">
                {line.replace(/^[\s-*]+/, "")}
              </p>
            );
          }
          if (/^\d+\.\s/.test(line.trim())) {
            return (
              <p key={lineIndex} className="message__numbered-item">
                {line}
              </p>
            );
          }
          if (line.trim() === "") {
            return <br key={lineIndex} />;
          }
          return <p key={lineIndex}>{line}</p>;
        })}
      </div>
    );
  });
}

function sourceLabel(sourcePath) {
  if (!sourcePath) return "Document";
  const parts = sourcePath.replace(/\\/g, "/").split("/");
  return parts[parts.length - 1] || sourcePath;
}

function uniqueSources(sources) {
  const seen = new Set();
  return sources.filter((item) => {
    const key = item.source || item.text?.slice(0, 80);
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export default function Message({
  role,
  content,
  sources = [],
  sourceType,
  onRegenerate,
}) {
  const [copied, setCopied] = useState(false);
  const isUser = role === "user";

  const handleCopy = async () => {
    await navigator.clipboard.writeText(
      typeof content === "string" ? content : String(content ?? "")
    );
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isUser) {
    return (
      <div className="message message--user">
        <div className="message__bubble">{content}</div>
      </div>
    );
  }

  return (
    <div className="message message--assistant">
      {sourceType && sourceType !== "error" && (
        <div className="message__source-badge">
          {sourceType === "document" ? "From your documents" : "From web search"}
        </div>
      )}
      <div className="message__content">{renderContent(content)}</div>
      {sources.length > 0 && (
        <details className="message__sources">
          <summary>Sources ({uniqueSources(sources).length})</summary>
          <ul>
            {uniqueSources(sources).map((item, index) => (
              <li key={`${item.source}-${index}`}>
                <span className="message__source-name">
                  {sourceLabel(item.source)}
                </span>
                {item.rerank_score != null && (
                  <span className="message__source-score">
                    relevance {item.rerank_score.toFixed(2)}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </details>
      )}
      <div className="message__actions">
        <button type="button" aria-label="Good response">
          <ThumbsUp size={16} strokeWidth={1.75} />
        </button>
        <button type="button" aria-label="Bad response">
          <ThumbsDown size={16} strokeWidth={1.75} />
        </button>
        <button type="button" onClick={handleCopy} aria-label="Copy">
          {copied ? (
            <Check size={16} strokeWidth={1.75} />
          ) : (
            <Copy size={16} strokeWidth={1.75} />
          )}
        </button>
        {onRegenerate && (
          <button type="button" onClick={onRegenerate} aria-label="Regenerate">
            <RotateCcw size={16} strokeWidth={1.75} />
          </button>
        )}
        <button type="button" aria-label="More">
          <MoreHorizontal size={16} strokeWidth={1.75} />
        </button>
      </div>
    </div>
  );
}
