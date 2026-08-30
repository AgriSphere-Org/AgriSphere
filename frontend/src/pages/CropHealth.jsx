import { useEffect, useRef, useState } from "react";

import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  Clock3,
  ImagePlus,
  Leaf,
  RefreshCw,
  ShieldCheck,
  Sprout,
  Upload,
  XCircle,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

function CropHealth() {

  const fileInputRef = useRef(null);

  const [crop, setCrop] = useState("");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [history, setHistory] = useState([]);


  /* =========================================================
     LOAD HISTORY
  ========================================================= */

  useEffect(() => {

    try {

      const saved =
        localStorage.getItem(
          "agrisphere_crop_health_history"
        );

      if (saved) {
        setHistory(JSON.parse(saved));
      }

    } catch (error) {

      console.error(
        "Unable to load crop health history:",
        error
      );

    }

  }, []);


  /* =========================================================
     IMAGE SELECTION
  ========================================================= */

  const handleImageSelect = (event) => {

    const selectedFile =
      event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setError("");
    setResult(null);

    const allowedTypes = [
      "image/jpeg",
      "image/jpg",
      "image/png",
      "image/webp",
    ];

    if (
      !allowedTypes.includes(
        selectedFile.type
      )
    ) {

      setError(
        "Please select a JPG, JPEG, PNG or WEBP image."
      );

      return;
    }

    if (
      selectedFile.size >
      10 * 1024 * 1024
    ) {

      setError(
        "Image size must be less than 10 MB."
      );

      return;
    }

    setImage(selectedFile);

    const imageUrl =
      URL.createObjectURL(selectedFile);

    setPreview(imageUrl);
  };


  /* =========================================================
     REMOVE IMAGE
  ========================================================= */

  const removeImage = () => {

    setImage(null);

    setPreview("");

    setResult(null);

    setError("");

    if (fileInputRef.current) {

      fileInputRef.current.value = "";

    }
  };


  /* =========================================================
     ANALYZE CROP
  ========================================================= */

  const analyzeCrop = async (event) => {

    event.preventDefault();

    setError("");

    setResult(null);

    if (!image) {

      setError(
        "Please upload a crop image first."
      );

      return;
    }

    setLoading(true);

    try {

      const formData =
        new FormData();

      if (crop.trim()) {

        formData.append(
          "crop",
          crop.trim()
        );

      }

      formData.append(
        "image",
        image
      );

      const response =
        await fetch(
          `${API_BASE_URL}/crop-health/analyze`,
          {
            method: "POST",
            body: formData,
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Crop analysis failed."
        );

      }

      setResult(data);

      saveToHistory(data);

    } catch (error) {

      console.error(
        "Crop health analysis error:",
        error
      );

      setError(
        error.message ||
        "Unable to analyze crop image."
      );

    } finally {

      setLoading(false);

    }
  };


  /* =========================================================
     SAVE HISTORY
  ========================================================= */

  const saveToHistory = (data) => {

    const historyItem = {

      id: Date.now(),

      crop:
        data.crop ||
        data.detected_crop ||
        "Unknown",

      detected_crop:
        data.detected_crop ||
        "Unknown",

      health_status:
        data.health_status ||
        "Unknown",

      health_score:
        data.health_score ?? 0,

      disease:
        data.disease ||
        "None detected",

      severity:
        data.severity ||
        "Unknown",

      timestamp:
        new Date().toISOString(),

    };

    setHistory((previous) => {

      const updated = [
        historyItem,
        ...previous,
      ].slice(0, 20);

      localStorage.setItem(
        "agrisphere_crop_health_history",
        JSON.stringify(updated)
      );

      return updated;

    });

  };


  /* =========================================================
     CLEAR HISTORY
  ========================================================= */

  const clearHistory = () => {

    localStorage.removeItem(
      "agrisphere_crop_health_history"
    );

    setHistory([]);

  };


  /* =========================================================
     STATUS CLASS
  ========================================================= */

  const getStatusClass = (status) => {

    const value =
      String(status || "")
        .toLowerCase();

    if (
      value.includes("healthy")
    ) {

      return "health-good";

    }

    if (
      value.includes("moderate") ||
      value.includes("mild")
    ) {

      return "health-warning";

    }

    if (
      value.includes("severe") ||
      value.includes("unhealthy") ||
      value.includes("disease")
    ) {

      return "health-danger";

    }

    return "health-neutral";

  };


  /* =========================================================
     SCORE CLASS
  ========================================================= */

  const getScoreClass = (score) => {

    if (score >= 80) {
      return "score-good";
    }

    if (score >= 50) {
      return "score-warning";
    }

    return "score-danger";

  };


  /* =========================================================
     DATE
  ========================================================= */

  const formatDate = (timestamp) => {

    try {

      return new Date(
        timestamp
      ).toLocaleString(
        "en-IN",
        {
          day: "numeric",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        }
      );

    } catch {

      return "Unknown date";

    }

  };


  /* =========================================================
     RENDER
  ========================================================= */

  return (

    <div className="crop-health-page">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <section className="crop-health-header">

        <div>

          <div className="crop-health-eyebrow">

            <Leaf size={14} />

            CROP HEALTH INTELLIGENCE

          </div>

          <h1>
            Understand the health
            of your crop
          </h1>

          <p>
            Upload a crop image and let
            AgriSphere AI analyze visible
            health conditions, symptoms,
            disease and severity.
          </p>

        </div>

        <div className="crop-health-header-icon">

          <Sprout size={32} />

        </div>

      </section>


      {/* =====================================================
          ANALYSIS AREA
      ===================================================== */}

      <section className="crop-health-analysis-layout">


        {/* ===================================================
            UPLOAD
        =================================================== */}

        <div className="crop-upload-card">

          <div className="crop-card-heading">

            <div className="crop-card-icon">

              <ImagePlus size={20} />

            </div>

            <div>

              <h2>
                Analyze a crop
              </h2>

              <p>
                Upload a clear image of the
                crop leaf or plant.
              </p>

            </div>

          </div>


          {/* IMAGE */}

          {preview ? (

            <div className="crop-image-preview">

              <img
                src={preview}
                alt="Selected crop"
              />

              <button
                type="button"
                className="crop-remove-image"
                onClick={removeImage}
              >

                <XCircle size={20} />

              </button>

            </div>

          ) : (

            <button
              type="button"
              className="crop-upload-zone"
              onClick={() =>
                fileInputRef.current?.click()
              }
            >

              <div className="crop-upload-icon">

                <Upload size={24} />

              </div>

              <strong>
                Upload crop image
              </strong>

              <span>
                JPG, JPEG, PNG or WEBP
              </span>

              <small>
                Maximum size: 10 MB
              </small>

            </button>

          )}


          <input
            ref={fileInputRef}
            type="file"
            accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
            onChange={handleImageSelect}
            hidden
          />


          {/* CROP */}

          <div className="crop-health-field">

            <label htmlFor="crop-name">

              Crop name

              <span>
                Optional
              </span>

            </label>

            <input
              id="crop-name"
              type="text"
              value={crop}
              onChange={(event) =>
                setCrop(
                  event.target.value
                )
              }
              placeholder="e.g. Tomato, Rice, Wheat"
            />

            <small>
              Providing the crop name helps
              the AI compare the image with
              the farmer's crop.
            </small>

          </div>


          {/* BUTTON */}

          <button
            type="button"
            className="crop-analyze-button"
            disabled={
              loading ||
              !image
            }
            onClick={analyzeCrop}
          >

            {loading ? (

              <>
                <RefreshCw
                  size={17}
                  className="spin"
                />

                Analyzing image...
              </>

            ) : (

              <>
                <Activity size={17} />

                Analyze crop health
              </>

            )}

          </button>


          {/* ERROR */}

          {error && (

            <div className="crop-health-error">

              <AlertTriangle size={17} />

              <span>
                {error}
              </span>

            </div>

          )}

        </div>


        {/* ===================================================
            RESULT
        =================================================== */}

        <div className="crop-result-card">

          {!result ? (

            <div className="crop-result-empty">

              <div className="crop-result-empty-icon">

                <ShieldCheck size={30} />

              </div>

              <h2>
                Analysis results
              </h2>

              <p>
                Your crop health report will
                appear here after image analysis.
              </p>

            </div>

          ) : (

            <CropResult
              result={result}
              getStatusClass={getStatusClass}
              getScoreClass={getScoreClass}
            />

          )}

        </div>

      </section>


      {/* =====================================================
          DETAILS
      ===================================================== */}

      {result && (

        <section className="crop-health-details">

          <div className="crop-section-heading">

            <div>

              <span>
                AI ANALYSIS
              </span>

              <h2>
                What we found
              </h2>

            </div>

          </div>


          <div className="crop-details-grid">

            <div className="crop-detail-card">

              <span>
                Detected crop
              </span>

              <strong>
                {result.detected_crop ||
                  "Unknown"}
              </strong>

            </div>


            <div className="crop-detail-card">

              <span>
                Crop match
              </span>

              <strong>
                {result.crop_match
                  ? "Matched"
                  : "Not matched"}
              </strong>

            </div>


            <div className="crop-detail-card">

              <span>
                Image quality
              </span>

              <strong>
                {result.image_quality ||
                  "Unknown"}
              </strong>

            </div>


            <div className="crop-detail-card">

              <span>
                Severity
              </span>

              <strong>
                {result.severity ||
                  "Unknown"}
              </strong>

            </div>

          </div>


          {/* SYMPTOMS */}

          <div className="crop-symptoms-card">

            <div className="crop-symptoms-heading">

              <Activity size={18} />

              <h3>
                Visible symptoms
              </h3>

            </div>

            {result.visible_symptoms?.length ? (

              <ul>

                {result.visible_symptoms.map(
                  (symptom, index) => (

                    <li key={index}>

                      <span>
                        •
                      </span>

                      {symptom}

                    </li>

                  )
                )}

              </ul>

            ) : (

              <p>
                No visible symptoms were
                reported by the analysis.
              </p>

            )}

          </div>


          {/* SUMMARY */}

          <div className="crop-summary-card">

            <div className="crop-summary-heading">

              <Sprout size={18} />

              <h3>
                AI analysis summary
              </h3>

            </div>

            <p>
              {result.analysis_summary ||
                "No analysis summary available."}
            </p>

          </div>

        </section>

      )}


      {/* =====================================================
          HISTORY
      ===================================================== */}

      <section className="crop-health-history">

        <div className="crop-section-heading history-heading">

          <div>

            <span>
              MONITORING
            </span>

            <h2>
              Crop health history
            </h2>

            <p>
              Previous analyses saved on
              this device.
            </p>

          </div>


          {history.length > 0 && (

            <button
              type="button"
              className="clear-history-button"
              onClick={clearHistory}
            >
              Clear history
            </button>

          )}

        </div>


        {history.length === 0 ? (

          <div className="history-empty">

            <Clock3 size={24} />

            <p>
              No previous crop health analyses.
            </p>

          </div>

        ) : (

          <div className="history-list">

            {history.map((item) => (

              <div
                className="history-item"
                key={item.id}
              >

                <div className="history-item-icon">

                  {item.health_score >= 80 ? (

                    <CheckCircle2 size={18} />

                  ) : (

                    <AlertTriangle size={18} />

                  )}

                </div>


                <div className="history-item-main">

                  <strong>
                    {item.crop}
                  </strong>

                  <span>
                    {item.disease}
                  </span>

                  <small>
                    {formatDate(
                      item.timestamp
                    )}
                  </small>

                </div>


                <div className="history-item-score">

                  <strong>
                    {item.health_score}
                  </strong>

                  <span>
                    / 100
                  </span>

                </div>


                <div
                  className={`history-status ${getStatusClass(
                    item.health_status
                  )}`}
                >
                  {item.health_status}
                </div>

              </div>

            ))}

          </div>

        )}

      </section>

    </div>

  );
}


/* =========================================================
   RESULT COMPONENT
========================================================= */

function CropResult({
  result,
  getStatusClass,
  getScoreClass,
}) {

  const score =
    Number(result.health_score) || 0;

  return (

    <div className="crop-result">

      <div className="crop-result-heading">

        <div>

          <span>
            ANALYSIS COMPLETE
          </span>

          <h2>
            {result.crop ||
              result.detected_crop ||
              "Crop"}
          </h2>

        </div>


        <div
          className={`result-status ${getStatusClass(
            result.health_status
          )}`}
        >
          {result.health_status ||
            "Unknown"}
        </div>

      </div>


      {/* SCORE */}

      <div className="health-score-container">

        <div
          className={`health-score-ring ${getScoreClass(
            score
          )}`}
          style={{
            "--score":
              `${Math.max(
                0,
                Math.min(
                  score,
                  100
                )
              ) * 3.6}deg`,
          }}
        >

          <div className="health-score-inner">

            <strong>
              {score}
            </strong>

            <span>
              / 100
            </span>

          </div>

        </div>


        <div className="health-score-info">

          <strong>
            Crop health score
          </strong>

          <p>
            Overall health estimation
            based on AI vision analysis
            and observed severity.
          </p>

        </div>

      </div>


      {/* METRICS */}

      <div className="result-metrics">

        <div>

          <span>
            Disease
          </span>

          <strong>
            {result.disease ||
              "None detected"}
          </strong>

        </div>


        <div>

          <span>
            Severity
          </span>

          <strong>
            {result.severity ||
              "Unknown"}
          </strong>

        </div>


        <div>

          <span>
            Image quality
          </span>

          <strong>
            {result.image_quality ||
              "Unknown"}
          </strong>

        </div>

      </div>

    </div>

  );
}

export default CropHealth;