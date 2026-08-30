import { useEffect, useState } from "react";

import {
  Settings as SettingsIcon,
  Sun,
  Moon,
  Monitor,
  Bell,
  Globe,
  LayoutDashboard,
  Save,
  RotateCcw,
  CheckCircle2,
  Palette,
} from "lucide-react";

function Settings() {

  const [theme, setTheme] =
    useState("system");

  const [notifications, setNotifications] =
    useState(true);

  const [language, setLanguage] =
    useState("English");

  const [compactMode, setCompactMode] =
    useState(false);

  const [saved, setSaved] =
    useState(false);


  /* =====================================================
     LOAD SETTINGS
  ===================================================== */

  useEffect(() => {

    try {

      const storedSettings =
        localStorage.getItem(
          "agrisphere_settings"
        );

      if (!storedSettings) {
        return;
      }

      const settings =
        JSON.parse(storedSettings);

      setTheme(
        settings.theme || "system"
      );

      setNotifications(
        settings.notifications !== false
      );

      setLanguage(
        settings.language || "English"
      );

      setCompactMode(
        settings.compactMode || false
      );

    } catch (error) {

      console.error(
        "Unable to load settings:",
        error
      );

    }

  }, []);


  /* =====================================================
     APPLY THEME
  ===================================================== */

  useEffect(() => {

    const root =
      document.documentElement;

    if (theme === "dark") {

      root.setAttribute(
        "data-theme",
        "dark"
      );

    } else if (theme === "light") {

      root.setAttribute(
        "data-theme",
        "light"
      );

    } else {

      root.removeAttribute(
        "data-theme"
      );

    }

  }, [theme]);


  /* =====================================================
     SAVE SETTINGS
  ===================================================== */

  const saveSettings = () => {

    const settings = {

      theme,

      notifications,

      language,

      compactMode,

    };

    localStorage.setItem(
      "agrisphere_settings",
      JSON.stringify(settings)
    );


    document.documentElement.classList.toggle(
      "compact-mode",
      compactMode
    );


    setSaved(true);


    setTimeout(() => {

      setSaved(false);

    }, 2500);

  };


  /* =====================================================
     RESET
  ===================================================== */

  const resetSettings = () => {

    setTheme("system");

    setNotifications(true);

    setLanguage("English");

    setCompactMode(false);


    localStorage.removeItem(
      "agrisphere_settings"
    );


    document.documentElement.removeAttribute(
      "data-theme"
    );

    document.documentElement.classList.remove(
      "compact-mode"
    );


    setSaved(false);

  };


  return (

    <div className="settings-page agent-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <SettingsIcon size={14} />

            SETTINGS

          </div>


          <h1>
            Make AgriSphere yours
          </h1>


          <p>
            Customize the appearance and
            behaviour of your AgriSphere
            experience.
          </p>

        </div>


        <div className="agent-header-icon">

          <SettingsIcon size={31} />

        </div>

      </section>


      {/* =================================================
          SETTINGS CONTENT
      ================================================= */}

      <div className="settings-container">


        {/* =================================================
            APPEARANCE
        ================================================= */}

        <section className="settings-card">

          <div className="settings-card-header">

            <div className="settings-section-icon">

              <Palette size={17} />

            </div>


            <div>

              <h2>
                Appearance
              </h2>

              <p>
                Choose how AgriSphere looks.
              </p>

            </div>

          </div>


          <div className="theme-options">


            {/* LIGHT */}

            <ThemeOption
              icon={<Sun size={19} />}
              title="Light"
              description="Bright and clean"
              value="light"
              selected={theme === "light"}
              onClick={() =>
                setTheme("light")
              }
            />


            {/* DARK */}

            <ThemeOption
              icon={<Moon size={19} />}
              title="Dark"
              description="Easy on the eyes"
              value="dark"
              selected={theme === "dark"}
              onClick={() =>
                setTheme("dark")
              }
            />


            {/* SYSTEM */}

            <ThemeOption
              icon={<Monitor size={19} />}
              title="System"
              description="Follow device"
              value="system"
              selected={theme === "system"}
              onClick={() =>
                setTheme("system")
              }
            />

          </div>

        </section>


        {/* =================================================
            NOTIFICATIONS
        ================================================= */}

        <section className="settings-card">

          <div className="settings-row">

            <div className="settings-row-icon">

              <Bell size={17} />

            </div>


            <div className="settings-row-content">

              <h3>
                Notifications
              </h3>

              <p>
                Receive alerts about climate,
                crop health, market changes
                and important recommendations.
              </p>

            </div>


            <Toggle
              enabled={notifications}
              onClick={() =>
                setNotifications(
                  !notifications
                )
              }
            />

          </div>

        </section>


        {/* =================================================
            LANGUAGE
        ================================================= */}

        <section className="settings-card">

          <div className="settings-row">

            <div className="settings-row-icon">

              <Globe size={17} />

            </div>


            <div className="settings-row-content">

              <h3>
                Language
              </h3>

              <p>
                Choose the language used
                throughout the application.
              </p>

            </div>


            <select
              className="settings-select"
              value={language}
              onChange={(event) =>
                setLanguage(
                  event.target.value
                )
              }
            >

              <option value="English">
                English
              </option>

              <option value="Hindi">
                हिंदी
              </option>

              <option value="Marathi">
                मराठी
              </option>

              <option value="Punjabi">
                ਪੰਜਾਬੀ
              </option>

              <option value="Tamil">
                தமிழ்
              </option>

              <option value="Telugu">
                తెలుగు
              </option>

            </select>

          </div>

        </section>


        {/* =================================================
            COMPACT MODE
        ================================================= */}

        <section className="settings-card">

          <div className="settings-row">

            <div className="settings-row-icon">

              <LayoutDashboard size={17} />

            </div>


            <div className="settings-row-content">

              <h3>
                Compact dashboard
              </h3>

              <p>
                Reduce spacing to show more
                information on the screen.
              </p>

            </div>


            <Toggle
              enabled={compactMode}
              onClick={() =>
                setCompactMode(
                  !compactMode
                )
              }
            />

          </div>

        </section>


        {/* =================================================
            ACTIONS
        ================================================= */}

        <div className="settings-actions">

          <button
            type="button"
            className="settings-reset-button"
            onClick={resetSettings}
          >

            <RotateCcw size={15} />

            Reset

          </button>


          <button
            type="button"
            className="settings-save-button"
            onClick={saveSettings}
          >

            <Save size={15} />

            Save settings

          </button>


          {saved && (

            <span className="settings-saved">

              <CheckCircle2 size={14} />

              Settings saved

            </span>

          )}

        </div>

      </div>

    </div>

  );
}


/* =========================================================
   THEME OPTION
========================================================= */

function ThemeOption({
  icon,
  title,
  description,
  selected,
  onClick,
}) {

  return (

    <button
      type="button"
      className={`theme-option ${
        selected
          ? "selected"
          : ""
      }`}
      onClick={onClick}
    >

      <div className="theme-option-icon">

        {icon}

      </div>


      <div>

        <strong>
          {title}
        </strong>

        <span>
          {description}
        </span>

      </div>


      <div className="theme-radio">

        {selected && (
          <div />
        )}

      </div>

    </button>

  );

}


/* =========================================================
   TOGGLE
========================================================= */

function Toggle({
  enabled,
  onClick,
}) {

  return (

    <button
      type="button"
      className={`settings-toggle ${
        enabled
          ? "enabled"
          : ""
      }`}
      onClick={onClick}
      aria-pressed={enabled}
    >

      <span />

    </button>

  );

}


export default Settings;