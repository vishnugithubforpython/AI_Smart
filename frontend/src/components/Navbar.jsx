import { Link } from "react-router-dom";
import { Menu } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import "./Navbar.css";

export default function Navbar({ onToggleSidebar }) {
  const { user } = useAuth();

  const initials = user?.username
    ? user.username.slice(0, 2).toUpperCase()
    : "AI";

  return (
    <header className="navbar">
      <div className="navbar__left">
        <button
          type="button"
          className="navbar__menu-btn"
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
        >
          <Menu size={20} strokeWidth={1.75} />
        </button>
        <span className="navbar__title">AI Smart</span>
      </div>
      <div className="navbar__right">
        <Link to="/dashboard" className="navbar__profile" aria-label="Profile">
          <span>{initials}</span>
        </Link>
      </div>
    </header>
  );
}
