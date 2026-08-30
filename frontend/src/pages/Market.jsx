import { useState } from "react";

import {
  TrendingUp,
  Search,
  MapPin,
  Sprout,
  Loader2,
  IndianRupee,
  ArrowUp,
  ArrowDown,
  Minus,
  BarChart3,
  Activity,
  CalendarDays,
  RefreshCw,
  AlertTriangle,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

function Market() {

  const [crop, setCrop] = useState("");

  const [state, setState] = useState("");

  const [district, setDistrict] = useState("");

  const [market, setMarket] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  /* =====================================================
     MARKET ANALYSIS
  ===================================================== */

  const handleAnalyze = async (event) => {

    event.preventDefault();

    setError("");
    setResult(null);


    if (!crop.trim()) {

      setError("Please enter a crop name.");

      return;
    }


    if (!state.trim()) {

      setError("Please enter your state.");

      return;
    }


    setLoading(true);


    try {

      const response = await fetch(
        `${API_BASE_URL}/market/analyze`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            crop: crop.trim(),

            state: state.trim(),

            district:
              district.trim() || null,

            market:
              market.trim() || null,

          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to fetch market information."
        );

      }


      setResult(data);

    } catch (err) {

      console.error(
        "Market analysis error:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to Market Intelligence Agent."
      );

    } finally {

      setLoading(false);

    }

  };


  /* =====================================================
     RESET
  ===================================================== */

  const resetMarket = () => {

    setCrop("");
    setState("");
    setDistrict("");
    setMarket("");

    setResult(null);
    setError("");

  };


  /* =====================================================
     HELPERS
  ===================================================== */

  const getValue = (...values) => {

    for (const value of values) {

      if (
        value !== undefined &&
        value !== null &&
        value !== ""
      ) {

        return value;

      }

    }

    return null;

  };


  const getTrend = (value) => {

    const text =
      String(value || "")
        .toLowerCase();


    if (
      text.includes("up") ||
      text.includes("increase") ||
      text.includes("rising") ||
      text.includes("bull")
    ) {

      return "up";

    }


    if (
      text.includes("down") ||
      text.includes("decrease") ||
      text.includes("fall") ||
      text.includes("bear")
    ) {

      return "down";

    }


    return "stable";

  };


  const getTrendIcon = (trend) => {

    if (trend === "up") {

      return <ArrowUp size={16} />;

    }


    if (trend === "down") {

      return <ArrowDown size={16} />;

    }


    return <Minus size={16} />;

  };


  const getTrendClass = (trend) => {

    if (trend === "up") {
      return "market-trend-up";
    }

    if (trend === "down") {
      return "market-trend-down";
    }

    return "market-trend-stable";

  };


  const formatPrice = (value) => {

    if (
      value === undefined ||
      value === null ||
      value === ""
    ) {

      return "—";

    }


    if (typeof value === "number") {

      return `₹${value.toLocaleString("en-IN")}`;

    }


    return String(value);

  };


  /* =====================================================
     NORMALIZE DATA
  ===================================================== */

  const currentPrice = result
    ? getValue(
        result.current_price,
        result.price,
        result.modal_price,
        result.currentPrice
      )
    : null;


  const minPrice = result
    ? getValue(
        result.min_price,
        result.minimum_price,
        result.minPrice
      )
    : null;


  const maxPrice = result
    ? getValue(
        result.max_price,
        result.maximum_price,
        result.maxPrice
      )
    : null;


  const trendValue = result
    ? getValue(
        result.trend,
        result.price_trend,
        result.market_trend,
        result.prediction
      )
    : null;


  const trend =
    getTrend(trendValue);


  const dataPoints =
    result?.prices ||
    result?.price_history ||
    result?.history ||
    result?.data ||
    result?.records ||
    [];


  const safeDataPoints =
    Array.isArray(dataPoints)
      ? dataPoints
      : [];


  const recommendation = result
    ? getValue(
        result.recommendation,
        result.advice,
        result.market_advice
      )
    : null;


  return (

    <div className="agent-page market-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <TrendingUp size={14} />

            MARKET INTELLIGENCE

          </div>


          <h1>
            Understand your crop's market
          </h1>


          <p>
            Track crop prices, identify market
            trends and make better selling decisions
            using agricultural market intelligence.
          </p>

        </div>


        <div className="agent-header-icon">

          <BarChart3 size={32} />

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
              Check market prices
            </h2>

            <p>
              Enter your crop and location to
              analyze available market information.
            </p>

          </div>

        </div>


        <form
          onSubmit={handleAnalyze}
          className="market-form"
        >


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
                setCrop(event.target.value)
              }
              placeholder="e.g. Wheat"
            />

          </div>


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
                setState(event.target.value)
              }
              placeholder="e.g. Maharashtra"
            />

          </div>


          {/* DISTRICT */}

          <div className="agent-field">

            <label>

              <MapPin size={14} />

              District

              <span>Optional</span>

            </label>


            <input
              type="text"
              value={district}
              onChange={(event) =>
                setDistrict(event.target.value)
              }
              placeholder="e.g. Nashik"
            />

          </div>


          {/* MARKET */}

          <div className="agent-field">

            <label>

              <BarChart3 size={14} />

              Market

              <span>Optional</span>

            </label>


            <input
              type="text"
              value={market}
              onChange={(event) =>
                setMarket(event.target.value)
              }
              placeholder="e.g. Lasalgaon"
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

                Analyzing...

              </>

            ) : (

              <>

                <Search size={17} />

                Analyze market

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

      {result && (

        <section className="market-results">


          {/* =================================================
              RESULT HEADER
          ================================================= */}

          <div className="agent-section-title">

            <div>

              <span>
                MARKET ANALYSIS
              </span>

              <h2>
                {crop} market overview
              </h2>

              <p>
                {district
                  ? `${district}, ${state}`
                  : state}
              </p>

            </div>


            <button
              type="button"
              className="market-refresh"
              onClick={handleAnalyze}
              disabled={loading}
            >

              <RefreshCw size={14} />

              Refresh

            </button>

          </div>


          {/* =================================================
              KPI CARDS
          ================================================= */}

          <div className="market-kpi-grid">


            <MarketKPI
              icon={<IndianRupee size={19} />}
              label="Current price"
              value={formatPrice(currentPrice)}
            />


            <MarketKPI
              icon={<TrendingUp size={19} />}
              label="Market trend"
              value={
                trendValue ||
                "Stable"
              }
              trend={trend}
            />


            <MarketKPI
              icon={<ArrowDown size={19} />}
              label="Minimum price"
              value={formatPrice(minPrice)}
            />


            <MarketKPI
              icon={<ArrowUp size={19} />}
              label="Maximum price"
              value={formatPrice(maxPrice)}
            />

          </div>


          {/* =================================================
              TREND CARD
          ================================================= */}

          <div className="market-main-grid">


            <div className="market-chart-card">


              <div className="market-card-heading">

                <div>

                  <span>
                    PRICE MOVEMENT
                  </span>

                  <h3>
                    Market price trend
                  </h3>

                </div>


                <div
                  className={`market-trend-badge ${getTrendClass(
                    trend
                  )}`}
                >

                  {getTrendIcon(trend)}

                  {trendValue ||
                    "Stable"}

                </div>

              </div>


              {safeDataPoints.length > 0 ? (

                <div className="market-chart">

                  <div className="market-y-axis">

                    <span>
                      High
                    </span>

                    <span>
                      Average
                    </span>

                    <span>
                      Low
                    </span>

                  </div>


                  <div className="market-bars">

                    {safeDataPoints.map(
                      (point, index) => {

                        const price =
                          typeof point ===
                          "object"
                            ? getValue(
                                point.price,
                                point.modal_price,
                                point.value
                              )
                            : point;


                        const numericPrice =
                          Number(price) || 0;


                        const maxChartPrice =
                          Math.max(
                            ...safeDataPoints.map(
                              (item) => {

                                const value =
                                  typeof item ===
                                  "object"
                                    ? getValue(
                                        item.price,
                                        item.modal_price,
                                        item.value
                                      )
                                    : item;

                                return Number(
                                  value
                                ) || 0;

                              }
                            ),
                            1
                          );


                        const height =
                          Math.max(
                            8,
                            (
                              numericPrice /
                              maxChartPrice
                            ) * 100
                          );


                        const label =
                          typeof point ===
                          "object"
                            ? getValue(
                                point.date,
                                point.day,
                                point.label
                              )
                            : `Day ${
                                index + 1
                              }`;


                        return (

                          <div
                            className="market-bar-wrapper"
                            key={index}
                          >

                            <div
                              className="market-bar"
                              style={{
                                height:
                                  `${height}%`,
                              }}
                              title={
                                `${formatPrice(
                                  numericPrice
                                )}`
                              }
                            />

                            <span>
                              {label}
                            </span>

                          </div>

                        );

                      }
                    )}

                  </div>

                </div>

              ) : (

                <div className="market-no-chart">

                  <BarChart3 size={32} />

                  <strong>
                    Price history unavailable
                  </strong>

                  <span>
                    The market service did not
                    return enough historical data
                    to draw the chart.
                  </span>

                </div>

              )}

            </div>


            {/* =================================================
                MARKET SUMMARY
            ================================================= */}

            <div className="market-summary-card">


              <div className="market-card-heading">

                <div>

                  <span>
                    AI INSIGHT
                  </span>

                  <h3>
                    Market outlook
                  </h3>

                </div>

              </div>


              <div
                className={`market-outlook-icon ${getTrendClass(
                  trend
                )}`}
              >

                {getTrendIcon(trend)}

              </div>


              <h4>
                {trendValue ||
                  "Market conditions are stable"}
              </h4>


              <p>
                {recommendation ||
                  "Continue monitoring local market prices before deciding when and where to sell your produce."}
              </p>


              <div className="market-location">

                <MapPin size={14} />

                <span>

                  {market
                    ? `${market}, `
                    : ""}

                  {district
                    ? `${district}, `
                    : ""}

                  {state}

                </span>

              </div>

            </div>

          </div>


          {/* =================================================
              DATA TABLE
          ================================================= */}

          {safeDataPoints.length > 0 && (

            <div className="market-table-card">


              <div className="market-card-heading">

                <div>

                  <span>
                    MARKET RECORDS
                  </span>

                  <h3>
                    Recent price observations
                  </h3>

                </div>

                <CalendarDays
                  size={18}
                />

              </div>


              <div className="market-table-wrapper">

                <table>

                  <thead>

                    <tr>

                      <th>
                        Date
                      </th>

                      <th>
                        Market
                      </th>

                      <th>
                        Price
                      </th>

                      <th>
                        Trend
                      </th>

                    </tr>

                  </thead>


                  <tbody>

                    {safeDataPoints.map(
                      (point, index) => {

                        const item =
                          typeof point ===
                          "object"
                            ? point
                            : {
                                price: point,
                              };


                        const price =
                          getValue(
                            item.price,
                            item.modal_price,
                            item.value
                          );


                        const date =
                          getValue(
                            item.date,
                            item.day,
                            item.label
                          ) ||
                          `Record ${index + 1}`;


                        const itemTrend =
                          getTrend(
                            getValue(
                              item.trend,
                              trendValue
                            )
                          );


                        return (

                          <tr key={index}>

                            <td>
                              {date}
                            </td>

                            <td>
                              {getValue(
                                item.market,
                                market
                              ) ||
                                "Market data"}
                            </td>

                            <td>
                              <strong>
                                {formatPrice(
                                  price
                                )}
                              </strong>
                            </td>

                            <td>

                              <span
                                className={`market-table-trend ${getTrendClass(
                                  itemTrend
                                )}`}
                              >

                                {getTrendIcon(
                                  itemTrend
                                )}

                                {itemTrend}

                              </span>

                            </td>

                          </tr>

                        );

                      }
                    )}

                  </tbody>

                </table>

              </div>

            </div>

          )}

        </section>

      )}

    </div>

  );
}


/* =========================================================
   MARKET KPI
========================================================= */

function MarketKPI({
  icon,
  label,
  value,
  trend,
}) {

  return (

    <div className="market-kpi">

      <div className="market-kpi-icon">

        {icon}

      </div>


      <div>

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

        {trend && (

          <small
            className={getTrendClassLocal(
              trend
            )}
          >

            {trend === "up"
              ? "Price rising"
              : trend === "down"
                ? "Price falling"
                : "Price stable"}

          </small>

        )}

      </div>

    </div>

  );

}


function getTrendClassLocal(trend) {

  if (trend === "up") {
    return "market-trend-up";
  }

  if (trend === "down") {
    return "market-trend-down";
  }

  return "market-trend-stable";

}


export default Market;