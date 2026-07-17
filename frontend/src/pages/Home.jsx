import { useState, useCallback, useRef } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import Chatbox from "../components/Chatbox";
import ChatInput from "../components/ChatInput";
import { askQuestion, extractErrorMessage } from "../services/api";

let chatIdCounter = 1;
let messageIdCounter = 1;

function createChat(title = "New chat") {
  chatIdCounter += 1;
  return {
    id: String(chatIdCounter),
    title,
    messages: [],
  };
}

function createMessage(role, content, meta = {}) {
  messageIdCounter += 1;
  return { id: String(messageIdCounter), role, content, ...meta };
}

let initialHomeState = null;

function getInitialHomeState() {
  if (!initialHomeState) {
    const chat = createChat();
    initialHomeState = { chats: [chat], activeChatId: chat.id };
  }
  return initialHomeState;
}

export default function Home() {
  const [chats, setChats] = useState(() => getInitialHomeState().chats);
  const [activeChatId, setActiveChatId] = useState(
    () => getInitialHomeState().activeChatId
  );
  const [loading, setLoading] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(
    window.innerWidth <= 768
  );

  const activeChatIdRef = useRef(activeChatId);
  activeChatIdRef.current = activeChatId;

  const activeChat = chats.find((c) => c.id === activeChatId) ?? chats[0];

  const appendToChat = useCallback((chatId, updater) => {
    setChats((prev) => {
      const targetId = prev.some((c) => c.id === chatId)
        ? chatId
        : prev[0]?.id;
      if (!targetId) return prev;

      return prev.map((chat) =>
        chat.id === targetId ? updater(chat) : chat
      );
    });
  }, []);

  const handleNewChat = () => {
    const chat = createChat();
    setChats((prev) => [chat, ...prev]);
    setActiveChatId(chat.id);
    if (window.innerWidth <= 768) {
      setSidebarCollapsed(true);
    }
  };

  const handleUserMessage = useCallback(
    (question) => {
      const chatId = activeChatIdRef.current;

      appendToChat(chatId, (chat) => {
        const userMsg = createMessage("user", question);
        const isFirstMessage = chat.messages.length === 0;
        const title = isFirstMessage
          ? question.slice(0, 30) + (question.length > 30 ? "…" : "")
          : chat.title;

        return {
          ...chat,
          title,
          messages: [...chat.messages, userMsg],
        };
      });

      setLoading(true);
    },
    [appendToChat]
  );

  const handleAssistantMessage = useCallback(
    ({ answer, sources, sourceType }) => {
      const chatId = activeChatIdRef.current;
      const assistantMsg = createMessage("assistant", answer, {
        sources,
        sourceType,
      });

      appendToChat(chatId, (chat) => ({
        ...chat,
        messages: [...chat.messages, assistantMsg],
      }));

      setLoading(false);
    },
    [appendToChat]
  );

  const handleError = useCallback((err) => {
    const chatId = activeChatIdRef.current;
    const errorMsg = createMessage(
      "assistant",
      err ? extractErrorMessage(err) : "Something went wrong. Please try again.",
      { sourceType: "error" }
    );

    appendToChat(chatId, (chat) => ({
      ...chat,
      messages: [...chat.messages, errorMsg],
    }));

    setLoading(false);
  }, [appendToChat]);

  const handleSuggestionClick = (text) => {
    handleUserMessage(text);

    askQuestion(text)
      .then(({ answer, sources, sourceType }) => {
        handleAssistantMessage({ answer, sources, sourceType });
      })
      .catch((err) => {
        handleError(err);
      });
  };

  const handleRegenerate = async (assistantIndex) => {
    const messages = activeChat.messages;
    const userMsg = messages[assistantIndex - 1];
    if (!userMsg || userMsg.role !== "user") return;

    const chatId = activeChatIdRef.current;

    appendToChat(chatId, (chat) => ({
      ...chat,
      messages: chat.messages.slice(0, assistantIndex),
    }));

    setLoading(true);

    try {
      const { answer, sources, sourceType } = await askQuestion(userMsg.content);
      handleAssistantMessage({ answer, sources, sourceType });
    } catch (err) {
      handleError(err);
    }
  };

  return (
    <div className="app">
      <Sidebar
        onNewChat={handleNewChat}
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed((prev) => !prev)}
      />

      <div className="main-area">
        <Navbar onToggleSidebar={() => setSidebarCollapsed((prev) => !prev)} />

        <div className="chat-viewport">
          <Chatbox
            messages={activeChat.messages}
            loading={loading}
            onSuggestionClick={handleSuggestionClick}
            onRegenerate={handleRegenerate}
          />
        </div>

        <div className="input-area">
          <div className="input-area-inner">
            <ChatInput
              onUserMessage={handleUserMessage}
              onAssistantMessage={handleAssistantMessage}
              onError={handleError}
              disabled={loading}
            />
            <p className="input-disclaimer">
              AI Smart searches your documents first, then the web. It can make
              mistakes — check important info.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
