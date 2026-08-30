import {
  Search,
  Sun,
  Moon,
  Bell,
  Mic,
  Globe,
  ChevronDown,
} from "lucide-react";

import { useTheme } from "../../context/ThemeContext";

function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="navbar">

      {/* Search */}

      <div className="navbar-search">
        <Search size={18} />

        <input
          type="text"
          placeholder="Search AgriSphere..."
        />

        <span className="search-shortcut">
          Ctrl K
        </span>
      </div>

      {/* Actions */}

      <div className="navbar-actions">

        {/* Language */}

        <button className="navbar-action language-button">
          <Globe size={18} />

          <span>English</span>

          <ChevronDown size={15} />
        </button>

        {/* Voice */}

        <button
          className="navbar-icon-button voice-button"
          title="Voice Assistant"
        >
          <Mic size={19} />
        </button>

        {/* Theme */}

        <button
          className="navbar-icon-button"
          onClick={toggleTheme}
          title="Toggle theme"
        >
          {theme === "light" ? (
            <Moon size={19} />
          ) : (
            <Sun size={19} />
          )}
        </button>

        {/* Notifications */}

        <button
          className="navbar-icon-button notification-button"
          title="Notifications"
        >
          <Bell size={19} />

          <span className="notification-dot">
            3
          </span>
        </button>

        {/* Profile */}

        <button className="navbar-profile">

          <div className="profile-avatar">
            K
          </div>

          <div className="profile-info">
            <strong>Farmer</strong>
            <span>AgriSphere User</span>
          </div>

          <ChevronDown size={15} />

        </button>

      </div>

    </header>
  );
}

export default Navbar;