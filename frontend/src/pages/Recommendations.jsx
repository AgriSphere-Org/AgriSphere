import { useState } from "react";

import {
  BrainCircuit,
  MapPin,
  Sprout,
  Search,
  Loader2,
  Droplets,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  ThermometerSun,
  CloudRain,
  Leaf,
  RefreshCw,
  Lightbulb,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

function Recommendations() {

  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [crop, setCrop] = useState("");

  const [recommendations, setRecommendations] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  /* =====================================================
     GENERATE RECOMMENDATIONS
  ===================================================== */

  const handleGenerate = async (event) => {

    event.preventDefault();

    setError("");
    setRecommendations(null);


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

      /*
       * The exact request can vary depending on the
       * Recommendation Agent implementation.
       *
       * We send the core farmer information first.
       */

      const response = await fetch(
        `${API_BASE_URL}/recommendations/recommend`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            state: state.trim(),

            district: district.trim(),

            crop: crop.trim(),

          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to generate recommendations."
        );

      }


      setRecommendations(data);


    } catch (err) {

      console.error(
        "Recommendation error:",
        err
      );


      setError(
        err.message ||
        "Unable to connect to the AI Recommendation Agent."
      );

    } finally {

      setLoading(false);

    }

  };


  /* =====================================================
     RESET
  ===================================================== */

  const reset = () => {

    setState("");
    setDistrict("");
    setCrop("");

    setRecommendations(null);
    setError("");

  };


  /* =====================================================
     NORMALIZE RESPONSE
  ===================================================== */

  const extractRecommendations = () => {

    if (!recommendations) {
      return [];
    }


    if (
      Array.isArray(
        recommendations.recommendations
      )
    ) {

      return recommendations.recommendations;

    }


    if (
      Array.isArray(
        recommendations.results
      )
    ) {

      return recommendations.results;

    }


    if (
      Array.isArray(
        recommendations.advice
      )
    ) {

      return recommendations.advice;

    }


    if (
      Array.isArray(
        recommendations.actions
      )
    ) {

      return recommendations.actions;

    }


    return [];

  };


  const results =
    extractRecommendations();


  return (

    <div className="recommendations-page agent-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <BrainCircuit size={14} />

            AI FARM RECOMMENDATIONS

          </div>


          <h1>
            Know what your farm needs next
          </h1>


          <p>
            AgriSphere combines information from
            its intelligence agents to provide
            practical actions for your farm.
          </p>

        </div>


        <div className="agent-header-icon">

          <BrainCircuit size={31} />

        </div>

      </section>


      {/* =================================================
          INPUT
      ================================================= */}

      <section className="agent-input-card">

        <div className="agent-card-heading">

          <div className="agent-card-icon">

            <Search size={18} />

          </div>


          <div>

            <h2>
              Tell us about your farm
            </h2>

            <p>
              Start with these basic details.
            </p>

          </div>

        </div>


        <form
          onSubmit={handleGenerate}
          className="recommendation-form"
        >


          {/* STATE */}

          <div className="agent-field">

            <label>

              <MapPin size={14} />

              State

            </label>


            <input
              type="text"
              value={state}
              onChange={(event) =>
                setState(
                  event.target.value
                )
              }
              placeholder="e.g. Punjab"
            />

          </div>


          {/* DISTRICT */}

          <div className="agent-field">

            <label>

              <MapPin size={14} />

              District

            </label>


            <input
              type="text"
              value={district}
              onChange={(event) =>
                setDistrict(
                  event.target.value
                )
              }
              placeholder="e.g. Amritsar"
            />

          </div>


          {/* CROP */}

          <div className="agent-field">

            <label>

              <Sprout size={14} />

              Crop

            </label>


            <input
              type="text"
              value={crop}
              onChange={(event) =>
                setCrop(
                  event.target.value
                )
              }
              placeholder="e.g. Wheat"
            />

          </div>


          {/* BUTTON */}

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

                Analyzing farm...

              </>

            ) : (

              <>

                <BrainCircuit size={17} />

                Generate recommendations

              </>

            )}

          </button>

        </form>


        {/* ERROR */}

        {error && (

          <div className="agent-error">

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

      {recommendations && (

        <section className="recommendation-results">


          {/* HEADER */}

          <div className="agent-section-title">

            <div>

              <span>
                AI FARM ANALYSIS
              </span>

              <h2>
                Your recommendations
              </h2>

              <p>
                Actions generated from your
                current farm information.
              </p>

            </div>


            <button
              type="button"
              className="recommendation-reset"
              onClick={reset}
            >

              <RefreshCw size={14} />

              New analysis

            </button>

          </div>


          {/* =================================================
              SUMMARY CARDS
          ================================================= */}

          <div className="recommendation-summary-grid">

            <SummaryCard
              icon={<Droplets size={17} />}
              title="Irrigation"
              value="Monitor"
              text="Check water requirement regularly."
            />


            <SummaryCard
              icon={<ThermometerSun size={17} />}
              title="Climate"
              value="Monitor"
              text="Use current weather before major activities."
            />


            <SummaryCard
              icon={<Leaf size={17} />}
              title="Crop health"
              value="Track"
              text="Regularly inspect leaves and plant growth."
            />


            <SummaryCard
              icon={<ShieldAlert size={17} />}
              title="Risk"
              value="Review"
              text="Check weather and disease warnings."
            />

          </div>


          {/* =================================================
              BACKEND RESULTS
          ================================================= */}

          {results.length > 0 ? (

            <div className="recommendation-list">

              {results.map(
                (item, index) => (

                  <RecommendationCard
                    key={index}
                    item={item}
                    index={index}
                  />

                )
              )}

            </div>

          ) : (

            /*
             * If the backend returns a different structure,
             * don't leave the page blank.
             */

            <div className="recommendation-fallback">

              <div className="recommendation-fallback-icon">

                <Lightbulb size={21} />

              </div>


              <div>

                <h3>
                  Analysis completed
                </h3>

                <p>
                  The Recommendation Agent returned
                  a result, but no recommendation list
                  was detected in the response.
                </p>

                <pre>
                  {JSON.stringify(
                    recommendations,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>

          )}


        </section>

      )}

    </div>

  );
}


/* =========================================================
   SUMMARY CARD
========================================================= */

function SummaryCard({
  icon,
  title,
  value,
  text,
}) {

  return (

    <div className="recommendation-summary-card">

      <div className="recommendation-summary-icon">

        {icon}

      </div>


      <span>
        {title}
      </span>


      <strong>
        {value}
      </strong>


      <p>
        {text}
      </p>

    </div>

  );

}


/* =========================================================
   RECOMMENDATION CARD
========================================================= */

function RecommendationCard({
  item,
  index,
}) {

  const title =
    item.title ||
    item.name ||
    item.category ||
    `Recommendation ${index + 1}`;


  const description =
    item.description ||
    item.recommendation ||
    item.advice ||
    item.message ||
    item.text ||
    "Follow the recommended farming practice.";


  const priority =
    item.priority ||
    item.risk ||
    "Normal";


  return (

    <article className="recommendation-card">

      <div className="recommendation-card-number">

        {index + 1}

      </div>


      <div className="recommendation-card-content">

        <div className="recommendation-card-heading">

          <div>

            <span>
              AI RECOMMENDATION
            </span>

            <h3>
              {title}
            </h3>

          </div>


          <span
            className={`recommendation-priority ${
              String(priority)
                .toLowerCase()
                .includes("high")
                ? "high"
                : String(priority)
                    .toLowerCase()
                    .includes("medium")
                  ? "medium"
                  : "normal"
            }`}
          >

            {priority}

          </span>

        </div>


        <p>
          {description}
        </p>


        <div className="recommendation-card-footer">

          <div>

            <CheckCircle2 size={13} />

            Recommended action

          </div>

        </div>

      </div>

    </article>

  );

}


export default Recommendations;