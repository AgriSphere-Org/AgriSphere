import { useState } from "react";

import {
  CloudSun,
  MapPin,
  Sprout,
  Search,
  Loader2,
  Thermometer,
  Droplets,
  Wind,
  CloudRain,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  Activity,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";


function Climate() {

  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [village, setVillage] = useState("");
  const [crop, setCrop] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  const analyzeClimate = async (event) => {

    event.preventDefault();

    setError("");
    setResult(null);


    if (!state.trim()) {
      setError("Please enter your state.");
      return;
    }

    if (!district.trim()) {
      setError("Please enter your district.");
      return;
    }

    if (!crop.trim()) {
      setError("Please enter your crop.");
      return;
    }


    setLoading(true);


    try {

      const response = await fetch(
        `${API_BASE_URL}/weather`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            state: state.trim(),
            district: district.trim(),
            village: village.trim() || null,
            crop: crop.trim(),
          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to analyze climate."
        );

      }


      setResult(data);

    }

    catch (err) {

      console.error(err);

      setError(
        err.message ||
        "Unable to connect to Climate Intelligence Agent."
      );

    }

    finally {

      setLoading(false);

    }

  };


  return (

    <div className="agent-page">


      {/* HEADER */}

      <div className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <CloudSun size={14} />

            CLIMATE INTELLIGENCE

          </div>

          <h1>
            Understand your farm's weather
          </h1>

          <p>
            Get crop-focused weather analysis,
            climate risks and farming recommendations
            for your exact region.
          </p>

        </div>

        <div className="agent-header-icon">
          <CloudSun size={32} />
        </div>

      </div>


      {/* SEARCH */}

      <div className="agent-input-card">

        <div className="agent-card-heading">

          <div className="agent-card-icon">
            <MapPin size={18} />
          </div>

          <div>

            <h2>
              Farm location
            </h2>

            <p>
              Enter your location and crop to get
              a crop-specific climate analysis.
            </p>

          </div>

        </div>


        <form
          onSubmit={analyzeClimate}
          className="agent-form"
        >


          <div className="agent-field">

            <label>
              State
            </label>

            <input
              value={state}
              onChange={(e) =>
                setState(e.target.value)
              }
              placeholder="e.g. Punjab"
            />

          </div>


          <div className="agent-field">

            <label>
              District
            </label>

            <input
              value={district}
              onChange={(e) =>
                setDistrict(e.target.value)
              }
              placeholder="e.g. Amritsar"
            />

          </div>


          <div className="agent-field">

            <label>
              Village / Town
              <span>Optional</span>
            </label>

            <input
              value={village}
              onChange={(e) =>
                setVillage(e.target.value)
              }
              placeholder="e.g. Majitha"
            />

          </div>


          <div className="agent-field">

            <label>
              Crop
            </label>

            <input
              value={crop}
              onChange={(e) =>
                setCrop(e.target.value)
              }
              placeholder="e.g. Wheat"
            />

          </div>


          <button
            type="submit"
            className="agent-primary-button"
            disabled={loading}
          >

            {loading ? (

              <>
                <Loader2
                  size={17}
                  className="spin"
                />

                Analyzing...

              </>

            ) : (

              <>
                <Search size={17} />

                Analyze climate

              </>

            )}

          </button>

        </form>


        {error && (

          <div className="agent-error">

            <AlertTriangle size={16} />

            {error}

          </div>

        )}

      </div>


      {/* RESULTS */}

      {result && (

        <>

          {/* CURRENT WEATHER */}

          <div className="agent-section-title">

            <div>

              <span>
                CURRENT CONDITIONS
              </span>

              <h2>
                {result.location}
              </h2>

            </div>

          </div>


          <div className="weather-metric-grid">


            <WeatherMetric
              icon={<Thermometer size={20} />}
              label="Temperature"
              value={`${result.current_weather?.temperature ?? 0}°C`}
            />


            <WeatherMetric
              icon={<Droplets size={20} />}
              label="Humidity"
              value={`${result.current_weather?.humidity ?? 0}%`}
            />


            <WeatherMetric
              icon={<CloudRain size={20} />}
              label="Rainfall"
              value={`${result.current_weather?.rainfall ?? 0} mm`}
            />


            <WeatherMetric
              icon={<Wind size={20} />}
              label="Wind"
              value={`${result.current_weather?.wind_speed ?? 0} m/s`}
            />

          </div>


          {/* ADVISORY */}

          <div className="climate-advisory-card">

            <div className="climate-advisory-header">

              <div>

                <span>
                  CROP ADVISORY
                </span>

                <h2>
                  {result.crop
                    ? `${result.crop} weather analysis`
                    : "Farm climate analysis"}
                </h2>

              </div>

              <Activity size={24} />

            </div>


            <div className="climate-risk-grid">


              <RiskCard
                label="Farming condition"
                value={
                  result.advisory?.farming_condition ||
                  "Unknown"
                }
                positive
              />


              <RiskCard
                label="Heat stress"
                value={
                  result.advisory?.heat_stress ||
                  "Unknown"
                }
              />


              <RiskCard
                label="Drought risk"
                value={
                  result.advisory?.drought_risk ||
                  "Unknown"
                }
              />


              <RiskCard
                label="Flood risk"
                value={
                  result.advisory?.flood_risk ||
                  "Unknown"
                }
              />

            </div>


            <div className="climate-recommendation">

              <CheckCircle2 size={18} />

              <div>

                <strong>
                  Recommendation
                </strong>

                <p>
                  {result.advisory?.recommendation ||
                    "No recommendation available."}
                </p>

              </div>

            </div>


            <div className="climate-advice-grid">

              <div>

                <Droplets size={16} />

                <div>

                  <span>
                    Irrigation advice
                  </span>

                  <strong>
                    {result.advisory?.irrigation_advice ||
                      "Not available"}
                  </strong>

                </div>

              </div>


              <div>

                <Activity size={16} />

                <div>

                  <span>
                    Disease risk
                  </span>

                  <strong>
                    {result.advisory?.disease_risk ||
                      "Unknown"}
                  </strong>

                </div>

              </div>

            </div>

          </div>


          {/* ANALYTICS */}

          {result.analytics && (

            <div className="climate-analytics-card">

              <div className="agent-section-title">

                <div>

                  <span>
                    WEATHER ANALYTICS
                  </span>

                  <h2>
                    Crop-focused weather trends
                  </h2>

                </div>

                <TrendingUp size={21} />

              </div>


              <div className="analytics-placeholder">

                <TrendingUp size={32} />

                <h3>
                  Weather trend analysis
                </h3>

                <p>
                  Forecast analytics are available
                  from the Climate Intelligence Agent.
                </p>

              </div>

            </div>

          )}

        </>

      )}

    </div>

  );

}


/* =========================================================
   WEATHER METRIC
========================================================= */

function WeatherMetric({
  icon,
  label,
  value,
}) {

  return (

    <div className="weather-metric-card">

      <div className="weather-metric-icon">
        {icon}
      </div>

      <div>

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

      </div>

    </div>

  );

}


/* =========================================================
   RISK CARD
========================================================= */

function RiskCard({
  label,
  value,
  positive = false,
}) {

  const lower =
    String(value).toLowerCase();


  const good =
    positive ||
    lower === "low" ||
    lower === "excellent" ||
    lower === "good";


  return (

    <div className="climate-risk-card">

      <span>
        {label}
      </span>

      <strong
        className={
          good
            ? "risk-good"
            : "risk-warning"
        }
      >
        {value}
      </strong>

    </div>

  );

}


export default Climate;