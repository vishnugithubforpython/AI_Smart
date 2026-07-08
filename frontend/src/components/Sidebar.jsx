import {
  Plus,
  Search,
  Library,
  Clock,
  LayoutGrid,
  Code2,
  MoreHorizontal,
  MessageSquare,
  Folder,
  HelpCircle,
} from "lucide-react";
import "./Sidebar.css";

const navItems = [
  { icon: Plus, label: "New chat", action: "new" },
  { icon: Search, label: "Search chats" },
  { icon: Library, label: "Library" },
  { icon: Clock, label: "Scheduled" },
  { icon: LayoutGrid, label: "Apps" },
  { icon: Code2, label: "Codex" },
  { icon: MoreHorizontal, label: "More" },
];

const projects = ["geni ai", "dsa", "DSA", "inidan army", "data science"];

export default function Sidebar({
  chats,
  activeChatId,
  onNewChat,
  onSelectChat,
  collapsed,
  onToggle,
}) {
  return (
    <>
      {collapsed && (
        <button
          type="button"
          className="sidebar-overlay"
          onClick={onToggle}
          aria-label="Close sidebar"
        />
      )}
      <aside className={`sidebar ${collapsed ? "sidebar--collapsed" : ""}`}>
        <div className="sidebar__top">
          <div className="sidebar__logo">
            <div className="sidebar__logo-icon">
              <MessageSquare size={18} strokeWidth={1.75} />
            </div>
          </div>

          <nav className="sidebar__nav">
            {navItems.map(({ icon: Icon, label, action }) => (
              <button
                key={label}
                type="button"
                className="sidebar__nav-item"
                onClick={action === "new" ? onNewChat : undefined}
              >
                <Icon size={18} strokeWidth={1.75} />
                <span>{label}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="sidebar__section">
          <p className="sidebar__section-title">Pinned</p>
          <ul className="sidebar__chat-list">
            {chats.map((chat) => (
              <li key={chat.id}>
                <button
                  type="button"
                  className={`sidebar__chat-item ${
                    chat.id === activeChatId ? "sidebar__chat-item--active" : ""
                  }`}
                  onClick={() => onSelectChat(chat.id)}
                >
                  <Folder size={16} strokeWidth={1.75} />
                  <span>{chat.title}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="sidebar__section sidebar__section--projects">
          <p className="sidebar__section-title">Projects</p>
          <ul className="sidebar__project-list">
            {projects.map((project) => (
              <li key={project}>
                <button type="button" className="sidebar__project-item">
                  <Folder size={16} strokeWidth={1.75} />
                  <span>{project}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="sidebar__footer">
          <button type="button" className="sidebar__user">
            <span className="sidebar__avatar">AI</span>
            <span className="sidebar__username">AI Smart</span>
          </button>
          <button type="button" className="sidebar__help" aria-label="Help">
            <HelpCircle size={18} strokeWidth={1.75} />
          </button>
        </div>
      </aside>
    </>
  );
}
