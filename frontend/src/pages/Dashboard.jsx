import {
  CloudSun,
  Droplets,
  ThermometerSun,
  Wind,
  Sprout,
  TrendingUp,
  Landmark,
  Leaf,
  ArrowUpRight,
  AlertTriangle,
  CheckCircle2,
  Activity,
} from "lucide-react";

function Dashboard() {
  return (
    <div className="dashboard-page">

      {/* Header */}

      <div className="dashboard-header">

        <div>
          <p className="dashboard-eyebrow">
            FARM INTELLIGENCE
          </p>

          <h1>
            Good morning, Farmer 🌱
          </h1>

          <p>
            Here's what AgriSphere AI found for your farm today.
          </p>
        </div>

        <div className="location-chip">
          <span className="location-dot" />
          Maharashtra, India
        </div>

      </div>

      {/* =====================================================
          WEATHER SUMMARY
      ===================================================== */}

      <section className="dashboard-section">

        <div className="section-heading">

          <div>
            <h2>Today's farm conditions</h2>

            <p>
              Current climate intelligence for your location.
            </p>
          </div>

          <button className="dashboard-link">
            View climate
            <ArrowUpRight size={15} />
          </button>

        </div>

        <div className="weather-dashboard-grid">

          {/* Main weather card */}

          <div className="weather-main-card">

            <div className="weather-card-top">

              <div>
                <span>Current temperature</span>

                <strong>28°</strong>

                <p>
                  Feels like 30°C
                </p>
              </div>

              <div className="weather-icon-large">
                <CloudSun size={52} />
              </div>

            </div>

            <div className="weather-condition">
              Good conditions for farming
            </div>

          </div>

          {/* Temperature */}

          <div className="metric-card">

            <div className="metric-icon">
              <ThermometerSun size={20} />
            </div>

            <span>Temperature</span>

            <strong>28°C</strong>

            <small>
              Optimal range
            </small>

          </div>

          {/* Humidity */}

          <div className="metric-card">

            <div className="metric-icon">
              <Droplets size={20} />
            </div>

            <span>Humidity</span>

            <strong>67%</strong>

            <small>
              Moderate
            </small>

          </div>

          {/* Wind */}

          <div className="metric-card">

            <div className="metric-icon">
              <Wind size={20} />
            </div>

            <span>Wind speed</span>

            <strong>12 km/h</strong>

            <small>
              Safe
            </small>

          </div>

        </div>

      </section>

      {/* =====================================================
          AI STATUS
      ===================================================== */}

      <section className="dashboard-section">

        <div className="section-heading">

          <div>
            <h2>AI farm intelligence</h2>

            <p>
              A quick overview from your agriculture agents.
            </p>
          </div>

        </div>

        <div className="agent-grid">

          {/* Crop health */}

          <div className="agent-card">

            <div className="agent-card-header">

              <div className="agent-icon">
                <Leaf size={20} />
              </div>

              <span className="agent-status good">
                Healthy
              </span>

            </div>

            <h3>
              Crop Health
            </h3>

            <strong className="agent-value">
              86%
            </strong>

            <p>
              Your crop is currently showing healthy
              growth indicators.
            </p>

            <button className="card-action">
              Analyze crop
              <ArrowUpRight size={14} />
            </button>

          </div>

          {/* Crop planning */}

          <div className="agent-card">

            <div className="agent-card-header">

              <div className="agent-icon">
                <Sprout size={20} />
              </div>

                <span className="agent-status good">
                  Recommended
                </span>

            </div>

            <h3>
              Crop Planning
            </h3>

            <strong className="agent-value">
              8 crops
            </strong>

            <p>
              AI identified suitable crops based on
              your climate and soil.
            </p>

            <button className="card-action">
              View recommendations
              <ArrowUpRight size={14} />
            </button>

          </div>

          {/* Market */}

          <div className="agent-card">

            <div className="agent-card-header">

              <div className="agent-icon">
                <TrendingUp size={20} />
              </div>

              <span className="agent-status positive">
                Rising
              </span>

            </div>

            <h3>
              Market Intelligence
            </h3>

            <strong className="agent-value">
              +8.4%
            </strong>

            <p>
              Your selected crop is showing a positive
              market trend.
            </p>

            <button className="card-action">
              View market
              <ArrowUpRight size={14} />
            </button>

          </div>

          {/* Government */}

          <div className="agent-card">

            <div className="agent-card-header">

              <div className="agent-icon">
                <Landmark size={20} />
              </div>

              <span className="agent-status info">
                5 matches
              </span>

            </div>

            <h3>
              Government Schemes
            </h3>

            <strong className="agent-value">
              5
            </strong>

            <p>
              Government schemes may be available
              for your farm.
            </p>

            <button className="card-action">
              Explore schemes
              <ArrowUpRight size={14} />
            </button>

          </div>

        </div>

      </section>

      {/* =====================================================
          FARM ALERTS + RECOMMENDATION
      ===================================================== */}

      <section className="dashboard-bottom-grid">

        {/* Alerts */}

        <div className="dashboard-panel">

          <div className="panel-heading">

            <div>
              <h2>Farm alerts</h2>

              <p>
                Things that may require your attention.
              </p>
            </div>

            <Activity size={19} />

          </div>

          <div className="alert-list">

            <div className="farm-alert">

              <div className="alert-icon warning">
                <AlertTriangle size={18} />
              </div>

              <div>
                <strong>
                  Monitor soil moisture
                </strong>

                <p>
                  Moisture levels may decrease during
                  the next few days.
                </p>
              </div>

            </div>

            <div className="farm-alert">

              <div className="alert-icon success">
                <CheckCircle2 size={18} />
              </div>

              <div>
                <strong>
                  Weather looks favorable
                </strong>

                <p>
                  Current conditions are suitable for
                  normal farm activities.
                </p>
              </div>

            </div>

          </div>

        </div>

        {/* Recommendation */}

        <div className="dashboard-panel recommendation-panel">

          <div className="recommendation-glow" />

          <div className="panel-heading">

            <div>
              <h2>
                AI recommendation
              </h2>

              <p>
                From AgriSphere Recommendation Agent
              </p>
            </div>

            <div className="ai-badge">
              AI
            </div>

          </div>

          <div className="recommendation-content">

            <div className="recommendation-icon">
              <Sprout size={23} />
            </div>

            <div>

              <h3>
                Conditions look favorable today
              </h3>

              <p>
                Based on the current climate conditions,
                continue your regular irrigation schedule.
                Avoid unnecessary watering while humidity
                remains moderate.
              </p>

            </div>

          </div>

          <button className="recommendation-button">
            View full recommendation
            <ArrowUpRight size={15} />
          </button>

        </div>

      </section>

    </div>
  );
}

export default Dashboard;