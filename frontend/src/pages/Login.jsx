import { useState } from "react";
import {
  Eye,
  EyeOff,
  Leaf,
  Mail,
  Lock,
  ArrowRight,
  Sun,
  Moon,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useTheme } from "../context/ThemeContext";

function Login() {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [form, setForm] = useState({
    email: "",
    password: "",
    remember: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Temporary frontend navigation.
    // Real authentication will be connected to FastAPI later.
    navigate("/dashboard");
  };

  return (
    <div className="auth-page">

      {/* LEFT BRANDING */}

      <section className="auth-visual">

        <div className="auth-brand">

          <div className="auth-logo">
            <Leaf size={28} />
          </div>

          <div>
            <strong>AgriSphere</strong>
            <span>AI</span>
          </div>

        </div>

        <div className="auth-visual-content">

          <div className="auth-badge">
            <span className="status-pulse" />
            AI-powered agriculture intelligence
          </div>

          <h1>
            Smarter farming.
            <br />
            <span>Better decisions.</span>
          </h1>

          <p>
            Climate intelligence, crop health, market insights
            and government assistance — all in one intelligent
            agriculture platform.
          </p>

          <div className="auth-feature-grid">

            <div className="auth-feature">
              <span>🌦️</span>
              <div>
                <strong>Climate Intelligence</strong>
                <small>Weather insights for farming</small>
              </div>
            </div>

            <div className="auth-feature">
              <span>🌱</span>
              <div>
                <strong>Crop Intelligence</strong>
                <small>AI-powered crop analysis</small>
              </div>
            </div>

            <div className="auth-feature">
              <span>📈</span>
              <div>
                <strong>Market Insights</strong>
                <small>Understand crop price trends</small>
              </div>
            </div>

            <div className="auth-feature">
              <span>🏛️</span>
              <div>
                <strong>Government Schemes</strong>
                <small>Find benefits you may qualify for</small>
              </div>
            </div>

          </div>

        </div>

        <div className="auth-visual-footer">
          © 2026 AgriSphere AI
        </div>

      </section>

      {/* LOGIN */}

      <section className="auth-form-section">

        <button
          className="auth-theme-button"
          onClick={toggleTheme}
          title="Toggle theme"
        >
          {theme === "light" ? (
            <Moon size={18} />
          ) : (
            <Sun size={18} />
          )}
        </button>

        <div className="auth-form-container">

          <div className="mobile-auth-brand">

            <div className="auth-logo">
              <Leaf size={25} />
            </div>

            <strong>
              AgriSphere <span>AI</span>
            </strong>

          </div>

          <div className="auth-heading">

            <p>WELCOME BACK</p>

            <h2>
              Sign in to AgriSphere
            </h2>

            <span>
              Continue your journey toward smarter farming.
            </span>

          </div>

          <form onSubmit={handleSubmit}>

            {/* EMAIL */}

            <div className="auth-field">

              <label htmlFor="email">
                Email or phone
              </label>

              <div className="auth-input-wrapper">

                <Mail size={18} />

                <input
                  id="email"
                  name="email"
                  type="text"
                  placeholder="Enter your email or phone"
                  value={form.email}
                  onChange={handleChange}
                  required
                />

              </div>

            </div>

            {/* PASSWORD */}

            <div className="auth-field">

              <div className="auth-label-row">

                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-button"
                  onClick={() =>
                    alert(
                      "Password recovery will be connected later."
                    )
                  }
                >
                  Forgot password?
                </button>

              </div>

              <div className="auth-input-wrapper">

                <Lock size={18} />

                <input
                  id="password"
                  name="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={form.password}
                  onChange={handleChange}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>

              </div>

            </div>

            {/* REMEMBER */}

            <label className="remember-row">

              <input
                type="checkbox"
                name="remember"
                checked={form.remember}
                onChange={handleChange}
              />

              <span>
                Remember me
              </span>

            </label>

            {/* SUBMIT */}

            <button
              type="submit"
              className="auth-submit"
            >
              <span>Sign in</span>
              <ArrowRight size={19} />
            </button>

          </form>

          {/* DIVIDER */}

          <div className="auth-divider">
            <span>or continue with</span>
          </div>

          {/* GOOGLE */}

          <button
            type="button"
            className="google-button"
            onClick={() =>
              alert(
                "Google authentication will be connected later."
              )
            }
          >
            <span className="google-icon">
              G
            </span>

            Continue with Google
          </button>

          {/* SIGNUP */}

          <p className="auth-switch">

            Don't have an account?

            <button
              type="button"
              onClick={() => navigate("/signup")}
            >
              Create account
            </button>

          </p>

        </div>

      </section>

    </div>
  );
}

export default Login;