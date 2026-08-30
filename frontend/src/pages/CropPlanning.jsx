import { useState } from "react";

import {
  Sprout,
  MapPin,
  FlaskConical,
  Search,
  Loader2,
  CheckCircle2,
  Droplets,
  CalendarDays,
  IndianRupee,
  Clock3,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  Leaf,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";


function CropPlanning() {

  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [soilPh, setSoilPh] = useState("");

  const [recommendations, setRecommendations] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [expandedCrop, setExpandedCrop] =
    useState(null);


  /* =====================================================
     FIND RECOMMENDED CROPS
  ===================================================== */

  const handleRecommend = async (event) => {

    event.preventDefault();

    setError("");
    setRecommendations([]);
    setExpandedCrop(null);


    /* -----------------------------------------------------
       VALIDATION
    ----------------------------------------------------- */

    if (!city.trim()) {

      setError(
        "Please enter your city or district."
      );

      return;
    }


    if (!soilPh) {

      setError(
        "Please enter your soil pH."
      );

      return;
    }


    const numericPh = Number(soilPh);


    if (
      Number.isNaN(numericPh) ||
      numericPh < 0 ||
      numericPh > 14
    ) {

      setError(
        "Soil pH must be between 0 and 14."
      );

      return;
    }


    setLoading(true);


    try {

      /* ---------------------------------------------------
         API REQUEST
      --------------------------------------------------- */

      const response = await fetch(
        `${API_BASE_URL}/crop/recommend`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            city: city.trim(),

            soil_ph: numericPh,

            state: state.trim() || null,

          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to generate crop recommendations."
        );

      }


      const results =
        Array.isArray(data.recommendations)
          ? data.recommendations
          : [];


      if (results.length === 0) {

        setError(
          "No crop recommendations were found. Check your location and soil pH."
        );

        return;
      }


      setRecommendations(results);

    }


    catch (err) {

      console.error(
        "Crop planning error:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to the Crop Planning Agent."
      );

    }


    finally {

      setLoading(false);

    }

  };


  /* =====================================================
     RESET
  ===================================================== */

  const resetPlanning = () => {

    setCity("");
    setState("");
    setSoilPh("");

    setRecommendations([]);

    setError("");

    setExpandedCrop(null);

  };


  /* =====================================================
     SUITABILITY CLASS
  ===================================================== */

  const getSuitabilityClass = (suitability) => {

    const value =
      String(suitability || "").toLowerCase();


    if (value === "excellent") {
      return "crop-suitability-excellent";
    }


    if (value === "very good") {
      return "crop-suitability-very-good";
    }


    if (value === "good") {
      return "crop-suitability-good";
    }


    if (value === "moderate") {
      return "crop-suitability-moderate";
    }


    return "crop-suitability-poor";

  };


  /* =====================================================
     SCORE CLASS
  ===================================================== */

  const getScoreClass = (score) => {

    const numericScore =
      Number(score) || 0;


    if (numericScore >= 80) {
      return "crop-score-high";
    }


    if (numericScore >= 60) {
      return "crop-score-medium";
    }


    return "crop-score-low";

  };


  /* =====================================================
     RENDER
  ===================================================== */

  return (

    <div className="crop-planning-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="crop-planning-header">

        <div>

          <div className="crop-planning-eyebrow">

            <Sprout size={14} />

            CROP PLANNING INTELLIGENCE

          </div>


          <h1>
            Find the right crop
            <br />
            for your land
          </h1>


          <p>
            AgriSphere combines current climate,
            soil pH and regional suitability to
            identify crops that are most suitable
            for your farm.
          </p>

        </div>


        <div className="crop-planning-header-icon">

          <Leaf size={31} />

        </div>

      </section>


      {/* =================================================
          INPUT CARD
      ================================================= */}

      <section className="crop-planning-input-card">


        <div className="crop-planning-card-title">

          <div className="crop-planning-title-icon">

            <Search size={19} />

          </div>


          <div>

            <h2>
              Tell us about your farm
            </h2>

            <p>
              Only a few details are needed
              to generate recommendations.
            </p>

          </div>

        </div>


        <form
          onSubmit={handleRecommend}
          className="crop-planning-form"
        >


          {/* =================================================
              CITY / DISTRICT
          ================================================= */}

          <div className="crop-planning-field">

            <label htmlFor="planning-city">

              <MapPin size={14} />

              City / District

            </label>


            <input
              id="planning-city"
              type="text"
              value={city}
              onChange={(event) =>
                setCity(event.target.value)
              }
              placeholder="e.g. Amritsar"
            />

          </div>


          {/* =================================================
              STATE
          ================================================= */}

          <div className="crop-planning-field">

            <label htmlFor="planning-state">

              <MapPin size={14} />

              State

              <span>
                Optional
              </span>

            </label>


            <input
              id="planning-state"
              type="text"
              value={state}
              onChange={(event) =>
                setState(event.target.value)
              }
              placeholder="e.g. Punjab"
            />

          </div>


          {/* =================================================
              SOIL PH
          ================================================= */}

          <div className="crop-planning-field">

            <label htmlFor="planning-ph">

              <FlaskConical size={14} />

              Soil pH

            </label>


            <input
              id="planning-ph"
              type="number"
              min="0"
              max="14"
              step="0.1"
              value={soilPh}
              onChange={(event) =>
                setSoilPh(event.target.value)
              }
              placeholder="e.g. 6.5"
            />


            <small>
              If you don't know your soil pH,
              use your latest soil test report.
            </small>

          </div>


          {/* =================================================
              BUTTON
          ================================================= */}

          <button
            type="submit"
            className="crop-planning-search-button"
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

                Recommend crops

              </>

            )}

          </button>


        </form>


        {/* =================================================
            ERROR
        ================================================= */}

        {error && (

          <div className="crop-planning-error">

            <AlertTriangle size={17} />

            <span>
              {error}
            </span>

          </div>

        )}

      </section>


      {/* =================================================
          RESULTS
      ================================================= */}

      {recommendations.length > 0 && (

        <section className="crop-planning-results">


          {/* =================================================
              RESULTS HEADER
          ================================================= */}

          <div className="crop-planning-results-header">

            <div>

              <span>
                AI ANALYSIS
              </span>

              <h2>
                Recommended crops
              </h2>

              <p>
                Ranked according to climate,
                soil and regional suitability.
              </p>

            </div>


            <button
              type="button"
              onClick={resetPlanning}
              className="crop-planning-reset"
            >
              New analysis
            </button>

          </div>


          {/* =================================================
              TOP RECOMMENDATION
          ================================================= */}

          {recommendations[0] && (

            <TopCropCard
              crop={recommendations[0]}
              getSuitabilityClass={
                getSuitabilityClass
              }
            />

          )}


          {/* =================================================
              ALL RECOMMENDATIONS
          ================================================= */}

          <div className="crop-recommendation-list">


            {recommendations.map(
              (crop, index) => {

                const isExpanded =
                  expandedCrop === index;


                return (

                  <div
                    className={`crop-recommendation-card ${
                      index === 0
                        ? "top-recommendation"
                        : ""
                    }`}
                    key={`${crop.crop}-${index}`}
                  >


                    {/* =========================================
                        CARD HEADER
                    ========================================= */}

                    <button
                      type="button"
                      className="crop-recommendation-main"
                      onClick={() =>
                        setExpandedCrop(
                          isExpanded
                            ? null
                            : index
                        )
                      }
                    >


                      <div className="crop-rank">

                        #{index + 1}

                      </div>


                      <div className="crop-main-info">

                        <div className="crop-name-row">

                          <h3>
                            {crop.crop}
                          </h3>


                          <span
                            className={`crop-suitability ${getSuitabilityClass(
                              crop.suitability
                            )}`}
                          >
                            {crop.suitability}
                          </span>

                        </div>


                        <p>
                          {crop.category ||
                            "Agricultural crop"}
                        </p>

                      </div>


                      <div className="crop-confidence">

                        <strong>
                          {Number(
                            crop.confidence || 0
                          ).toFixed(1)}
                          %
                        </strong>

                        <span>
                          Confidence
                        </span>

                      </div>


                      <div className="crop-expand">

                        {isExpanded ? (

                          <ChevronUp size={17} />

                        ) : (

                          <ChevronDown size={17} />

                        )}

                      </div>

                    </button>


                    {/* =========================================
                        EXPANDED DETAILS
                    ========================================= */}

                    {isExpanded && (

                      <div className="crop-recommendation-details">


                        {/* =====================================
                            SCORE METRICS
                        ===================================== */}

                        <div className="crop-detail-metrics">


                          <Metric
                            icon={
                              <CheckCircle2
                                size={16}
                              />
                            }
                            label="Climate"
                            value={
                              `${Number(
                                crop.climate_score || 0
                              ).toFixed(0)}%`
                            }
                            score={
                              crop.climate_score
                            }
                            getScoreClass={
                              getScoreClass
                            }
                          />


                          <Metric
                            icon={
                              <FlaskConical
                                size={16}
                              />
                            }
                            label="Soil"
                            value={
                              `${Number(
                                crop.soil_score || 0
                              ).toFixed(0)}%`
                            }
                            score={
                              crop.soil_score
                            }
                            getScoreClass={
                              getScoreClass
                            }
                          />


                          <Metric
                            icon={
                              <MapPin
                                size={16}
                              />
                            }
                            label="Region"
                            value={
                              `${Number(
                                crop.region_score || 0
                              ).toFixed(0)}%`
                            }
                            score={
                              crop.region_score
                            }
                            getScoreClass={
                              getScoreClass
                            }
                          />

                        </div>


                        {/* =====================================
                            CROP INFORMATION
                        ===================================== */}

                        <div className="crop-information-grid">


                          <InfoItem
                            icon={
                              <CalendarDays
                                size={15}
                              />
                            }
                            label="Season"
                            value={
                              crop.season
                            }
                          />


                          <InfoItem
                            icon={
                              <IndianRupee
                                size={15}
                              />
                            }
                            label="Expected profit"
                            value={
                              crop.expected_profit
                            }
                          />


                          <InfoItem
                            icon={
                              <Droplets
                                size={15}
                              />
                            }
                            label="Water requirement"
                            value={
                              crop.water_requirement
                            }
                          />


                          <InfoItem
                            icon={
                              <Clock3
                                size={15}
                              />
                            }
                            label="Duration"
                            value={
                              crop.duration_days
                                ? `${crop.duration_days} days`
                                : "Not available"
                            }
                          />

                        </div>


                        {/* =====================================
                            REASONS
                        ===================================== */}

                        <div className="crop-reasons">

                          <h4>
                            Why this crop?
                          </h4>


                          {Array.isArray(
                            crop.reasons
                          ) &&
                            crop.reasons.map(
                              (
                                reason,
                                reasonIndex
                              ) => (

                                <div
                                  className="crop-reason"
                                  key={
                                    reasonIndex
                                  }
                                >

                                  <CheckCircle2
                                    size={14}
                                  />

                                  <span>
                                    {reason}
                                  </span>

                                </div>

                              )
                            )}

                        </div>

                      </div>

                    )}

                  </div>

                );

              }
            )}

          </div>

        </section>

      )}

    </div>

  );

}


/* =========================================================
   TOP CROP CARD
========================================================= */

function TopCropCard({
  crop,
  getSuitabilityClass,
}) {

  return (

    <div className="top-crop-card">


      {/* ===================================================
          CROP NAME
      =================================================== */}

      <div className="top-crop-left">


        <div className="top-crop-badge">

          <CheckCircle2 size={13} />

          BEST MATCH

        </div>


        <h3>
          {crop.crop}
        </h3>


        <p>
          {crop.category ||
            "Recommended crop"}
        </p>


        <div
          className={`top-crop-suitability ${getSuitabilityClass(
            crop.suitability
          )}`}
        >
          {crop.suitability}
        </div>

      </div>


      {/* ===================================================
          CONFIDENCE
      =================================================== */}

      <div className="top-crop-score">

        <span>
          Confidence
        </span>


        <strong>
          {Number(
            crop.confidence || 0
          ).toFixed(1)}
          %
        </strong>


        <div className="top-crop-progress">

          <div
            style={{
              width: `${Math.min(
                Math.max(
                  Number(
                    crop.confidence || 0
                  ),
                  0
                ),
                100
              )}%`,
            }}
          />

        </div>

      </div>


      {/* ===================================================
          SUMMARY
      =================================================== */}

      <div className="top-crop-summary">


        <div>

          <CalendarDays size={15} />

          <span>
            {crop.season ||
              "Season not available"}
          </span>

        </div>


        <div>

          <Droplets size={15} />

          <span>
            {crop.water_requirement ||
              "Water requirement unavailable"}
          </span>

        </div>


        <div>

          <Clock3 size={15} />

          <span>
            {crop.duration_days
              ? `${crop.duration_days} days`
              : "Duration unavailable"}
          </span>

        </div>

      </div>

    </div>

  );

}


/* =========================================================
   METRIC
========================================================= */

function Metric({
  icon,
  label,
  value,
  score,
  getScoreClass,
}) {

  return (

    <div className="crop-metric">


      <div className="crop-metric-top">

        <span className="crop-metric-icon">

          {icon}

        </span>


        <span>
          {label}
        </span>

      </div>


      <strong
        className={getScoreClass(score)}
      >
        {value}
      </strong>


    </div>

  );

}


/* =========================================================
   INFO ITEM
========================================================= */

function InfoItem({
  icon,
  label,
  value,
}) {

  return (

    <div className="crop-info-item">


      <div className="crop-info-icon">

        {icon}

      </div>


      <div>

        <span>
          {label}
        </span>


        <strong>
          {value || "Not available"}
        </strong>

      </div>


    </div>

  );

}


/* =========================================================
   EXPORT
========================================================= */

export default CropPlanning;