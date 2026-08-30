import { useState } from "react";
import {
  Leaf,
  User,
  Phone,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  Sun,
  Moon,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useTheme } from "../context/ThemeContext";

function Signup() {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const [form, setForm] = useState({
    name: "",
    phone: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "Farmer",
    language: "English",
    terms: false,
  });

  const handleChange = (e) => {
    const {
      name,
      value,
      type,
      checked,
    } = e.target;

    setForm((previous) => ({
      ...previous,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (
      form.password !==
      form.confirmPassword
    ) {
      alert("Passwords do not match.");
      return;
    }

    if (!form.terms) {
      alert(
        "Please accept the terms and privacy policy."
      );
      return;
    }

    // Temporary frontend navigation.
    // Real registration will be connected to FastAPI later.
    navigate("/dashboard");
  };

  return (
    <div className="auth-page">

      {/* LEFT */}

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
            Join the future of farming
          </div>

          <h1>
            Your farm.
            <br />
            <span>Your intelligence.</span>
          </h1>

          <p>
            Create your AgriSphere account and
            bring climate, crop, market and
            government intelligence together.
          </p>

          <div className="signup-stat-grid">

            <div>
              <strong>8+</strong>
              <span>AI Agents</span>
            </div>

            <div>
              <strong>24/7</strong>
              <span>Intelligence</span>
            </div>

            <div>
              <strong>10+</strong>
              <span>Languages</span>
            </div>

          </div>

        </div>

        <div className="auth-visual-footer">
          Built for smarter agriculture 🌱
        </div>

      </section>

      {/* RIGHT */}

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

        <div className="auth-form-container signup-container">

          <div className="mobile-auth-brand">

            <div className="auth-logo">
              <Leaf size={25} />
            </div>

            <strong>
              AgriSphere <span>AI</span>
            </strong>

          </div>

          <div className="auth-heading">

            <p>GET STARTED</p>

            <h2>
              Create your account
            </h2>

            <span>
              Set up your personalized
              agriculture intelligence profile.
            </span>

          </div>

          <form onSubmit={handleSubmit}>

            {/* NAME + PHONE */}

            <div className="auth-two-column">

              <div className="auth-field">

                <label>
                  Full name
                </label>

                <div className="auth-input-wrapper">

                  <User size={17} />

                  <input
                    name="name"
                    type="text"
                    placeholder="Your name"
                    value={form.name}
                    onChange={handleChange}
                    required
                  />

                </div>

              </div>

              <div className="auth-field">

                <label>
                  Phone
                </label>

                <div className="auth-input-wrapper">

                  <Phone size={17} />

                  <input
                    name="phone"
                    type="tel"
                    placeholder="+91"
                    value={form.phone}
                    onChange={handleChange}
                    required
                  />

                </div>

              </div>

            </div>

            {/* EMAIL */}

            <div className="auth-field">

              <label>
                Email
              </label>

              <div className="auth-input-wrapper">

                <Mail size={17} />

                <input
                  name="email"
                  type="email"
                  placeholder="you@example.com"
                  value={form.email}
                  onChange={handleChange}
                  required
                />

              </div>

            </div>

            {/* PASSWORD */}

            <div className="auth-two-column">

              <div className="auth-field">

                <label>
                  Password
                </label>

                <div className="auth-input-wrapper">

                  <Lock size={17} />

                  <input
                    name="password"
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    placeholder="Create password"
                    value={form.password}
                    onChange={handleChange}
                    required
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowPassword(
                        !showPassword
                      )
                    }
                  >
                    {showPassword ? (
                      <EyeOff size={17} />
                    ) : (
                      <Eye size={17} />
                    )}
                  </button>

                </div>

              </div>

              <div className="auth-field">

                <label>
                  Confirm password
                </label>

                <div className="auth-input-wrapper">

                  <Lock size={17} />

                  <input
                    name="confirmPassword"
                    type={
                      showConfirmPassword
                        ? "text"
                        : "password"
                    }
                    placeholder="Repeat password"
                    value={
                      form.confirmPassword
                    }
                    onChange={handleChange}
                    required
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowConfirmPassword(
                        !showConfirmPassword
                      )
                    }
                  >
                    {showConfirmPassword ? (
                      <EyeOff size={17} />
                    ) : (
                      <Eye size={17} />
                    )}
                  </button>

                </div>

              </div>

            </div>

            {/* ROLE */}

            <div className="auth-field">

              <label>
                I am a
              </label>

              <div className="role-options">

                {[
                  "Farmer",
                  "Agricultural Officer",
                  "Researcher",
                ].map((role) => (

                  <label
                    key={role}
                    className={`role-option ${
                      form.role === role
                        ? "selected"
                        : ""
                    }`}
                  >

                    <input
                      type="radio"
                      name="role"
                      value={role}
                      checked={
                        form.role === role
                      }
                      onChange={handleChange}
                    />

                    <span>
                      {role}
                    </span>

                  </label>

                ))}

              </div>

            </div>

            {/* LANGUAGE */}

            <div className="auth-field">

              <label>
                Preferred language
              </label>

              <select
                name="language"
                value={form.language}
                onChange={handleChange}
                className="auth-select"
              >
                <option>English</option>
                <option>Hindi</option>
                <option>Marathi</option>
                <option>Gujarati</option>
                <option>Punjabi</option>
                <option>Bengali</option>
                <option>Tamil</option>
                <option>Telugu</option>
                <option>Kannada</option>
                <option>Malayalam</option>
              </select>

            </div>

            {/* TERMS */}

            <label className="remember-row">

              <input
                type="checkbox"
                name="terms"
                checked={form.terms}
                onChange={handleChange}
              />

              <span>
                I agree to the terms and privacy policy.
              </span>

            </label>

            <button
              type="submit"
              className="auth-submit"
            >
              <span>Create account</span>
              <ArrowRight size={19} />
            </button>

          </form>

          {/* LOGIN */}

          <p className="auth-switch">

            Already have an account?

            <button
              type="button"
              onClick={() => navigate("/login")}
            >
              Sign in
            </button>

          </p>

        </div>

      </section>

    </div>
  );
}

export default Signup;