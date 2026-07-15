import { useRef, useState } from "react";
import { Mic, ArrowUp } from "lucide-react";
import { askQuestion, uploadFile } from "../services/api";
import Upload from "./Upload";
import "./ChatInput.css";

export default function ChatInput({ onUserMessage, onAssistantMessage, onError, disabled }) {
  const [value, setValue] = useState("");
  const [sending, setSending] = useState(false);
  const [uploading, setUploading] = useState(false);
  const textareaRef = useRef(null);

  const isBusy = disabled || sending || uploading;

  const handleInput = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  };

  const sendQuestion = async (question) => {
    const text = question.trim();
    if (!text || isBusy) return;

    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }

    onUserMessage(text);
    setSending(true);

    try {
      const { answer, sources, sourceType } = await askQuestion(text);
      onAssistantMessage({ answer, sources, sourceType });
    } catch {
      onError();
    } finally {
      setSending(false);
    }
  };

  const handleSend = () => sendQuestion(value);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !isBusy) {
        handleSend();
      }
    }
  };

  const handleFileSelect = async (file) => {
    if (isBusy) return;

    onUserMessage(`Uploaded: ${file.name}`);
    setUploading(true);

    try {
      const result = await uploadFile(file);
      onAssistantMessage({
        answer: result.message ?? `${file.name} uploaded successfully.`,
        sources: [],
        sourceType: "upload",
      });
    } catch (err) {
      onAssistantMessage({
        answer: err.message ?? "Upload failed. Please try again.",
        sources: [],
        sourceType: "error",
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="chat-input">
      <div className="chat-input__wrapper">
        <Upload
          onFileSelect={handleFileSelect}
          disabled={disabled || sending}
          uploading={uploading}
        />
        <textarea
          ref={textareaRef}
          className="chat-input__field"
          placeholder="Ask anything"
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            handleInput();
          }}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={isBusy}
        />
        <div className="chat-input__actions">
          <button type="button" className="chat-input__mic" aria-label="Voice input">
            <Mic size={20} strokeWidth={1.75} />
          </button>
          <button
            type="button"
            className={`chat-input__send ${value.trim() ? "chat-input__send--active" : ""}`}
            onClick={handleSend}
            disabled={!value.trim() || isBusy}
            aria-label="Send message"
          >
            <ArrowUp size={18} strokeWidth={2} />
          </button>
        </div>
      </div>
    </div>
  );
}
