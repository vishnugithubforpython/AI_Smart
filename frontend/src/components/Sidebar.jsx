import { Link, useNavigate } from "react-router-dom";
import { Plus, FileText, User, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import "./Sidebar.css";

export default function Sidebar({ onNewChat, collapsed, onToggle }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

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
        <div className="sidebar__body">
          <Link to="/chat" className="sidebar__brand">
            <span className="sidebar__brand-icon">AI</span>
            <span className="sidebar__brand-name">AI Smart</span>
          </Link>

          <nav className="sidebar__nav">
            <button
              type="button"
              className="sidebar__nav-item"
              onClick={onNewChat}
            >
              <Plus size={18} strokeWidth={1.75} />
              <span>New Chat</span>
            </button>

            <button
              type="button"
              className="sidebar__nav-item sidebar__nav-item--disabled"
              disabled
              title="Coming soon"
            >
              <FileText size={18} strokeWidth={1.75} />
              <span>My Documents</span>
            </button>

            <Link to="/dashboard" className="sidebar__nav-item">
              <User size={18} strokeWidth={1.75} />
              <span>Profile</span>
            </Link>
          </nav>
        </div>

        <div className="sidebar__footer">
          <button
            type="button"
            className="sidebar__logout"
            onClick={handleLogout}
          >
            <LogOut size={18} strokeWidth={1.75} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
}
