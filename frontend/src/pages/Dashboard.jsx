import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { extractErrorMessage } from "../services/api";
import "./Auth.css";

export default function Dashboard() {
  const { user, loadUser, logout } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(!user);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadProfile() {
      setLoading(true);
      setError("");
      try {
        await loadUser();
      } catch (err) {
        if (!cancelled) {
          setError(extractErrorMessage(err));
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadProfile();
    return () => {
      cancelled = true;
    };
  }, [loadUser]);

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div className="dashboard-header__brand">
          <div className="auth-card__logo-icon">AI</div>
          <span>AI Smart</span>
        </div>
        <div className="dashboard-header__actions">
          <Link to="/chat" className="dashboard-nav-btn dashboard-nav-btn--primary">
            Open Chat
          </Link>
          <button type="button" className="dashboard-nav-btn dashboard-nav-btn--danger" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        {loading ? (
          <div className="dashboard-loading">
            <Loader2 size={32} strokeWidth={1.75} className="auth-spinner" />
          </div>
        ) : error ? (
          <div className="auth-error">{error}</div>
        ) : user ? (
          <>
            <h1>Welcome, {user.username}</h1>
            <p className="dashboard-content__subtitle">
              Your account details are shown below.
            </p>

            <div className="dashboard-profile">
              <div className="dashboard-profile__row">
                <span className="dashboard-profile__label">Username</span>
                <span className="dashboard-profile__value">{user.username}</span>
              </div>
              <div className="dashboard-profile__row">
                <span className="dashboard-profile__label">Email</span>
                <span className="dashboard-profile__value">{user.email}</span>
              </div>
              <div className="dashboard-profile__row">
                <span className="dashboard-profile__label">Role</span>
                <span className="dashboard-profile__role">{user.role}</span>
              </div>
            </div>
          </>
        ) : null}
      </main>
    </div>
  );
}
