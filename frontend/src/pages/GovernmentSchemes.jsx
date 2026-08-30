import { useState } from "react";

import {
  Landmark,
  Search,
  MapPin,
  Sprout,
  Ruler,
  Droplets,
  User,
  CalendarDays,
  Loader2,
  ExternalLink,
  CheckCircle2,
  Clock3,
  AlertTriangle,
  ShieldCheck,
  FileText,
  RefreshCw,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

function GovernmentSchemes() {

  const [state, setState] = useState("");

  const [farmerCategory, setFarmerCategory] =
    useState("");

  const [farmSize, setFarmSize] =
    useState("");

  const [crop, setCrop] =
    useState("");

  const [irrigation, setIrrigation] =
    useState("");

  const [gender, setGender] =
    useState("");

  const [age, setAge] =
    useState("");

  const [schemes, setSchemes] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  /* =====================================================
     SEARCH SCHEMES
  ===================================================== */

  const handleSearch = async (event) => {

    event.preventDefault();

    setError("");
    setSchemes([]);


    if (!state.trim()) {

      setError(
        "Please select or enter your state."
      );

      return;
    }


    if (!farmerCategory) {

      setError(
        "Please select your farmer category."
      );

      return;
    }


    if (!farmSize) {

      setError(
        "Please enter your farm size."
      );

      return;
    }


    if (!crop.trim()) {

      setError(
        "Please enter your main crop."
      );

      return;
    }


    if (!irrigation) {

      setError(
        "Please select your irrigation type."
      );

      return;
    }


    if (!gender) {

      setError(
        "Please select your gender."
      );

      return;
    }


    if (!age) {

      setError(
        "Please enter your age."
      );

      return;
    }


    const numericFarmSize =
      Number(farmSize);

    const numericAge =
      Number(age);


    if (
      Number.isNaN(numericFarmSize) ||
      numericFarmSize <= 0
    ) {

      setError(
        "Please enter a valid farm size."
      );

      return;
    }


    if (
      Number.isNaN(numericAge) ||
      numericAge < 18 ||
      numericAge > 120
    ) {

      setError(
        "Please enter a valid age between 18 and 120."
      );

      return;
    }


    setLoading(true);


    try {

      const response =
        await fetch(
          `${API_BASE_URL}/government/recommend`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({

              state:
                state.trim(),

              farmer_category:
                farmerCategory,

              farm_size:
                numericFarmSize,

              crop:
                crop.trim(),

              irrigation:
                irrigation,

              gender:
                gender,

              age:
                numericAge,

            }),
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to find government schemes."
        );

      }


      const results =
        Array.isArray(
          data.recommendations
        )
          ? data.recommendations
          : [];


      setSchemes(results);


      if (results.length === 0) {

        setError(
          "No matching government schemes were found for the information provided."
        );

      }

    } catch (err) {

      console.error(
        "Government scheme error:",
        err
      );


      setError(
        err.message ||
        "Unable to connect to Government Scheme Agent."
      );

    } finally {

      setLoading(false);

    }

  };


  /* =====================================================
     RESET
  ===================================================== */

  const resetSearch = () => {

    setState("");
    setFarmerCategory("");
    setFarmSize("");
    setCrop("");
    setIrrigation("");
    setGender("");
    setAge("");

    setSchemes([]);
    setError("");

  };


  return (

    <div className="agent-page government-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <Landmark size={14} />

            GOVERNMENT SCHEME INTELLIGENCE

          </div>


          <h1>
            Find schemes you may be eligible for
          </h1>


          <p>
            AgriSphere checks agricultural schemes
            against your farming profile and helps
            you reach the official application page.
          </p>

        </div>


        <div className="agent-header-icon">

          <Landmark size={32} />

        </div>

      </section>


      {/* =================================================
          SEARCH CARD
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
              These details help us identify
              potentially relevant schemes.
            </p>

          </div>

        </div>


        <form
          onSubmit={handleSearch}
          className="government-form"
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
              placeholder="e.g. Maharashtra"
            />

          </div>


          {/* CATEGORY */}

          <div className="agent-field">

            <label>

              <User size={14} />

              Farmer category

            </label>


            <select
              value={farmerCategory}
              onChange={(event) =>
                setFarmerCategory(
                  event.target.value
                )
              }
            >

              <option value="">
                Select category
              </option>

              <option value="Small">
                Small
              </option>

              <option value="Marginal">
                Marginal
              </option>

              <option value="Medium">
                Medium
              </option>

              <option value="Large">
                Large
              </option>

            </select>

          </div>


          {/* FARM SIZE */}

          <div className="agent-field">

            <label>

              <Ruler size={14} />

              Farm size

            </label>


            <div className="government-input-with-unit">

              <input
                type="number"
                min="0"
                step="0.1"
                value={farmSize}
                onChange={(event) =>
                  setFarmSize(
                    event.target.value
                  )
                }
                placeholder="e.g. 2.5"
              />

              <span>
                acres
              </span>

            </div>

          </div>


          {/* CROP */}

          <div className="agent-field">

            <label>

              <Sprout size={14} />

              Main crop

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


          {/* IRRIGATION */}

          <div className="agent-field">

            <label>

              <Droplets size={14} />

              Irrigation

            </label>


            <select
              value={irrigation}
              onChange={(event) =>
                setIrrigation(
                  event.target.value
                )
              }
            >

              <option value="">
                Select irrigation
              </option>

              <option value="Rainfed">
                Rainfed
              </option>

              <option value="Drip">
                Drip
              </option>

              <option value="Sprinkler">
                Sprinkler
              </option>

              <option value="Canal">
                Canal
              </option>

              <option value="Borewell">
                Borewell
              </option>

              <option value="Other">
                Other
              </option>

            </select>

          </div>


          {/* GENDER */}

          <div className="agent-field">

            <label>

              <User size={14} />

              Gender

            </label>


            <select
              value={gender}
              onChange={(event) =>
                setGender(
                  event.target.value
                )
              }
            >

              <option value="">
                Select gender
              </option>

              <option value="Male">
                Male
              </option>

              <option value="Female">
                Female
              </option>

              <option value="Other">
                Other
              </option>

            </select>

          </div>


          {/* AGE */}

          <div className="agent-field">

            <label>

              <CalendarDays size={14} />

              Age

            </label>


            <input
              type="number"
              min="18"
              max="120"
              value={age}
              onChange={(event) =>
                setAge(
                  event.target.value
                )
              }
              placeholder="e.g. 42"
            />

          </div>


          {/* BUTTON */}

          <button
            type="submit"
            className="agent-primary-button government-search-button"
            disabled={loading}
          >

            {loading ? (

              <>

                <Loader2
                  size={17}
                  className="spin"
                />

                Finding schemes...

              </>

            ) : (

              <>

                <Search size={17} />

                Find eligible schemes

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

      {schemes.length > 0 && (

        <section className="government-results">


          {/* RESULTS HEADER */}

          <div className="agent-section-title">

            <div>

              <span>
                ELIGIBILITY ANALYSIS
              </span>

              <h2>
                Schemes found for you
              </h2>

              <p>
                {schemes.length} potentially
                relevant scheme
                {schemes.length !== 1
                  ? "s"
                  : ""}{" "}
                identified.
              </p>

            </div>


            <button
              type="button"
              className="government-reset"
              onClick={resetSearch}
            >

              <RefreshCw size={14} />

              New search

            </button>

          </div>


          {/* SCHEME LIST */}

          <div className="government-scheme-list">

            {schemes.map(
              (scheme, index) => (

                <SchemeCard
                  key={
                    scheme.scheme_name ||
                    index
                  }
                  scheme={scheme}
                  index={index}
                />

              )
            )}

          </div>


          {/* DISCLAIMER */}

          <div className="government-disclaimer">

            <ShieldCheck size={17} />

            <div>

              <strong>
                Important
              </strong>

              <p>
                AgriSphere provides eligibility
                guidance based on the information
                available in its scheme database.
                Final eligibility and application
                approval are determined by the
                respective government authority.
              </p>

            </div>

          </div>

        </section>

      )}

    </div>

  );
}


/* =========================================================
   SCHEME CARD
========================================================= */

function SchemeCard({
  scheme,
  index,
}) {

  const confidence =
    Number(
      scheme.confidence || 0
    );


  const progress =
    Math.min(
      Math.max(
        confidence,
        0
      ),
      100
    );


  const applicationStatus =
    scheme.application_status ||
    scheme.status ||
    "Not started";


  const applicationProgress =
    Number(
      scheme.application_progress ??
      scheme.progress ??
      0
    );


  const officialLink =
    scheme.official_link ||
    scheme.application_link ||
    scheme.apply_url ||
    "";


  const benefit =
    scheme.benefit ||
    "Benefits depend on the scheme and applicant eligibility.";


  const isComplete =
    applicationProgress >= 100;


  return (

    <article className="government-scheme-card">


      {/* =================================================
          CARD HEADER
      ================================================= */}

      <div className="government-scheme-top">


        <div className="government-scheme-rank">

          #{index + 1}

        </div>


        <div className="government-scheme-title">

          <div className="government-scheme-tag">

            <Landmark size={11} />

            GOVERNMENT SCHEME

          </div>


          <h3>
            {scheme.scheme_name}
          </h3>

        </div>


        <div className="scheme-confidence">

          <span>
            MATCH
          </span>

          <strong>
            {confidence}%
          </strong>

        </div>

      </div>


      {/* =================================================
          BENEFIT
      ================================================= */}

      <div className="government-benefit">

        <div className="government-benefit-icon">

          <IndianRupeeIcon />

        </div>


        <div>

          <span>
            BENEFIT
          </span>

          <strong>
            {benefit}
          </strong>

        </div>

      </div>


      {/* =================================================
          APPLICATION PROGRESS
      ================================================= */}

      <div className="application-progress-section">


        <div className="application-progress-header">

          <div>

            <span>
              APPLICATION PROGRESS
            </span>

            <strong>
              {applicationStatus}
            </strong>

          </div>


          <span>
            {applicationProgress}%
          </span>

        </div>


        <div className="application-progress-bar">

          <div
            style={{
              width: `${Math.min(
                Math.max(
                  applicationProgress,
                  0
                ),
                100
              )}%`,
            }}
          />

        </div>


        <div className="application-steps">

          <ApplicationStep
            label="Eligibility"
            active={true}
            complete={confidence >= 70}
          />

          <ApplicationStep
            label="Application"
            active={
              applicationProgress >= 25
            }
            complete={
              applicationProgress >= 50
            }
          />

          <ApplicationStep
            label="Submitted"
            active={
              applicationProgress >= 50
            }
            complete={
              applicationProgress >= 75
            }
          />

          <ApplicationStep
            label="Approved"
            active={
              applicationProgress >= 75
            }
            complete={
              applicationProgress >= 100
            }
          />

        </div>

      </div>


      {/* =================================================
          ACTIONS
      ================================================= */}

      <div className="government-scheme-actions">


        {officialLink ? (

          <a
            href={officialLink}
            target="_blank"
            rel="noopener noreferrer"
            className="government-apply-button"
          >

            <ExternalLink size={15} />

            {isComplete
              ? "View official page"
              : "Apply on official website"}

          </a>

        ) : (

          <button
            type="button"
            className="government-apply-button disabled"
            disabled
          >

            <FileText size={15} />

            Official link unavailable

          </button>

        )}


        <div className="official-source">

          <ShieldCheck size={13} />

          Official source

        </div>

      </div>

    </article>

  );
}


/* =========================================================
   APPLICATION STEP
========================================================= */

function ApplicationStep({
  label,
  active,
  complete,
}) {

  return (

    <div
      className={`application-step ${
        active
          ? "active"
          : ""
      }`}
    >

      <div className="application-step-dot">

        {complete ? (

          <CheckCircle2 size={12} />

        ) : active ? (

          <Clock3 size={11} />

        ) : (

          <span />

        )}

      </div>


      <span>
        {label}
      </span>

    </div>

  );
}


/* =========================================================
   RUPEE ICON
========================================================= */

function IndianRupeeIcon() {

  return (
    <span
      style={{
        fontSize: "18px",
        fontWeight: 800,
      }}
    >
      ₹
    </span>
  );

}


export default GovernmentSchemes;