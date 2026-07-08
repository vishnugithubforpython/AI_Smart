import { ChevronDown, Share2, Menu, Folder } from "lucide-react";
import "./Navbar.css";

export default function Navbar({ onToggleSidebar }) {
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
        <button type="button" className="navbar__breadcrumb">
          <Folder size={16} strokeWidth={1.75} />
          <span>AI Smart</span>
          <ChevronDown size={16} strokeWidth={1.75} />
        </button>
      </div>
      <div className="navbar__right">
        <button type="button" className="navbar__icon-btn" aria-label="Share">
          <Share2 size={18} strokeWidth={1.75} />
        </button>
        <button type="button" className="navbar__profile" aria-label="Profile">
          <span>AI</span>
        </button>
      </div>
    </header>
  );
}
